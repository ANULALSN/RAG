from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.material_repository import (
    create_material,
    delete_material,
    get_material,
    list_materials,
    update_material_status,
)
from app.ingestion.material_ingestion import ingest_pptx


router = APIRouter(
    tags=["Materials"]
)


# --------------------------------------------------
# Temporary upload directory
# --------------------------------------------------

UPLOAD_DIR = Path("data/uploads")

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
# POST /subjects/{subject_id}/materials
# --------------------------------------------------

@router.post(
    "/subjects/{subject_id}/materials",
    status_code=201,
)
def upload_material(
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

    if not filename.lower().endswith(".pptx"):

        raise HTTPException(
            status_code=400,
            detail="Only PPTX files are currently supported.",
        )

    # ----------------------------------------------
    # 3. Generate material ID
    # ----------------------------------------------

    material_id = str(uuid4())

    # ----------------------------------------------
    # 4. Save metadata
    # ----------------------------------------------

    material = create_material(
        db,
        subject_id=subject_id,
        filename=filename,
        display_name=Path(filename).stem,
        file_type="pptx",
    )

    # ----------------------------------------------
    # 5. Save uploaded file temporarily
    # ----------------------------------------------

    temp_path = (
        UPLOAD_DIR
        / f"{material_id}_{filename}"
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
        # 6. Run ingestion
        # ------------------------------------------

        chunk_count = ingest_pptx(
            file_path=temp_path,
            subject_id=subject_id,
            material_id=material.id,
        )

        # ------------------------------------------
        # 7. Mark indexed
        # ------------------------------------------

        material = update_material_status(
            db,
            material,
            status="indexed",
            chunk_count=chunk_count,
        )

    except Exception as exc:

        # ------------------------------------------
        # 8. Mark failed
        # ------------------------------------------

        update_material_status(
            db,
            material,
            status="failed",
        )

        raise HTTPException(
            status_code=500,
            detail=f"Material ingestion failed: {str(exc)}",
        )

    finally:

        # ------------------------------------------
        # 9. Remove temporary file
        # ------------------------------------------

        if temp_path.exists():
            temp_path.unlink()

    return material


# --------------------------------------------------
# GET /subjects/{subject_id}/materials
# --------------------------------------------------

@router.get(
    "/subjects/{subject_id}/materials",
)
def get_subject_materials(
    subject_id: str,
    db: Session = Depends(get_db),
):

    if subject_id not in VALID_SUBJECTS:

        raise HTTPException(
            status_code=404,
            detail="Subject not found.",
        )

    return list_materials(
        db,
        subject_id,
    )


# --------------------------------------------------
# GET /materials/{material_id}
# --------------------------------------------------

@router.get(
    "/materials/{material_id}",
)
def get_material_by_id(
    material_id: str,
    db: Session = Depends(get_db),
):

    material = get_material(
        db,
        material_id,
    )

    if material is None:

        raise HTTPException(
            status_code=404,
            detail="Material not found.",
        )

    return material


# --------------------------------------------------
# DELETE /materials/{material_id}
# --------------------------------------------------

@router.delete(
    "/materials/{material_id}",
)
def remove_material(
    material_id: str,
    db: Session = Depends(get_db),
):

    material = get_material(
        db,
        material_id,
    )

    if material is None:

        raise HTTPException(
            status_code=404,
            detail="Material not found.",
        )

    delete_material(
        db,
        material,
    )

    return {
        "deleted": True,
        "material_id": material_id,
    }