from fastapi import (FastAPI,HTTPException)

from app.api.schemas import (
    QuestionRequest,
    QuestionResponse,
)
from app.orchestration.rag_pipeline import (
    RAGPipeline,
)


app = FastAPI(
    title="MSc RAG API",
    description=(
        "Course-grounded Retrieval-Augmented Generation API "
        "for MSc Computer Science course material."
    ),
    version="1.0.0",
)


rag = RAGPipeline()


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
):

    try:
        result = rag.ask(
            request.question
        )

        return QuestionResponse(
            question=request.question,
            answer=result["answer"],
            abstained=result["abstained"],
            best_score=result["best_score"],
            sources=result["sources"],
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline error: {str(exc)}",
        )