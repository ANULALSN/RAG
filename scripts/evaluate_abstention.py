from qdrant_client import QdrantClient

from app.evaluation.dataset import EVALUATION_DATASET
from app.retrieval.embeddings import embed_text


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70


def evaluate_question(client, item):

    question = item["question"]

    query_vector = embed_text(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    best_score = results[0].score if results else 0.0

    abstained = best_score < RELEVANCE_THRESHOLD

    correct = abstained

    print("\n" + "-" * 70)
    print(f"{item['id']}: {question}")
    print(f"Best retrieval score: {best_score:.4f}")
    print(f"Threshold: {RELEVANCE_THRESHOLD:.2f}")

    print(
        f"Abstained: "
        f"{'YES' if abstained else 'NO'}"
    )

    print(
        f"Expected abstention: YES"
    )

    print(
        f"Result: "
        f"{'CORRECT' if correct else 'INCORRECT'}"
    )

    return correct


def main():

    print("=" * 70)
    print("MSc RAG — ABSTENTION EVALUATION")
    print("=" * 70)

    client = QdrantClient(path=QDRANT_PATH)

    total = 0
    correct = 0

    for item in EVALUATION_DATASET:

        if item["type"] != "out_of_domain":
            continue

        result = evaluate_question(client, item)

        total += 1
        correct += int(result)

    client.close()

    accuracy = (
        correct / total
        if total
        else 0.0
    )

    print("\n" + "=" * 70)
    print("FINAL ABSTENTION RESULTS")
    print("=" * 70)

    print(
        f"Correct abstentions : "
        f"{correct}/{total}"
    )

    print(
        f"Abstention accuracy : "
        f"{accuracy:.2%}"
    )


if __name__ == "__main__":
    main()