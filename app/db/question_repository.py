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
    
def get_question_paper_overview(
    db: Session,
    question_paper_id: str,
) -> dict:
    questions = list_questions(
        db,
        question_paper_id,
    )

    sections = {}

    # Number of questions the student answers
    # in each section for the MSc examination.
    answer_counts = {
        "A": 4,
        "B": 4,
        "C": 2,
    }

    for question in questions:
        section = question.section
        weightage = question.weightage

        if section not in sections:
            sections[section] = {
                "available_questions": 0,
                "answerable_questions": (
                    answer_counts.get(section)
                ),
                "weightage_per_question": weightage,
                "section_weightage": 0,
                "marks_per_weightage": 5,
                "section_marks": 0,
            }

        sections[section]["available_questions"] += 1

    maximum_weightage = 0
    maximum_marks = 0

    for section, data in sections.items():
        weightage = data["weightage_per_question"]
        answerable = data["answerable_questions"]

        if (
            weightage is not None
            and answerable is not None
        ):
            section_weightage = (
                answerable * weightage
            )

            section_marks = (
                section_weightage * 5
            )

            data["section_weightage"] = (
                section_weightage
            )

            data["section_marks"] = (
                section_marks
            )

            maximum_weightage += (
                section_weightage
            )

            maximum_marks += section_marks

    return {
        "question_paper_id": question_paper_id,
        "available_question_count": len(questions),
        "maximum_weightage": maximum_weightage,
        "marks_per_weightage": 5,
        "maximum_marks": maximum_marks,
        "sections": sections,
    }