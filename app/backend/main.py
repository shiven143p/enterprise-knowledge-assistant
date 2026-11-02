from fastapi import FastAPI
from fastapi import HTTPException

from app.backend.services.document_service import (
    list_documents,
    get_document
)

# Create FastAPI application
app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="API-driven AI application for enterprise knowledge management",
    version="1.0.0"
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Enterprise Knowledge Assistant API"
    }


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Enterprise Knowledge Assistant",
        "version": "1.0.0"
    }


@app.get("/api/documents")
def get_all_documents():
    documents = list_documents()

    return {
        "total": len(documents),
        "documents": documents
    }


@app.get("/api/documents/{document_id}")
def get_document_by_id(document_id: str):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document
