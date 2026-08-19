from __future__ import annotations

import re


MAX_WORDS = 300
OVERLAP_WORDS = 40


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""

    paragraphs = []

    for paragraph in text.splitlines():
        paragraph = re.sub(r"\s+", " ", paragraph).strip()

        if paragraph:
            paragraphs.append(paragraph)

    return "\n".join(paragraphs)


def remove_duplicate_title(title: str, text: str) -> str:
    """
    Remove a title if it appears as the first line of the body text.
    """

    if not title or not text:
        return text

    title_normalized = " ".join(title.split()).strip()

    lines = text.splitlines()

    if not lines:
        return text

    first_line = " ".join(lines[0].split()).strip()

    if first_line.casefold() == title_normalized.casefold():
        return "\n".join(lines[1:]).strip()

    return text


def split_large_text(
    text: str,
    max_words: int = MAX_WORDS,
    overlap_words: int = OVERLAP_WORDS,
) -> list[str]:
    """
    Split large slide text while preserving paragraph boundaries
    where possible.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.splitlines()
        if paragraph.strip()
    ]

    chunks = []
    current_words: list[str] = []

    for paragraph in paragraphs:
        paragraph_words = paragraph.split()

        if len(current_words) + len(paragraph_words) <= max_words:
            current_words.extend(paragraph_words)
            continue

        if current_words:
            chunks.append(" ".join(current_words))

        if len(paragraph_words) > max_words:
            start = 0

            while start < len(paragraph_words):
                end = start + max_words
                chunks.append(" ".join(paragraph_words[start:end]))

                start = end - overlap_words

            current_words = []
        else:
            current_words = paragraph_words.copy()

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def chunk_slide(slide: dict) -> list[dict]:
    """
    Convert one normalized slide into one or more RAG chunks.
    """

    slide_number = slide["slide"]

    title = normalize_whitespace(
        slide.get("title", "")
    )

    text = normalize_whitespace(
        slide.get("text", "")
    )

    # Remove title if PowerPoint extraction also placed it
    # at the beginning of the body text.
    text = remove_duplicate_title(title, text)

    # Ignore completely empty slides.
    if not title and not text:
        return []

    # Combine title + body exactly once.
    if title and text:
        combined_text = f"{title}\n{text}"
    elif title:
        combined_text = title
    else:
        combined_text = text

    # Keep normal-sized slides as a single semantic chunk.
    if len(combined_text.split()) <= MAX_WORDS:
        parts = [combined_text]
    else:
        parts = split_large_text(combined_text)

    chunks = []

    for index, part in enumerate(parts, start=1):
        chunks.append(
            {
                "slide": slide_number,
                "chunk_index": index,
                "title": title,
                "text": part,
                "source_type": slide.get(
                    "source_type",
                    "pptx",
                ),
            }
        )

    return chunks