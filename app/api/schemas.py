from pydantic import BaseModel, Field
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatCreateRequest(BaseModel):
    title: str = Field(
        default="New Chat",
        min_length=1,
        max_length=200,
    )


class ChatResponse(BaseModel):
    id: str
    subject_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatMessageResponse(BaseModel):
    id: str
    chat_id: str
    role: str
    content: str
    created_at: datetime

    abstained: bool | None = None
    best_score: float | None = None
    relevance_threshold: float | None = None
    retrieved_count: int | None = None

    sources: list[dict] = []

    model_config = ConfigDict(
        from_attributes=True
    )

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
    subject_id: str | None = None
    material_id: str | None = None
    title: str | None = None

class QuestionResponse(BaseModel):
    question: str
    answer: str
    abstained: bool
    best_score: float
    sources: list[Source]

class ChatMessageCreateRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )
class SubjectResponse(BaseModel):
    id: str
    name: str
    short_name: str


class RecentChatResponse(BaseModel):
    id: str
    title: str
    updated_at: datetime


class SubjectDashboardStats(BaseModel):
    materials: int | None = None
    questions: int = 0
    quiz_score: float | None = None
    weak_topics: int = 0


class SubjectDashboardResponse(BaseModel):
    subject: SubjectResponse
    stats: SubjectDashboardStats
    recent_chat: RecentChatResponse | None = None
    frequently_asked: list = []