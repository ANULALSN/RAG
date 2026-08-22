from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the course material.",
    )


class Source(BaseModel):
    id: int
    document: str
    slide: int | str
    subject: str | None = None
    module: str | None = None
    title: str | None = None


class QuestionResponse(BaseModel):
    question: str
    answer: str
    abstained: bool
    best_score: float
    sources: list[Source]