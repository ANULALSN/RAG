from qdrant_client import QdrantClient

from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context
from app.generation.llm import generate_answer


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 3


def main():

    query = "What is the CAP theorem in distributed databases?"

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

    context, sources = build_context(relevant_results)

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
5. When a statement is supported by a source, cite the
   corresponding source number shown in the context,
   such as [1] or [2].
6. If the sources do not contain enough information to answer
   the question, say exactly:

"I don't have enough information in the provided course material."

7. Keep the answer concise and academically clear.
8. Answer in 1–3 concise sentences.
9. Do not repeat the same idea.
10. Do not add unnecessary examples or explanations.

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
    print("SOURCES")
    print("=" * 70)

    for source in sources:
        print(
            f"[{source['id']}] "
            f"{source['document']} "
            f"— Slide {source['slide']}"
        )



if __name__ == "__main__":
    main()