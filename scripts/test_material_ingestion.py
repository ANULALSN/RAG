from pathlib import Path
from uuid import uuid4

from app.ingestion.material_ingestion import ingest_pptx


PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)


def main():

    print("=" * 70)
    print("MATERIAL INGESTION TEST")
    print("=" * 70)

    material_id = str(uuid4())

    print(f"Subject ID : big-data")
    print(f"Material ID: {material_id}")
    print(f"File      : {PPTX_PATH}")

    chunk_count = ingest_pptx(
        file_path=PPTX_PATH,
        subject_id="big-data",
        material_id=material_id,
    )

    print("\n" + "=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)

    print(f"Chunks inserted: {chunk_count}")
    print(f"Material ID    : {material_id}")


if __name__ == "__main__":
    main()