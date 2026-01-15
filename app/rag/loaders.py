import fitz
from PyPDF2 import PdfReader
from PIL import Image
import io
from typing import List, Tuple

from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.rag.constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def load_pdf_text(
    pdf_path: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    reader = PdfReader(pdf_path)
    raw_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            raw_text += page_text + "\n"

    return split_text(raw_text, chunk_size, chunk_overlap)


def extract_images_and_tables(
    pdf_path: str
) -> Tuple[list, list]:
    doc = fitz.open(pdf_path)
    images = []
    tables = []  # placeholder for future table extraction

    for page_idx, page in enumerate(doc):
        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            images.append(
                (f"Page {page_idx + 1}, Image {img_idx + 1}", image)
            )

    return images, tables
