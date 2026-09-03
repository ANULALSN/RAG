from fastapi import (FastAPI,HTTPException)
from fastapi.middleware.cors import CORSMiddleware

from app.api.chats import (
    router as chats_router,
    set_rag_pipeline,
)

from app.api.schemas import (
    QuestionRequest,
    QuestionResponse,
)
from app.orchestration.rag_pipeline import (
    RAGPipeline,
)
from app.api.subjects import router as subjects_router
from app.api.materials import router as materials_router


app = FastAPI(
    title="MSc RAG API",
    description=(
        "Course-grounded Retrieval-Augmented Generation API "
        "for MSc Computer Science course material."
    ),
    version="1.0.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(subjects_router)
app.include_router(chats_router)
app.include_router(materials_router)


rag = RAGPipeline()

set_rag_pipeline(rag)


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