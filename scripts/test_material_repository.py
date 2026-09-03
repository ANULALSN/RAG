from app.db.database import SessionLocal
from app.db.material_repository import (
    create_material,
    get_material,
    list_materials,
    update_material_status,
    delete_material,
)


def main():

    print("=" * 70)
    print("MATERIAL REPOSITORY TEST")
    print("=" * 70)

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # 1. Create
        # --------------------------------------------------

        material = create_material(
            db,
            subject_id="big-data",
            filename="Module 1_BD.pptx",
            display_name="Module 1_BD",
            file_type="pptx",
        )

        print("\nCreated material:")
        print(f"ID: {material.id}")
        print(f"Subject: {material.subject_id}")
        print(f"Filename: {material.filename}")
        print(f"Status: {material.status}")

        # --------------------------------------------------
        # 2. Get
        # --------------------------------------------------

        retrieved = get_material(
            db,
            material.id,
        )

        print("\nRetrieved material:")
        print(f"ID: {retrieved.id}")
        print(f"Status: {retrieved.status}")

        # --------------------------------------------------
        # 3. Update
        # --------------------------------------------------

        updated = update_material_status(
            db,
            retrieved,
            status="indexed",
            chunk_count=83,
        )

        print("\nUpdated material:")
        print(f"Status: {updated.status}")
        print(f"Chunks: {updated.chunk_count}")

        # --------------------------------------------------
        # 4. List
        # --------------------------------------------------

        materials = list_materials(
            db,
            "big-data",
        )

        print(
            f"\nMaterials for big-data: "
            f"{len(materials)}"
        )

        # --------------------------------------------------
        # 5. Delete
        # --------------------------------------------------

        delete_material(
            db,
            updated,
        )

        deleted = get_material(
            db,
            updated.id,
        )

        print(
            f"Deleted: {deleted is None}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()