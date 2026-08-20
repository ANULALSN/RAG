from qdrant_client import QdrantClient

from app.evaluation.generation_dataset import GENERATION_DATASET
from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context
from app.generation.llm import generate_answer
from app.generation.context_selector import select_context


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 2


ABSTENTION_MESSAGE = (
    "I don't have enough information in the provided course material."
)


def evaluate_query(client, item):

    query = item["question"]

    print("\n" + "=" * 70)
    print(f"{item['id']}: {query}")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Embed query
    # --------------------------------------------------

    query_vector = embed_text(query)

    # --------------------------------------------------
    # 2. Retrieve
    # --------------------------------------------------

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    best_score = results[0].score if results else 0.0

    print(f"Best retrieval score: {best_score:.4f}")

    # --------------------------------------------------
    # 3. Relevance gate
    # --------------------------------------------------

    if best_score < RELEVANCE_THRESHOLD:

        print("\nABSTAINING")
        print(ABSTENTION_MESSAGE)

        expected_abstention = (
            item["type"] == "unanswerable"
        )

        print(
            f"Expected abstention: "
            f"{'YES' if expected_abstention else 'NO'}"
        )

        print(
            f"Abstention result: "
            f"{'CORRECT' if expected_abstention else 'INCORRECT'}"
        )

        return {
            "generated": False,
            "abstained": True,
            "correct_abstention": expected_abstention,
        }

    # --------------------------------------------------
    # 4. Filter context
    # --------------------------------------------------

    relevant_results = [
    result
    for result in results
    if result.score >= RELEVANCE_THRESHOLD
]

    relevant_results = select_context(
        relevant_results,
        max_results=MAX_CONTEXT_RESULTS,
    )

    print(
        f"Retrieved: {len(results)} chunks"
    )

    print(
        f"Using {len(relevant_results)} "
        f"relevant chunks for generation."
    )

    # --------------------------------------------------
    # 5. Build context
    # --------------------------------------------------

    context, sources = build_context(
        relevant_results
    )

    # --------------------------------------------------
    # 6. Grounded prompt
    # --------------------------------------------------

    prompt = f"""
You are an academic assistant answering questions from a course.

Use ONLY the information in the course material.

STRICT RULES:
1. Answer ONLY the question asked.
2. Use only facts explicitly stated in the course material.
3. Do not use outside knowledge.
4. Do not add information from related topics unless it directly answers the question.
5. Do not repeat information.
6. Give the shortest complete answer possible.
7. Answer in at most 2 sentences.
8. If the course material does not contain enough information, reply exactly:
I don't have enough information in the provided course material.

QUESTION:
{query}

COURSE MATERIAL:
{context}

ANSWER:
"""

    # --------------------------------------------------
    # 7. Generate
    # --------------------------------------------------

    print("\nGenerating answer...\n")

    answer = generate_answer(prompt)

    print("=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    # --------------------------------------------------
    # 8. Sources
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

    return {
        "generated": True,
        "abstained": False,
        "correct_abstention": False,
    }


def main():

    print("=" * 70)
    print("MSc RAG — GENERATION EVALUATION")
    print("=" * 70)

    client = QdrantClient(
        path=QDRANT_PATH
    )

    for item in GENERATION_DATASET:

        evaluate_query(
            client,
            item
        )

    client.close()


if __name__ == "__main__":
    main()