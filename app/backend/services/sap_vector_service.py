
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[3]

SAP_DOCS_DIR = PROJECT_ROOT / "data" / "sap_documents"
DB_DIR = PROJECT_ROOT / "data" / "vector_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="sap_support_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def build_sap_index():
    ids = []
    texts = []
    metadata = []

    for file_path in sorted(SAP_DOCS_DIR.glob("*.txt")):
        content = file_path.read_text(encoding="utf-8")

        # Split at numbered section headings.
        import re

        sections = re.split(
            r"(?m)^(?=\d+\.\s+[A-Z])",
            content
        )

        for index, section in enumerate(sections):
            section = section.strip()

            if not section:
                continue

            ids.append(f"{file_path.stem}_{index}")
            texts.append(section)

            metadata.append({
                "filename": file_path.name,
                "document_id": file_path.stem
            })

    if not texts:
        raise ValueError("No SAP documents found.")

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True
    )

    # Rebuild this dedicated synthetic collection.
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

    return len(texts)


def search_sap_documents(query, top_k=4):
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if collection.count() == 0:
        return []

    embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )

    result = collection.query(
        query_embeddings=embedding.tolist(),
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    for text, meta, distance in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0]
    ):
        matches.append({
            "document": text,
            "filename": meta["filename"],
            "document_id": meta["document_id"],
            "distance": float(distance)
        })

    return matches
