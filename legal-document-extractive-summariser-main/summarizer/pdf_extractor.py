from PyPDF2 import PdfReader


def extract_pdf_text(filepath):

    text = ""

    try:

        reader = PdfReader(filepath)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    except Exception as e:

        print("PDF extraction error:", e)

    return text