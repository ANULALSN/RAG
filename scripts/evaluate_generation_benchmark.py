import json
from pathlib import Path


MANUAL_SCORES_PATH = (
    Path("app/evaluation/manual_scores.json")
)


def load_manual_scores():
    """Load manually assigned semantic quality scores."""

    with open(
        MANUAL_SCORES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def average(values):
    """Calculate the average of a list of values."""

    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_dimension_scores(scores):
    """Calculate average score for each quality dimension."""

    dimensions = [
        "correctness",
        "grounding",
        "relevance",
        "conciseness",
        "source_correctness",
        "topic_drift",
    ]

    results = {}

    for dimension in dimensions:

        values = [
            item[dimension]
            for item in scores.values()
        ]

        results[dimension] = average(values)

    return results


def calculate_overall_score(dimension_scores):
    """
    Calculate the overall generation quality score.

    All six dimensions have equal weight.
    """

    return average(
        list(dimension_scores.values())
    )


def print_dimension_scores(dimension_scores):

    print("\n" + "=" * 70)
    print("GENERATION QUALITY DIMENSIONS")
    print("=" * 70)

    labels = {
        "correctness": "Correctness",
        "grounding": "Grounding",
        "relevance": "Relevance",
        "conciseness": "Conciseness",
        "source_correctness": "Source Correctness",
        "topic_drift": "Topic Drift",
    }

    for dimension, score in dimension_scores.items():

        print(
            f"{labels[dimension]:<22}: "
            f"{score:.2%}"
        )


def print_per_question_scores(scores):

    print("\n" + "=" * 70)
    print("PER-QUESTION QUALITY SCORES")
    print("=" * 70)

    headers = [
        "ID",
        "Correct",
        "Ground",
        "Relevant",
        "Concise",
        "Source",
        "No Drift",
    ]

    print(
        f"{headers[0]:<6}"
        f"{headers[1]:<10}"
        f"{headers[2]:<10}"
        f"{headers[3]:<10}"
        f"{headers[4]:<10}"
        f"{headers[5]:<10}"
        f"{headers[6]:<10}"
    )

    print("-" * 70)

    for item_id, item in scores.items():

        print(
            f"{item_id:<6}"
            f"{item['correctness']:<10.2f}"
            f"{item['grounding']:<10.2f}"
            f"{item['relevance']:<10.2f}"
            f"{item['conciseness']:<10.2f}"
            f"{item['source_correctness']:<10.2f}"
            f"{item['topic_drift']:<10.2f}"
        )


def print_overall_score(score):

    print("\n" + "=" * 70)
    print("FINAL GENERATION QUALITY BENCHMARK")
    print("=" * 70)

    print(
        f"\nOverall Generation Quality: "
        f"{score:.2%}"
    )

    print(
        "\nScoring method:"
    )

    print(
        "Six dimensions with equal weighting:"
    )

    print(
        "  Correctness"
    )
    print(
        "  Grounding"
    )
    print(
        "  Relevance"
    )
    print(
        "  Conciseness"
    )
    print(
        "  Source Correctness"
    )
    print(
        "  Topic Drift"
    )


def main():

    print("=" * 70)
    print(
        "MSc RAG — GENERATION QUALITY BENCHMARK"
    )
    print("=" * 70)

    scores = load_manual_scores()

    print(
        f"\nEvaluation cases: "
        f"{len(scores)}"
    )

    # --------------------------------------------------
    # Dimension averages
    # --------------------------------------------------

    dimension_scores = (
        calculate_dimension_scores(
            scores
        )
    )

    # --------------------------------------------------
    # Per-question results
    # --------------------------------------------------

    print_per_question_scores(
        scores
    )

    # --------------------------------------------------
    # Dimension results
    # --------------------------------------------------

    print_dimension_scores(
        dimension_scores
    )

    # --------------------------------------------------
    # Overall score
    # --------------------------------------------------

    overall_score = (
        calculate_overall_score(
            dimension_scores
        )
    )

    print_overall_score(
        overall_score
    )


if __name__ == "__main__":
    main()