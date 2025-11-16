# RapidQuest Challenge - Knowledge Discovery & Internal Search

## Aim
Build a smart internal search tool for marketing teams that indexes all internal documents and digital assets, delivers fast and relevant results, and helps teams find information instantly.

---

## Problem Statement
Marketing teams generate massive amounts of documents — but finding the right file becomes challenging as content becomes scattered. This leads to wasted time and inconsistent messaging.

**Challenge Objectives:**
- Index internal documents and digital assets.
- Enable smart search across multiple formats (PDF, DOCX).
- Automatically categorize documents by topic/project/team.
- Preview or link directly to files.
- Provide a clean UI optimized for quick access.

---

## Objective
- Enable fast retrieval of marketing and other internal documents.
- Reduce search time and improve productivity.
- Provide meaningful categorization to organize documents.
- Support multiple document formats with preview functionality.

---

## Tech Stack

**Frontend:**
- React.js
- HTML, CSS, Bootstrap

**Backend:**
- Python Django, Django REST Framework
- SQLite database
- Libraries: PyPDF2, python-docx, NLTK, python-magic, pytesseract

**Other Tools:**
- Node.js, npm (frontend)
- Vite (frontend bundler)
- Git & GitHub

---

## Features
- Upload documents (PDF/DOCX)
- Automatic text extraction
- Keyword generation for better search
- Automatic document categorization
- Search by keyword and/or category
- Preview documents from dashboard
- Display all documents when search bar is cleared

---

## Project Structure
```
Hackathon/
├── backend/
│   ├── venv/
│   ├── manage.py
│   ├── requirements.txt
│   └── ... (Django app files)
├── frontend/
│   ├── node_modules/
│   ├── .env
│   ├── package.json
│   └── src/
├── .gitignore
└── README.md
```

---

## Installation & Setup Instructions

### Backend
1. Navigate to the backend folder:
```bash
cd backend
```
2. Create and activate virtual environment:
- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
- Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run Django server:
```bash
python manage.py runserver
```
Backend runs at `http://127.0.0.1:8000`.

---

### Frontend
1. Navigate to the frontend folder:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Add `.env` file in frontend folder with:
```
VITE_API_URL=http://127.0.0.1:8000
```
4. Run frontend:
```bash
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## Usage
1. Open frontend URL in browser.
2. Dashboard displays all uploaded documents by default.
3. Use search bar to filter documents by keywords.
4. Select category from dropdown to filter by category.
5. Upload documents via "Upload Document" page (supports PDF & DOCX).
6. Clear search bar to view all documents again.

---

## How It Works
- **UploadDocumentAPIView**: Handles uploading and processing of files. Extracts text, generates keywords, normalizes filenames, and categorizes documents automatically.
- **ListDocumentsAPIView**: Returns all documents in the system.
- **SearchDocumentsAPIView**: Supports searching by keyword and filtering by category. Clears search to display all documents.

**Automatic Categorization Example:**
- Keywords like "project", "plan", "hackathon" → Project/Hackathon
- Keywords like "marketing", "brand", "campaign" → Marketing
- Keywords like "finance", "budget", "sales" → Finance/Sales
- Keywords like "UI", "frontend", "app" → Tech
- Anything else → General

---

## Notes
- Supports PDF and DOCX file formats.
- Keyword extraction ignores common stopwords using NLTK.
- Normalizes filenames to improve search accuracy.

---

## Future Improvements
- Add user authentication and permissions.
- Support more file formats (Excel, PPTX).
- Full-text search with ranking.
- Integrate advanced AI-based search for relevance scoring.

---
