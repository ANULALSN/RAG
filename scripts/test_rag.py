from qdrant_client import QdrantClient

from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context
from app.generation.llm import generate_answer


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 3


def main():

    query = "What is Volume in Big Data?"

    print("=" * 70)
    print("REAL RAG TEST")
    print("=" * 70)

    print(f"\nQuestion: {query}")

    # --------------------------------------------------
    # 1. Embed the user's question
    # --------------------------------------------------

    query_vector = embed_text(query)

    # --------------------------------------------------
    # 2. Retrieve relevant chunks
    # --------------------------------------------------

    client = QdrantClient(path=QDRANT_PATH)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    best_score = results[0].score if results else 0.0

    print(f"\nBest retrieval score: {best_score:.4f}")

    # --------------------------------------------------
    # 3. Relevance gate
    # --------------------------------------------------

    if best_score < RELEVANCE_THRESHOLD:
        print("\n" + "=" * 70)
        print("ABSTAINING")
        print("=" * 70)

        print(
            "I don't have enough information "
            "in the provided course material."
        )

        client.close()
        return

    # --------------------------------------------------
    # 4. Filter and limit context
    # --------------------------------------------------

    relevant_results = [
        result
        for result in results
        if result.score >= RELEVANCE_THRESHOLD
    ][:MAX_CONTEXT_RESULTS]

    print(f"Retrieved: {len(results)} chunks")
    print(
        f"Using {len(relevant_results)} "
        f"relevant chunks for generation."
    )

    print("\nRetrieval scores:")

    for rank, result in enumerate(results, start=1):

        payload = result.payload

        print(
            f"{rank}. "
            f"{result.score:.4f} "
            f"→ Slide {payload.get('slide')} "
            f"→ {payload.get('title', '')}"
        )

    client.close()

    # --------------------------------------------------
    # 5. Build context from filtered results
    # --------------------------------------------------

    context = build_context(relevant_results)

    # --------------------------------------------------
    # 6. Build grounded prompt
    # --------------------------------------------------

    prompt = f"""
You are an academic assistant for an MSc Computer Science student.

IMPORTANT RULES:

1. Answer ONLY using the supplied course material.
2. Do NOT use your pretrained knowledge.
3. Do NOT invent facts.
4. Do NOT infer information that is not explicitly supported
   by the sources.
5. If the sources do not contain enough information to answer
   the question, say exactly:

"I don't have enough information in the provided course material."

6. Keep the answer concise and academically clear.

QUESTION:
{query}

COURSE MATERIAL:
{context}

ANSWER:
"""

    # --------------------------------------------------
    # 7. Generate answer
    # --------------------------------------------------

    print("\nGenerating answer...\n")

    answer = generate_answer(prompt)

    print("=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    # --------------------------------------------------
    # 8. Show sources actually used for generation
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("SOURCES USED")
    print("=" * 70)

    for index, result in enumerate(
        relevant_results,
        start=1
    ):

        payload = result.payload

        print(
            f"{index}. "
            f"{payload.get('document')} "
            f"— Slide {payload.get('slide')}"
        )


if __name__ == "__main__":
    main()