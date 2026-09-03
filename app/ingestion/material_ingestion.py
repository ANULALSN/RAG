from pathlib import Path
from uuid import uuid4

from qdrant_client.models import PointStruct

from app.ingestion.pptx_loader import extract_pptx
from app.ingestion.chunker import chunk_slide
from app.retrieval.embeddings import embed_text
from app.retrieval.qdrant_store import get_qdrant_client


COLLECTION_NAME = "msc_knowledge"


def ingest_pptx(
    file_path: str | Path,
    subject_id: str,
    material_id: str,
) -> int:
    """
    Extract, chunk, embed, and store a PPTX in Qdrant.

    Returns the number of inserted chunks.
    """

    file_path = Path(file_path)

    # --------------------------------------------------
    # 1. Validate file
    # --------------------------------------------------

    if not file_path.exists():
        raise FileNotFoundError(
            f"Material not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pptx":
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}"
        )

    # --------------------------------------------------
    # 2. Extract slides
    # --------------------------------------------------

    slides = extract_pptx(
        file_path
    )

    # --------------------------------------------------
    # 3. Create chunks
    # --------------------------------------------------

    chunks = []

    for slide in slides:

        slide_chunks = chunk_slide(
            slide
        )

        for chunk in slide_chunks:

            chunk["subject_id"] = subject_id
            chunk["material_id"] = material_id
            chunk["document"] = file_path.name

            chunks.append(
                chunk
            )

    if not chunks:
        raise ValueError(
            "No usable content was extracted from the PPTX."
        )

    # --------------------------------------------------
    # 4. Get shared Qdrant client
    # --------------------------------------------------

    client = get_qdrant_client()

    # --------------------------------------------------
    # 5. Embed chunks
    # --------------------------------------------------

    points = []

    for chunk in chunks:

        vector = embed_text(
            chunk["text"]
        )

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload=chunk,
            )
        )

    # --------------------------------------------------
    # 6. Store vectors
    # --------------------------------------------------

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    # --------------------------------------------------
    # 7. Return inserted chunk count
    # --------------------------------------------------

    return len(points)