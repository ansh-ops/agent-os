from pathlib import Path

from app.services.document_ingestion import extract_document_text


def test_extract_markdown_text(tmp_path: Path) -> None:
    document = tmp_path / "brief.md"
    document.write_text("# Brief\nAgent OS coordinates specialist agents.", encoding="utf-8")

    text, file_type = extract_document_text(document, "brief.md")

    assert file_type == "md"
    assert "Agent OS coordinates specialist agents" in text


def test_unsupported_file_returns_empty_text(tmp_path: Path) -> None:
    document = tmp_path / "image.png"
    document.write_bytes(b"not a document")

    text, file_type = extract_document_text(document, "image.png")

    assert text == ""
    assert file_type is None
