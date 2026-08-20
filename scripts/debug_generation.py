from qdrant_client import QdrantClient
from app.generation.llm import generate_answer

from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 3


def main():

    query = "What is structured data?"

    print("=" * 70)
    print("GENERATION DEBUG")
    print("=" * 70)

    query_vector = embed_text(query)

    client = QdrantClient(
        path=QDRANT_PATH
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    best_score = results[0].score if results else 0.0

    print(f"Best score: {best_score:.4f}")

    relevant_results = [
        result
        for result in results
        if result.score >= RELEVANCE_THRESHOLD
    ][:MAX_CONTEXT_RESULTS]

    print(
        f"Relevant chunks: "
        f"{len(relevant_results)}"
    )

    context, sources = build_context(
        relevant_results
    )

    print(
        f"\nContext characters: "
        f"{len(context)}"
    )

    print(
        f"Context words: "
        f"{len(context.split())}"
    )

    print("\n" + "-" * 70)
    print("SOURCES")
    print("-" * 70)

    for source in sources:
        print(
            f"[{source['id']}] "
            f"{source['document']} "
            f"— Slide {source['slide']}"
        )

    print("\n" + "-" * 70)
    print("CONTEXT")
    print("-" * 70)

    print(context)

    print("\n" + "-" * 70)
    print("TESTING GENERATION")
    print("-" * 70)

    prompt = f"""
You are answering an MSc Computer Science question using ONLY the course material below.

Rules:
- Use only information explicitly present in the course material.
- Do not add outside knowledge.
- Do not invent or infer facts.
- Cite supporting sources as [1], [2], etc.
- Answer in 1-3 concise sentences.
- If the course material does not contain enough information, answer exactly:
"I don't have enough information in the provided course material."

Question:
{query}

Course material:
{context}

Answer:
"""

    print(f"Prompt characters: {len(prompt)}")
    print(f"Prompt words: {len(prompt.split())}")

    answer = generate_answer(prompt)

    print("\nANSWER:")
    print(answer)

    client.close()


if __name__ == "__main__":
    main()