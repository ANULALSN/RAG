from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    RecentChatResponse,
    SubjectDashboardResponse,
    SubjectResponse,
)
from app.db.chat_repository import get_chats_by_subject
from app.db.database import SessionLocal


router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


# --------------------------------------------------
# Canonical backend subjects
# --------------------------------------------------

SUBJECTS = [
    {
        "id": "big-data",
        "name": "Big Data",
        "short_name": "BD",
    },
    {
        "id": "dbms",
        "name": "DBMS",
        "short_name": "DB",
    },
    {
        "id": "computer-networks",
        "name": "Computer Networks",
        "short_name": "CN",
    },
    {
        "id": "operating-systems",
        "name": "Operating Systems",
        "short_name": "OS",
    },
]


def get_subject(subject_id: str) -> dict | None:

    for subject in SUBJECTS:
        if subject["id"] == subject_id:
            return subject

    return None


# --------------------------------------------------
# GET /subjects
# --------------------------------------------------

@router.get(
    "",
    response_model=list[SubjectResponse],
)
def list_subjects():

    return SUBJECTS


# --------------------------------------------------
# GET /subjects/{subject_id}
# --------------------------------------------------

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def get_subject_endpoint(
    subject_id: str,
):

    subject = get_subject(subject_id)

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    return subject


# --------------------------------------------------
# GET /subjects/{subject_id}/dashboard
# --------------------------------------------------

@router.get(
    "/{subject_id}/dashboard",
    response_model=SubjectDashboardResponse,
)
def get_subject_dashboard(
    subject_id: str,
):

    subject = get_subject(subject_id)

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    db = SessionLocal()

    try:

        chats = get_chats_by_subject(
            db=db,
            subject_id=subject_id,
        )

        recent_chat = None

        if chats:

            chat = chats[0]

            recent_chat = RecentChatResponse(
                id=chat.id,
                title=chat.title,
                updated_at=chat.updated_at,
            )

    finally:
        db.close()

    return SubjectDashboardResponse(
        subject=subject,
        stats={
            # Material metadata is not yet exposed through
            # a dedicated backend repository.
            "materials": None,

            # Question-bank functionality is not implemented yet.
            "questions": 0,

            # Quiz functionality is not implemented yet.
            "quiz_score": None,

            # Progress/weak-topic tracking is not implemented yet.
            "weak_topics": 0,
        },
        recent_chat=recent_chat,
        frequently_asked=[],
    )