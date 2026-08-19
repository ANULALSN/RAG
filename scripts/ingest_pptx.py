from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.ingestion.pptx_loader import extract_pptx
from app.ingestion.chunker import chunk_slide
from app.retrieval.embeddings import embed_text


PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)

QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"


def build_chunks() -> list[dict]:
    """Extract slides and convert them into RAG chunks."""

    slides = extract_pptx(PPTX_PATH)

    chunks = []

    for slide in slides:
        slide_chunks = chunk_slide(slide)

        for chunk in slide_chunks:
            chunk["subject"] = "BigData"
            chunk["module"] = "Module1"
            chunk["document"] = PPTX_PATH.name

            chunks.append(chunk)

    return chunks


def main():
    print("=" * 70)
    print("MSc RAG — PPTX INGESTION")
    print("=" * 70)

    chunks = build_chunks()

    print(f"Source: {PPTX_PATH}")
    print(f"Chunks: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No chunks were generated.")

    client = QdrantClient(path=QDRANT_PATH)

    points = []

    for index, chunk in enumerate(chunks, start=1):
        print(
            f"[{index}/{len(chunks)}] "
            f"Embedding slide {chunk['slide']}..."
        )

        vector = embed_text(chunk["text"])

        points.append(
            PointStruct(
                id=index,
                vector=vector,
                payload=chunk,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print("\n" + "=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)
    print(f"Inserted vectors: {len(points)}")
    print(f"Collection: {COLLECTION_NAME}")

    client.close()


if __name__ == "__main__":
    main()