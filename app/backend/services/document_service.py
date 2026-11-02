
from pathlib import Path

# Resolve project root from this file's location.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


def list_documents():
    """Return metadata for all available text documents."""

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        documents.append({
            "id": file_path.stem,
            "filename": file_path.name,
            "size_bytes": file_path.stat().st_size
        })

    return documents


def get_document(document_id: str):
    """Return a document's content by its identifier."""

    # Only permit simple document identifiers.
    if not document_id or not all(
        char.isalnum() or char in "_-"
        for char in document_id
    ):
        return None

    file_path = DOCUMENTS_DIR / f"{document_id}.txt"

    if not file_path.is_file():
        return None

    return {
        "id": document_id,
        "filename": file_path.name,
        "content": file_path.read_text(encoding="utf-8")
    }
