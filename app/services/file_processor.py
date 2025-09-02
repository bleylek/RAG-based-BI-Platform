from PyPDF2 import PdfReader
from docx import Document
import os


def extract_text(file_storage):
    filename = file_storage.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_storage)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_storage)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(file_storage)
    else:
        return ""


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()


def extract_text_from_txt(file):
    return file.read().decode("utf-8").strip()
