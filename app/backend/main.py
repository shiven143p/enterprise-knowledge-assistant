from fastapi import FastAPI
from fastapi import HTTPException

from app.backend.services.document_service import (
    list_documents,
    get_document
)

from pydantic import BaseModel, Field

from app.backend.services.classifier_service import (
    classify_query
)

from app.backend.services.vector_service import (
    search_documents
)

from app.backend.services.rag_service import (
    answer_question
)

from app.backend.services.summarizer_service import (
    summarize_document
)
from typing import Literal

from app.backend.services.draft_service import (
    generate_workplace_draft
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


class ClassificationRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=2000
    )


@app.post("/api/classify")
def classify_employee_query(
    request: ClassificationRequest
):
    return classify_query(request.query)



class SearchRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=2000
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10
    )


@app.post("/api/search")
def semantic_search(request: SearchRequest):

    matches = search_documents(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "total_matches": len(matches),
        "matches": matches
    }


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=2000
    )

    top_k: int = Field(
        default=4,
        ge=1,
        le=10
    )


@app.post("/api/chat")
def chat_with_knowledge_base(
    request: ChatRequest
):
    try:
        return answer_question(
            query=request.query,
            top_k=request.top_k
        )

    except Exception as error:
        # Log the error server-side without exposing
        # credentials or provider details to users.
        import logging

        logging.getLogger(__name__).error(
            "RAG request failed: %s",
            type(error).__name__
        )

        raise HTTPException(
            status_code=503,
            detail="Knowledge assistant temporarily unavailable."
        ) from None


class SummarizationRequest(BaseModel):
    document_id: str = Field(min_length=1)
    summary_type: Literal["brief", "detailed"] = "brief"


@app.post("/api/summarize")
def summarize_enterprise_document(
    request: SummarizationRequest
):
    try:
        return summarize_document(
            document_id=request.document_id,
            summary_type=request.summary_type
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Summarization service unavailable."
        )



class DraftRequest(BaseModel):
    request: str = Field(
        min_length=5,
        max_length=3000
    )

    draft_type: Literal[
        "email",
        "support_ticket",
        "formal_request"
    ] = "email"

    tone: Literal[
        "professional",
        "formal",
        "concise"
    ] = "professional"


@app.post("/api/generate")
def generate_draft(request: DraftRequest):
    try:
        return generate_workplace_draft(
            request_text=request.request,
            draft_type=request.draft_type,
            tone=request.tone
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Draft generation service unavailable."
        )
