from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image
from pypdf import PdfReader


def extract_pdf(file_path: str | Path) -> list[dict]:
    """
    Extract text from each page of a PDF.

    Uses normal PDF text extraction first.
    Falls back to OCR for pages with no usable text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Question paper not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}"
        )

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""
        text = text.strip()

        # ------------------------------------------
        # OCR fallback for scanned pages
        # ------------------------------------------

        if not text:

            document = pymupdf.open(str(file_path))

            try:
                pdf_page = document[page_number - 1]

                pixmap = pdf_page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False,
                )

                image = Image.frombytes(
                    "RGB",
                    [
                        pixmap.width,
                        pixmap.height,
                    ],
                    pixmap.samples,
                )

                text = pytesseract.image_to_string(
                    image
                ).strip()

            finally:
                document.close()

        pages.append(
            {
                "page": page_number,
                "text": text,
            }
        )

    return pages