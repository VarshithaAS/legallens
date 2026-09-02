import pymupdf
import pytesseract
from PIL import Image


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_with_ocr(filepath):

    ocr_text = ""

    try:

        pdf_document = pymupdf.open(filepath)

        for page_number, page in enumerate(pdf_document):

            print(
                "OCR processing page:",
                page_number + 1
            )

            # Convert PDF page into image
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            # Convert image to PIL
            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # Read text using Tesseract
            page_text = pytesseract.image_to_string(
                image
            )

            ocr_text += page_text + " "

        pdf_document.close()

    except Exception as e:

        print("OCR ERROR:", e)

    return ocr_text