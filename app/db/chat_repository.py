from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChatMessage, ChatSession
from datetime import datetime, timezone


def create_chat(
    db: Session,
    subject_id: str,
    title: str = "New Chat",
) -> ChatSession:

    chat = ChatSession(
        subject_id=subject_id,
        title=title,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chats_by_subject(
    db: Session,
    subject_id: str,
) -> list[ChatSession]:

    statement = (
        select(ChatSession)
        .where(
            ChatSession.subject_id == subject_id
        )
        .order_by(
            ChatSession.updated_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def get_chat(
    db: Session,
    chat_id: str,
) -> ChatSession | None:

    return db.get(
        ChatSession,
        chat_id,
    )


def delete_chat(
    db: Session,
    chat_id: str,
) -> bool:

    chat = get_chat(
        db,
        chat_id,
    )

    if chat is None:
        return False

    db.delete(chat)
    db.commit()

    return True


def get_chat_messages(
    db: Session,
    chat_id: str,
) -> list[ChatMessage]:

    statement = (
        select(ChatMessage)
        .where(
            ChatMessage.chat_id == chat_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )

def create_message(
    db: Session,
    chat_id: str,
    role: str,
    content: str,
    abstained: bool | None = None,
    best_score: float | None = None,
    relevance_threshold: float | None = None,
    retrieved_count: int | None = None,
    sources: str | None = None,
) -> ChatMessage:

    message = ChatMessage(
        chat_id=chat_id,
        role=role,
        content=content,
        abstained=abstained,
        best_score=best_score,
        relevance_threshold=relevance_threshold,
        retrieved_count=retrieved_count,
        sources=sources,
    )

    db.add(message)

    # Keep the chat's updated_at current.
    chat = get_chat(
        db,
        chat_id,
    )

    if chat is not None:
        chat.updated_at = datetime.now(
            timezone.utc
        )

    db.commit()
    db.refresh(message)

    return message