
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.backend.services.chunking_service import (
    get_all_chunks
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_DB_DIR = PROJECT_ROOT / "data" / "vector_db"

COLLECTION_NAME = "enterprise_knowledge"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# Initialize embedding model
embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# Initialize persistent ChromaDB
chroma_client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


def build_vector_database():
    """
    Convert document chunks into embeddings
    and store them in ChromaDB.
    """

    chunks = get_all_chunks()

    if not chunks:
        raise ValueError(
            "No document chunks available for indexing."
        )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "document_id": chunk["document_id"],
            "filename": chunk["filename"]
        }
        for chunk in chunks
    ]

    # Generate embeddings
    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    # Upsert allows rebuilding without
    # duplicating existing chunk IDs.
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return {
        "indexed_chunks": len(chunks),
        "collection_count": collection.count()
    }


def search_documents(query: str, top_k: int = 3):
    """
    Retrieve semantically relevant passages
    from the enterprise knowledge base.
    """

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if collection.count() == 0:
        return []

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        matches.append({
            "document": document,
            "filename": metadata["filename"],
            "document_id": metadata["document_id"],
            "distance": round(float(distance), 4)
        })

    return matches
