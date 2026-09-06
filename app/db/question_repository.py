from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Question, QuestionPaper




def create_question(
    db: Session,
    *,
    question_paper_id: str,
    question_number: int,
    section: str,
    text: str,
    page: int,
    weightage: int | None = None,
) -> Question:

    question = Question(
        question_paper_id=question_paper_id,
        question_number=question_number,
        section=section,
        text=text,
        page=page,
        weightage=weightage,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def create_questions(
    db: Session,
    *,
    question_paper_id: str,
    questions: list[dict],
) -> list[Question]:

    question_records = []

    for question_data in questions:
        question = Question(
            question_paper_id=question_paper_id,
            question_number=question_data["question_number"],
            section=question_data["section"],
            text=question_data["text"],
            page=question_data["page"],
            weightage=question_data.get("weightage"),
        )

        question_records.append(question)

    db.add_all(question_records)
    db.commit()

    for question in question_records:
        db.refresh(question)

    return question_records


def get_question(
    db: Session,
    question_id: str,
) -> Question | None:

    return db.get(Question, question_id)


def list_questions(
    db: Session,
    question_paper_id: str,
) -> list[Question]:

    statement = (
        select(Question)
        .where(
            Question.question_paper_id
            == question_paper_id
        )
        .order_by(
            Question.question_number.asc()
        )
    )

    return list(db.scalars(statement).all())

def list_questions_by_subject(
    db: Session,
    subject_id: str,
    section: str | None = None,
    exam_session: str | None = None,
    search: str | None = None,
) -> list[Question]:
    statement = (
        select(Question)
        .join(
            QuestionPaper,
            Question.question_paper_id
            == QuestionPaper.id,
        )
        .where(
            QuestionPaper.subject_id == subject_id
        )
    )

    if section is not None:
        statement = statement.where(
            Question.section == section
        )

    if exam_session is not None:
        statement = statement.where(
            QuestionPaper.exam_session
            == exam_session
        )

    if search is not None:
        statement = statement.where(
            Question.text.ilike(
                f"%{search}%"
            )
        )

    statement = statement.order_by(
        Question.question_number.asc()
    )

    return list(
        db.scalars(statement).all()
    )


def delete_questions(
    db: Session,
    question_paper_id: str,
) -> None:

    questions = list_questions(
        db,
        question_paper_id,
    )

    for question in questions:
        db.delete(question)

    db.commit()