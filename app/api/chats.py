import re
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.chat_repository import create_message
from app.api.schemas import ChatMessageCreateRequest

from app.api.schemas import (
    ChatCreateRequest,
    ChatMessageResponse,
    ChatResponse,
)
from app.db.chat_repository import (
    create_chat,
    delete_chat,
    get_chat,
    get_chat_messages,
    get_chats_by_subject,
)
from app.db.database import get_db


router = APIRouter(
    tags=["Chats"],
)

_rag_pipeline = None


def set_rag_pipeline(rag):
    global _rag_pipeline
    _rag_pipeline = rag

# --------------------------------------------------
# Create chat
# --------------------------------------------------

@router.post(
    "/subjects/{subject_id}/chats",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_endpoint(
    subject_id: str,
    request: ChatCreateRequest,
    db: Session = Depends(get_db),
):

    chat = create_chat(
        db=db,
        subject_id=subject_id,
        title=request.title,
    )

    return chat


# --------------------------------------------------
# List chats for subject
# --------------------------------------------------

@router.get(
    "/subjects/{subject_id}/chats",
    response_model=list[ChatResponse],
)
def list_chats_endpoint(
    subject_id: str,
    db: Session = Depends(get_db),
):

    return get_chats_by_subject(
        db=db,
        subject_id=subject_id,
    )


# --------------------------------------------------
# Get chat
# --------------------------------------------------

@router.get(
    "/chats/{chat_id}",
    response_model=ChatResponse,
)
def get_chat_endpoint(
    chat_id: str,
    db: Session = Depends(get_db),
):

    chat = get_chat(
        db=db,
        chat_id=chat_id,
    )

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    return chat


# --------------------------------------------------
# Delete chat
# --------------------------------------------------

@router.delete(
    "/chats/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chat_endpoint(
    chat_id: str,
    db: Session = Depends(get_db),
):

    deleted = delete_chat(
        db=db,
        chat_id=chat_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    return None


# --------------------------------------------------
# Get chat messages
# --------------------------------------------------

@router.get(
    "/chats/{chat_id}/messages",
    response_model=list[ChatMessageResponse],
)
def get_messages_endpoint(
    chat_id: str,
    db: Session = Depends(get_db),
):

    chat = get_chat(
        db=db,
        chat_id=chat_id,
    )

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    messages = get_chat_messages(
        db=db,
        chat_id=chat_id,
    )

    response = []

    for message in messages:

        try:
            sources = (
                json.loads(message.sources)
                if message.sources
                else []
            )

        except json.JSONDecodeError:
            sources = []

        response.append(
            ChatMessageResponse(
                id=message.id,
                chat_id=message.chat_id,
                role=message.role,
                content=message.content,
                created_at=message.created_at,
                abstained=message.abstained,
                best_score=message.best_score,
                relevance_threshold=(
                    message.relevance_threshold
                ),
                retrieved_count=(
                    message.retrieved_count
                ),
                sources=sources,
            )
        )

    return response

@router.post(
    "/chats/{chat_id}/messages",
    response_model=list[ChatMessageResponse],
)
def send_chat_message(
    chat_id: str,
    request: ChatMessageCreateRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------
    # 1. Find chat
    # --------------------------------------------------

    chat = get_chat(
    db=db,
    chat_id=chat_id,
       )

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    question = request.content.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty.",
        )


    # --------------------------------------------------
    # 2. Set title from first user message
    # --------------------------------------------------

        # --------------------------------------------------
    # 2. Set title from first user message
    # --------------------------------------------------

    if chat.title == "New Chat":

        existing_messages = get_chat_messages(
            db=db,
            chat_id=chat.id,
        )

        has_user_message = any(
            message.role == "user"
            for message in existing_messages
        )

        if not has_user_message:

            title = re.sub(
                r"\s+",
                " ",
                question,
            ).strip()

            if len(title) > 42:
                title = (
                    title[:41].rstrip()
                    + "…"
                )

            if title:
                title = (
                    title[0].upper()
                    + title[1:]
                )

            chat.title = title

    # --------------------------------------------------
    # 3. Persist user message
    # --------------------------------------------------

    create_message(
        db=db,
        chat_id=chat.id,
        role="user",
        content=question,
    )

    # --------------------------------------------------
    # 3. Run existing RAG pipeline
    # --------------------------------------------------

    try:

        if _rag_pipeline is None:
            raise HTTPException(
                status_code=500,
                detail="RAG pipeline is not initialized.",
            )

        result = _rag_pipeline.ask(
    question,
    subject_id=chat.subject_id,
)

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline error: {str(exc)}",
        )

    # --------------------------------------------------
    # 4. Serialize sources
    # --------------------------------------------------

    sources_json = json.dumps(
        result.get(
            "sources",
            [],
        )
    )

    # --------------------------------------------------
    # 5. Persist assistant response
    # --------------------------------------------------

    create_message(
        db=db,
        chat_id=chat.id,
        role="assistant",
        content=result["answer"],
        abstained=result["abstained"],
        best_score=result["best_score"],
        relevance_threshold=0.70,
        retrieved_count=None,
        sources=sources_json,
    )

    # --------------------------------------------------
    # 6. Return complete conversation
    # --------------------------------------------------

    messages = get_chat_messages(
        db=db,
        chat_id=chat.id,
    )

    response = []

    for message in messages:

        try:
            sources = (
                json.loads(message.sources)
                if message.sources
                else []
            )

        except json.JSONDecodeError:
            sources = []

        response.append(
            ChatMessageResponse(
                id=message.id,
                chat_id=message.chat_id,
                role=message.role,
                content=message.content,
                created_at=message.created_at,
                abstained=message.abstained,
                best_score=message.best_score,
                relevance_threshold=(
                    message.relevance_threshold
                ),
                retrieved_count=(
                    message.retrieved_count
                ),
                sources=sources,
            )
        )

    return response