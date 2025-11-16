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

# Download stopwords once
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))


# --------------------------
#   TEXT NORMALIZATION
# --------------------------

def normalize_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    return text


# --------------------------
#   FILENAME NORMALIZATION
# --------------------------

def normalize_filename(name):
    """
    Converts 'TimeTable (1).pdf' → 'time table (1).pdf'
    Allows search: 'time table', 'timetable', 'table', etc.
    """
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)  # split camelCase or PascalCase
    name = name.replace("_", " ")
    name = " ".join(name.split())
    return name.lower()


# --------------------------
#   TEXT EXTRACTION HELPERS
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


# --------------------------
#   AUTOMATIC CATEGORIZATION
# --------------------------

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
#      UPLOAD DOCUMENT
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

        # Save document
        doc = Document.objects.create(
            filename=file.name,
            normalized_filename=normalized_name,
            file=file,
            content=extracted_text,
            keywords=keywords,
            category=category
        )

        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response({"message": "Use POST to upload document"})


# --------------------------
#   LIST DOCUMENTS
# --------------------------

class ListDocumentsAPIView(APIView):
    def get(self, request):
        docs = Document.objects.all().order_by('-uploaded_at')
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)


# --------------------------
#   SEARCH DOCUMENTS
# --------------------------

class SearchDocumentsAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        category_filter = request.GET.get("category", "").strip()

        docs = Document.objects.all()

        # Apply search query OR logic
        if query:
            docs = docs.filter(
                Q(filename__icontains=query) |
                Q(normalized_filename__icontains=query) |  # <-- NEW important line
                Q(content__icontains=query) |
                Q(keywords__icontains=query)
            )

        # Category filter
        if category_filter and category_filter.lower() != "all":
            docs = docs.filter(category__icontains=category_filter)

        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)
