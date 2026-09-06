from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.question_paper_repository import (
    create_question_paper,
    get_question_paper,
    get_question_paper_by_filename,
    list_question_papers,
    update_question_paper_status,
    delete_question_paper,
)
from app.db.question_repository import (
    create_questions,
    list_questions,
    list_questions_by_subject,
)
from app.ingestion.pdf_loader import extract_pdf
from app.ingestion.question_parser import parse_questions

from app.ingestion.question_paper_metadata import (
    extract_question_paper_metadata,
)


router = APIRouter(
    tags=["Question Papers"]
)


# --------------------------------------------------
# Temporary upload directory
# --------------------------------------------------

UPLOAD_DIR = Path("data/uploads/question_papers")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# Subject validation
# --------------------------------------------------

VALID_SUBJECTS = {
    "big-data",
    "dbms",
    "computer-networks",
    "operating-systems",
}


# --------------------------------------------------
# POST /subjects/{subject_id}/question-papers
# --------------------------------------------------

@router.post(
    "/subjects/{subject_id}/question-papers",
    status_code=201,
)
def upload_question_paper(
    subject_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    # ----------------------------------------------
    # 1. Validate subject
    # ----------------------------------------------

    if subject_id not in VALID_SUBJECTS:

        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    # ----------------------------------------------
    # 2. Validate file type
    # ----------------------------------------------

    filename = file.filename or ""

    if not filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are currently supported.",
        )

    # ----------------------------------------------
    # 3. Prevent duplicate paper
    # ----------------------------------------------

    existing_paper = get_question_paper_by_filename(
        db,
        subject_id,
        filename,
    )

    if existing_paper is not None:

        raise HTTPException(
            status_code=409,
            detail="A question paper with this filename already exists for this subject.",
        )

    # ----------------------------------------------
    # 4. Create metadata
    # ----------------------------------------------

    paper = create_question_paper(
        db,
        subject_id=subject_id,
        filename=filename,
        display_name=Path(filename).stem,
        file_type="pdf",
    )

    # ----------------------------------------------
    # 5. Save temporary PDF
    # ----------------------------------------------

    temp_path = (
        UPLOAD_DIR
        / f"{paper.id}_{filename}"
    )

    try:

        with temp_path.open("wb") as destination:

            while True:

                chunk = file.file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                destination.write(chunk)

        # ------------------------------------------
        # 6. Extract PDF
        # ------------------------------------------

        pages = extract_pdf(temp_path)

        # ------------------------------------------
        # 7. Parse questions
        # ------------------------------------------
          
        metadata = extract_question_paper_metadata(pages)  
        
        questions = parse_questions(pages)

        # ------------------------------------------
        # 8. Store questions
        # ------------------------------------------

        create_questions(
            db,
            question_paper_id=paper.id,
            questions=questions,
        )
        
        
        paper.exam_session = metadata["exam_session"]
        paper.course_code = metadata["course_code"]
        paper.exam_title = metadata["exam_title"]

        db.commit()
        db.refresh(paper)

        # ------------------------------------------
        # 9. Mark paper as indexed
        # ------------------------------------------

        paper = update_question_paper_status(
            db,
            paper,
            status="indexed",
            page_count=len(pages),
            question_count=len(questions),
        )

    except Exception as exc:

        # ------------------------------------------
        # 10. Mark failed
        # ------------------------------------------

        update_question_paper_status(
            db,
            paper,
            status="failed",
        )

        raise HTTPException(
            status_code=500,
            detail=f"Question paper processing failed: {str(exc)}",
        )

    finally:

        # ------------------------------------------
        # 11. Remove temporary file
        # ------------------------------------------

        if temp_path.exists():
            temp_path.unlink()

    return paper


# --------------------------------------------------
# GET /subjects/{subject_id}/question-papers
# --------------------------------------------------

@router.get(
    "/subjects/{subject_id}/question-papers",
)
def get_subject_question_papers(
    subject_id: str,
    db: Session = Depends(get_db),
):

    if subject_id not in VALID_SUBJECTS:

        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    return list_question_papers(
        db,
        subject_id,
    )

# --------------------------------------------------
# GET /subjects/{subject_id}/questions
# --------------------------------------------------

# --------------------------------------------------
# GET /subjects/{subject_id}/questions
# --------------------------------------------------

# --------------------------------------------------
# GET /subjects/{subject_id}/questions
# --------------------------------------------------

@router.get(
    "/subjects/{subject_id}/questions",
)
def get_subject_questions(
    subject_id: str,
    section: str | None = Query(
        default=None,
        pattern="^[ABCabc]$",
    ),
    exam_session: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
    ),
    db: Session = Depends(get_db),
):
    if subject_id not in VALID_SUBJECTS:
        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    return list_questions_by_subject(
        db,
        subject_id,
        section=section.upper()
        if section
        else None,
        exam_session=(
            exam_session.upper()
            if exam_session
            else None
        ),
        search=search,
    )

    
# --------------------------------------------------
# GET /question-papers/{question_paper_id}
# --------------------------------------------------

@router.get(
    "/question-papers/{question_paper_id}",
)
def get_question_paper_by_id(
    question_paper_id: str,
    db: Session = Depends(get_db),
):

    paper = get_question_paper(
        db,
        question_paper_id,
    )

    if paper is None:

        raise HTTPException(
            status_code=404,
            detail="Question paper not found.",
        )

    return paper

# --------------------------------------------------
# GET /question-papers/{question_paper_id}/questions
# --------------------------------------------------

@router.get(
    "/question-papers/{question_paper_id}/questions",
)
def get_question_paper_questions(
    question_paper_id: str,
    db: Session = Depends(get_db),
):

    paper = get_question_paper(
        db,
        question_paper_id,
    )

    if paper is None:

        raise HTTPException(
            status_code=404,
            detail="Question paper not found.",
        )

    return list_questions(
        db,
        question_paper_id,
    )



# --------------------------------------------------
# DELETE /question-papers/{question_paper_id}
# --------------------------------------------------

@router.delete(
    "/question-papers/{question_paper_id}",
)
def remove_question_paper(
    question_paper_id: str,
    db: Session = Depends(get_db),
):

    paper = get_question_paper(
        db,
        question_paper_id,
    )

    if paper is None:

        raise HTTPException(
            status_code=404,
            detail="Question paper not found.",
        )

    delete_question_paper(
        db,
        paper,
    )

    return {
        "deleted": True,
        "question_paper_id": question_paper_id,
    }