from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import QuestionPaper


def create_question_paper(
    db: Session,
    *,
    subject_id: str,
    filename: str,
    display_name: str,
    file_type: str = "pdf",
) -> QuestionPaper:

    question_paper = QuestionPaper(
        subject_id=subject_id,
        filename=filename,
        display_name=display_name,
        file_type=file_type,
        status="processing",
        page_count=0,
        question_count=0,
    )

    db.add(question_paper)
    db.commit()
    db.refresh(question_paper)

    return question_paper


def get_question_paper(
    db: Session,
    question_paper_id: str,
) -> QuestionPaper | None:

    return db.get(
        QuestionPaper,
        question_paper_id,
    )


def list_question_papers(
    db: Session,
    subject_id: str,
) -> list[QuestionPaper]:

    statement = (
        select(QuestionPaper)
        .where(
            QuestionPaper.subject_id == subject_id
        )
        .order_by(
            QuestionPaper.created_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def get_question_paper_by_filename(
    db: Session,
    subject_id: str,
    filename: str,
) -> QuestionPaper | None:

    statement = (
        select(QuestionPaper)
        .where(
            QuestionPaper.subject_id == subject_id,
            QuestionPaper.filename == filename,
        )
    )

    return db.scalars(statement).first()


def update_question_paper_status(
    db: Session,
    question_paper: QuestionPaper,
    *,
    status: str,
    page_count: int | None = None,
    question_count: int | None = None,
) -> QuestionPaper:

    question_paper.status = status

    if page_count is not None:
        question_paper.page_count = page_count

    if question_count is not None:
        question_paper.question_count = question_count

    db.commit()
    db.refresh(question_paper)

    return question_paper


def delete_question_paper(
    db: Session,
    question_paper: QuestionPaper,
) -> None:

    db.delete(question_paper)
    db.commit()