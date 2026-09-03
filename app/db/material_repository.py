from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Material


def create_material(
    db: Session,
    *,
    subject_id: str,
    filename: str,
    display_name: str,
    file_type: str,
) -> Material:
    material = Material(
        subject_id=subject_id,
        filename=filename,
        display_name=display_name,
        file_type=file_type,
        status="processing",
        chunk_count=0,
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return material


def get_material(
    db: Session,
    material_id: str,
) -> Material | None:

    return db.get(
        Material,
        material_id,
    )


def list_materials(
    db: Session,
    subject_id: str,
) -> list[Material]:

    statement = (
        select(Material)
        .where(
            Material.subject_id == subject_id
        )
        .order_by(
            Material.created_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def update_material_status(
    db: Session,
    material: Material,
    *,
    status: str,
    chunk_count: int | None = None,
) -> Material:

    material.status = status

    if chunk_count is not None:
        material.chunk_count = chunk_count

    db.commit()
    db.refresh(material)

    return material


def delete_material(
    db: Session,
    material: Material,
) -> None:

    db.delete(material)
    db.commit()