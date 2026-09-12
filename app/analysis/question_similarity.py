import math

from app.retrieval.embeddings import embed_text


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculate cosine similarity between two vectors."""

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding dimensions do not match.")

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def question_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Calculate semantic similarity between two questions
    using the existing local embedding model.
    """

    embedding_a = embed_text(text_a)
    embedding_b = embed_text(text_b)

    return cosine_similarity(
        embedding_a,
        embedding_b,
    )


def classify_similarity(score: float) -> str:
    """
    Classify semantic similarity.
    Thresholds will be validated against real exam questions.
    """

    if score >= 0.80:
        return "repeated"

    if score >= 0.65:
        return "related"

    return "unrelated"