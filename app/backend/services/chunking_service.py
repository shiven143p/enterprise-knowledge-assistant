
import re

from app.backend.services.document_service import (
    list_documents,
    get_document
)


def split_into_chunks(document):
    """
    Split a structured policy document into
    smaller sections suitable for retrieval.
    """

    content = document["content"]

    # Match numbered section headings.
    pattern = r"(?m)^(?=\d+\.\s+[A-Z])"

    sections = re.split(pattern, content)

    chunks = []

    for index, section in enumerate(sections):

        text = section.strip()

        if not text:
            continue

        chunks.append({
            "chunk_id": f"{document['id']}_{index}",
            "document_id": document["id"],
            "filename": document["filename"],
            "text": text
        })

    return chunks


def get_all_chunks():
    """Load and chunk all enterprise documents."""

    all_chunks = []

    for document_info in list_documents():

        document = get_document(
            document_info["id"]
        )

        if document:
            chunks = split_into_chunks(document)
            all_chunks.extend(chunks)

    return all_chunks
