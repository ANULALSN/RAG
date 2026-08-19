from pathlib import Path

from app.ingestion.pptx_loader import extract_pptx
from app.ingestion.chunker import chunk_slide


PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)


def main():
    slides = extract_pptx(PPTX_PATH)

    all_chunks = []

    for slide in slides:
        chunks = chunk_slide(slide)
        all_chunks.extend(chunks)

    print("=" * 70)
    print("CHUNKING TEST")
    print("=" * 70)

    print(f"Slides: {len(slides)}")
    non_empty_slides = sum(
    bool(s.get("title") or s.get("text"))
    for s in slides
    )

    print(f"Non-empty slides: {non_empty_slides}")
    print(f"Generated chunks: {len(all_chunks)}")

    print("\nFirst 10 chunks:\n")

    for chunk in all_chunks[:10]:
        print("-" * 70)
        print(
            f"Slide: {chunk['slide']} | "
            f"Chunk: {chunk['chunk_index']}"
        )
        print(f"Words: {len(chunk['text'].split())}")

        if chunk["title"]:
            print(f"Title: {chunk['title']}")

        print(f"Text: {chunk['text'][:500]}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()