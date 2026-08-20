from qdrant_client import QdrantClient

from app.evaluation.dataset import EVALUATION_DATASET
from app.retrieval.embeddings import embed_text


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"


def evaluate_query(client, item):
    """Evaluate retrieval for one question."""

    question = item["question"]
    expected_slides = set(item["expected_slides"])

    query_vector = embed_text(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    retrieved_slides = [
        result.payload.get("slide")
        for result in results
    ]


    # Find the rank of the first relevant result.
    first_relevant_rank = None

    for rank, slide in enumerate(retrieved_slides, start=1):
        if slide in expected_slides:
            first_relevant_rank = rank
            break

    if first_relevant_rank is not None:
        reciprocal_rank = 1 / first_relevant_rank
    else:
        reciprocal_rank = 0.0

    

    print("\n" + "-" * 70)
    print(f"{item['id']}: {question}")
    print(f"Expected slides: {sorted(expected_slides)}")
    print(f"Retrieved slides: {retrieved_slides}")
    print(
            f"First relevant rank: "
            f"{first_relevant_rank if first_relevant_rank else 'NONE'}"
        )
    
    print(
            f"Reciprocal Rank: "
            f"{reciprocal_rank:.4f}"
        )

    metrics = {}

    for k in [1, 3, 5]:

        top_k = retrieved_slides[:k]

        # Did we retrieve at least one relevant slide?
        hit = any(
            slide in expected_slides
            for slide in top_k
        )

        # How many of the expected relevant slides
        # were actually retrieved?
        retrieved_relevant = (
            set(top_k) & expected_slides
        )

        recall = (
            len(retrieved_relevant)
            / len(expected_slides)
            if expected_slides
            else 0.0
        )

        metrics[f"hit@{k}"] = int(hit)
        metrics[f"recall@{k}"] = recall
        

        print(
            f"Hit@{k}: "
            f"{'HIT' if hit else 'MISS'}"
        )

        print(
            f"Recall@{k}: "
            f"{recall:.2%}"
        )
    metrics["mrr"] = reciprocal_rank

    return metrics


def main():

    print("=" * 70)
    print("MSc RAG — RETRIEVAL EVALUATION")
    print("=" * 70)

    client = QdrantClient(path=QDRANT_PATH)

    totals = {
    "hit@1": 0,
    "hit@3": 0,
    "hit@5": 0,
    "recall@1": 0.0,
    "recall@3": 0.0,
    "recall@5": 0.0,
    "mrr": 0.0,
    }

    count = 0

    for item in EVALUATION_DATASET:

        # Out-of-domain questions are evaluated separately.
        if item["type"] != "in_domain":
            continue

        metrics = evaluate_query(client, item)

        for metric, value in metrics.items():
            totals[metric] += value

        count += 1

    client.close()

    print("\n" + "=" * 70)
    print("FINAL RETRIEVAL RESULTS")
    print("=" * 70)

    for metric, value in totals.items():

        score = value / count if count else 0.0

        print(
            f"{metric.upper():<12}: "
            f"{score:.2%}"
        )


if __name__ == "__main__":
    main()