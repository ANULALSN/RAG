from pathlib import Path

from app.ingestion.pptx_loader import extract_pptx


PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)

slides = extract_pptx(PPTX_PATH)

slide_map = {
    slide["slide"]: slide
    for slide in slides
}

slide_numbers = [
    2, 3, 5, 6, 8, 9,
    13, 14, 15, 16,
    19, 23, 26,
    38, 40, 43,
    57, 59,
    62, 63,
    66, 67, 69, 70,
    71, 73, 76, 79, 80,
]

for number in slide_numbers:

    slide = slide_map.get(number)

    print("\n" + "=" * 70)
    print(f"SLIDE {number}")
    print("=" * 70)

    if not slide:
        print("NOT FOUND")
        continue

    print(f"Title: {slide.get('title', '')}")
    print()
    print(slide.get("text", ""))