import os

from docx import Document

from summarizer.pdf_extractor import extract_pdf_text
from summarizer.ocr import extract_text_with_ocr


def extract_document_text(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    # ==========================================
    # PDF
    # ==========================================

    if extension == ".pdf":

        text = extract_pdf_text(filepath)

        # OCR fallback for scanned PDFs

        if not text.strip():

            text = extract_text_with_ocr(filepath)

        return text


    # ==========================================
    # DOCX
    # ==========================================

    elif extension == ".docx":

        document = Document(filepath)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:

                paragraphs.append(text)

        return "\n".join(paragraphs)


    # ==========================================
    # TXT
    # ==========================================

    elif extension == ".txt":

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read()

        except UnicodeDecodeError:

            with open(
                filepath,
                "r",
                encoding="latin-1"
            ) as file:

                return file.read()


    # ==========================================
    # UNSUPPORTED
    # ==========================================

    return ""