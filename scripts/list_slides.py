from pathlib import Path

from app.ingestion.pptx_loader import extract_pptx


PPTX_PATH = Path(
    "data/raw/BigData/Module1/Module 1_BD.pptx"
)

slides = extract_pptx(PPTX_PATH)

print("=" * 70)
print("BIG DATA MODULE — SLIDE INVENTORY")
print("=" * 70)

for slide in slides:
    print(
        f"{slide.get('slide'):>3}: "
        f"{slide.get('title', '[No title]')}"
    )