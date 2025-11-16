from django.urls import path
from .views import UploadDocumentAPIView, ListDocumentsAPIView, SearchDocumentsAPIView

urlpatterns = [
    path("upload/", UploadDocumentAPIView.as_view()),
    path("documents/", ListDocumentsAPIView.as_view()),
    path("search/", SearchDocumentsAPIView.as_view()),
]
