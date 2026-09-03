from pathlib import Path

from app.ingestion.material_ingestion import ingest_pptx


MATERIAL_ID = "495bbe09-4118-4825-9660-94ad1fe6f66a"

SUBJECT_ID = "big-data"

PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)


def main():

    print("=" * 70)
    print("REINDEXING MATERIAL")
    print("=" * 70)

    print(f"Subject ID : {SUBJECT_ID}")
    print(f"Material ID: {MATERIAL_ID}")
    print(f"File       : {PPTX_PATH}")

    chunks = ingest_pptx(
        file_path=PPTX_PATH,
        subject_id=SUBJECT_ID,
        material_id=MATERIAL_ID,
    )

    print()
    print("=" * 70)
    print("REINDEX COMPLETE")
    print("=" * 70)
    print(f"Chunks inserted: {chunks}")


if __name__ == "__main__":
    main()