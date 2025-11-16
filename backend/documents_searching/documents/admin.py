from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "filename",
        "normalized_filename",
        "category",
        "uploaded_at",
    )
    search_fields = (
        "filename",
        "normalized_filename",
        "keywords",
        "category",
    )
    list_filter = ("category", "uploaded_at")
