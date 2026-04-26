from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


SUPPORTED_DOCUMENT_SUFFIXES = {".txt", ".md", ".markdown", ".pdf", ".docx"}


class DocumentIngestionError(ValueError):
    pass


def extract_document_text(file_path: Path, original_name: str | None = None) -> tuple[str, str | None]:
    suffix = Path(original_name or file_path.name).suffix.lower()
    if suffix not in SUPPORTED_DOCUMENT_SUFFIXES:
        return "", None

    if suffix in {".txt", ".md", ".markdown"}:
        return file_path.read_text(encoding="utf-8", errors="ignore"), suffix.lstrip(".")
    if suffix == ".docx":
        return _extract_docx_text(file_path), "docx"
    if suffix == ".pdf":
        return _extract_pdf_text(file_path), "pdf"

    return "", None


def _extract_docx_text(file_path: Path) -> str:
    with ZipFile(file_path) as docx:
        xml_bytes = docx.read("word/document.xml")

    root = ET.fromstring(xml_bytes)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace))
        if text.strip():
            paragraphs.append(text.strip())
    return "\n".join(paragraphs)


def _extract_pdf_text(file_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise DocumentIngestionError("PDF extraction requires the `pypdf` package.") from exc

    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(page.strip() for page in pages if page.strip())
