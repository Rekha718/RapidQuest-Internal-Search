from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer

# Extraction imports
import PyPDF2
from docx import Document as DocxDocument
import nltk
from nltk.corpus import stopwords
import string
import re

# Appwrite imports
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile  # <-- for unique file IDs

# Download stopwords once
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

# Appwrite config
APPWRITE_ENDPOINT = "https://fra.cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "69199dd4001999027b50"
APPWRITE_BUCKET_ID = "69199e4b0022548436b1"
APPWRITE_API_KEY = "YOUR_APPWRITE_API_KEY_HERE"

client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
storage = Storage(client)


# --------------------------
# TEXT NORMALIZATION
# --------------------------
def normalize_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    return text

def normalize_filename(name):
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    name = name.replace("_", " ")
    name = " ".join(name.split())
    return name.lower()


# --------------------------
# TEXT EXTRACTION
# --------------------------
def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                page_text = normalize_text(page_text)
                text += page_text + " "
        return text.strip()
    except:
        return ""

def extract_text_from_docx(file):
    try:
        doc = DocxDocument(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return normalize_text(text)
    except:
        return ""


def generate_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 3]
    freq = {}
    for w in filtered:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_words = [w[0] for w in sorted_words[:5]]
    return ", ".join(top_words)


def categorize_document(keywords):
    keywords_lower = keywords.lower()
    if any(k in keywords_lower for k in ['project', 'plan', 'hackathon']):
        return "Project/Hackathon"
    elif any(k in keywords_lower for k in ['marketing', 'brand', 'campaign']):
        return "Marketing"
    elif any(k in keywords_lower for k in ['finance', 'budget', 'invoice', 'sales', 'revenue']):
        return "Finance/Sales"
    elif any(k in keywords_lower for k in ['ui', 'app', 'frontend']):
        return "Tech"
    else:
        return "General"


# --------------------------
# UPLOAD DOCUMENT
# --------------------------
class UploadDocumentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data.get("file")
        filename = file.name.lower()

        # Extract content
        if filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(file)
        else:
            return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize filename
        normalized_name = normalize_filename(file.name)

        # Generate keywords + category
        keywords = generate_keywords(extracted_text)
        category = categorize_document(keywords)

        # Upload to Appwrite
        appwrite_file = storage.create_file(
            bucket_id=APPWRITE_BUCKET_ID,
            file_id=InputFile.unique(),  # correct usage
            file=file
        )

        # Save document with Appwrite file ID
        doc = Document.objects.create(
            filename=file.name,
            normalized_filename=normalized_name,
            file_id=appwrite_file["$id"],
            content=extracted_text,
            keywords=keywords,
            category=category
        )

        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response({"message": "Use POST to upload document"})


# --------------------------
# LIST DOCUMENTS
# --------------------------
class ListDocumentsAPIView(APIView):
    def get(self, request):
        docs = Document.objects.all().order_by('-uploaded_at')
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)


# --------------------------
# SEARCH DOCUMENTS
# --------------------------
class SearchDocumentsAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        category_filter = request.GET.get("category", "").strip()
        docs = Document.objects.all()

        if query:
            docs = docs.filter(
                Q(filename__icontains=query) |
                Q(normalized_filename__icontains=query) |
                Q(content__icontains=query) |
                Q(keywords__icontains=query)
            )

        if category_filter and category_filter.lower() != "all":
            docs = docs.filter(category__icontains=category_filter)

        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)
