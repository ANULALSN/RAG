from qdrant_client import QdrantClient

from app.evaluation.generation_quality_dataset import (
    GENERATION_QUALITY_DATASET,
)
from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context
from app.generation.llm import generate_answer


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 2

ABSTENTION_MESSAGE = (
    "I don't have enough information in the provided course material."
)


def retrieve_context(client, question):
    """Retrieve and prepare context for one question."""

    query_vector = embed_text(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points

    best_score = results[0].score if results else 0.0

    if best_score < RELEVANCE_THRESHOLD:
        return {
            "abstained": True,
            "best_score": best_score,
            "results": [],
            "sources": [],
            "context": "",
        }

    relevant_results = [
        result
        for result in results
        if result.score >= RELEVANCE_THRESHOLD
    ][:MAX_CONTEXT_RESULTS]

    context, sources = build_context(
        relevant_results
    )

    return {
        "abstained": False,
        "best_score": best_score,
        "results": relevant_results,
        "sources": sources,
        "context": context,
    }


def generate_grounded_answer(question, context):
    """Generate an answer strictly from retrieved course material."""

    prompt = f"""
You are an academic assistant answering questions from a course.

Use ONLY the information contained in the COURSE MATERIAL.

STRICT RULES:

1. Answer ONLY the question asked.
2. Use only information explicitly supported by the course material.
3. Do NOT use outside knowledge.
4. Do NOT introduce information from related topics.
5. Do NOT repeat information.
6. Give the shortest complete answer possible.
7. Keep the answer academically clear.
8. If the course material does not contain enough information, reply exactly:

I don't have enough information in the provided course material.

QUESTION:
{question}

COURSE MATERIAL:
{context}

ANSWER:
"""

    return generate_answer(prompt)


def normalize(text):
    """Normalize text for simple lexical comparison."""

    return (
        text.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(",", " ")
        .replace(".", " ")
    )


def concept_coverage(answer, required_concepts):
    """
    Calculate simple lexical concept coverage.

    This is a heuristic only.
    It is NOT a semantic correctness metric.
    """

    if not required_concepts:
        return 1.0, []

    normalized_answer = normalize(answer)

    matched = []

    for concept in required_concepts:

        normalized_concept = normalize(
            concept
        )

        if normalized_concept in normalized_answer:
            matched.append(concept)

    score = (
        len(matched)
        / len(required_concepts)
    )

    return score, matched


def analyze_sources(sources, expected_slides):
    """
    Compare retrieved source slides against the gold source slides.
    """

    retrieved_slides = [
        source["slide"]
        for source in sources
    ]

    retrieved_set = set(
        retrieved_slides
    )

    expected_set = set(
        expected_slides
    )

    correct_sources = (
        retrieved_set & expected_set
    )

    extra_sources = (
        retrieved_set - expected_set
    )

    missing_sources = (
        expected_set - retrieved_set
    )

    return {
        "retrieved_slides": retrieved_slides,
        "correct_sources": sorted(
            correct_sources
        ),
        "extra_sources": sorted(
            extra_sources
        ),
        "missing_sources": sorted(
            missing_sources
        ),
        "all_expected_found": (
            expected_set <= retrieved_set
        ),
        "primary_source_found": bool(
            correct_sources
        ),
    }


def print_manual_evaluation_template():
    """Print dimensions that require semantic evaluation."""

    print("\nMANUAL EVALUATION")
    print("-" * 70)

    print(
        "Correctness       : [0-1]"
    )
    print(
        "Grounding         : [0-1]"
    )
    print(
        "Relevance         : [0-1]"
    )
    print(
        "Conciseness       : [0-1]"
    )
    print(
        "Topic drift       : [0-1]"
    )

    print(
        "\nThese dimensions require semantic/manual "
        "evaluation and are not inferred automatically."
    )


def evaluate_item(client, item):

    question = item["question"]

    print("\n" + "=" * 70)
    print(
        f"{item['id']}: {question}"
    )
    print("=" * 70)

    retrieval = retrieve_context(
        client,
        question,
    )

    print(
        f"Best retrieval score: "
        f"{retrieval['best_score']:.4f}"
    )

    # ==================================================
    # EXPECTED ABSTENTION
    # ==================================================

    if item.get("expected_abstention", False):

        actual_abstention = (
            retrieval["abstained"]
        )

        print(
            f"Expected abstention : "
            f"{'YES' if item['expected_abstention'] else 'NO'}"
        )

        print(
            f"Actual abstention   : "
            f"{'YES' if actual_abstention else 'NO'}"
        )

        result = (
            "CORRECT"
            if actual_abstention
            else "INCORRECT"
        )

        print(
            f"Result              : {result}"
        )

        return {
            "id": item["id"],
            "abstention_correct": (
                actual_abstention
            ),
            "concept_coverage": 1.0
            if actual_abstention
            else 0.0,
            "primary_source_found": True
            if actual_abstention
            else False,
            "all_expected_sources_found": True
            if actual_abstention
            else False,
            "extra_source_count": 0,
            "missing_source_count": 0,
        }

    # ==================================================
    # UNEXPECTED ABSTENTION
    # ==================================================

    if retrieval["abstained"]:

        print(
            "\nUNEXPECTED ABSTENTION"
        )

        print(
            ABSTENTION_MESSAGE
        )

        return {
            "id": item["id"],
            "abstention_correct": False,
            "concept_coverage": 0.0,
            "primary_source_found": False,
            "all_expected_sources_found": False,
            "extra_source_count": 0,
            "missing_source_count": len(
                item["expected_slides"]
            ),
        }

    # ==================================================
    # SOURCE ANALYSIS
    # ==================================================

    source_analysis = analyze_sources(
        retrieval["sources"],
        item["expected_slides"],
    )

    print("\nSOURCE ANALYSIS")
    print("-" * 70)

    print(
        f"Expected slides       : "
        f"{item['expected_slides']}"
    )

    print(
        f"Retrieved slides      : "
        f"{source_analysis['retrieved_slides']}"
    )

    print(
        f"Correct source slides : "
        f"{source_analysis['correct_sources']}"
    )

    print(
        f"Extra source slides   : "
        f"{source_analysis['extra_sources']}"
    )

    print(
        f"Missing source slides : "
        f"{source_analysis['missing_sources']}"
    )

    print(
        f"Primary source found  : "
        f"{'YES' if source_analysis['primary_source_found'] else 'NO'}"
    )

    # ==================================================
    # GENERATION
    # ==================================================

    print("\nGENERATING ANSWER...")

    answer = generate_grounded_answer(
        question,
        retrieval["context"],
    )

    print("\nANSWER")
    print("-" * 70)
    print(answer)

    # ==================================================
    # REFERENCE ANSWER
    # ==================================================

    print("\nREFERENCE ANSWER")
    print("-" * 70)
    print(
        item["reference_answer"]
    )

    # ==================================================
    # CONCEPT COVERAGE
    # ==================================================

    coverage, matched = concept_coverage(
        answer,
        item["required_concepts"],
    )

    print("\nAUTOMATIC CONCEPT CHECK")
    print("-" * 70)

    print(
        f"Concept coverage : "
        f"{coverage:.2%}"
    )

    print(
        f"Matched concepts : "
        f"{matched}"
    )

    # ==================================================
    # SOURCES
    # ==================================================

    print("\nSOURCES USED")
    print("-" * 70)

    for source in retrieval["sources"]:

        print(
            f"[{source['id']}] "
            f"{source['document']} "
            f"— Slide {source['slide']}"
        )

    # ==================================================
    # MANUAL EVALUATION
    # ==================================================

    print_manual_evaluation_template()

    return {
        "id": item["id"],
        "abstention_correct": None,
        "concept_coverage": coverage,
        "primary_source_found": (
            source_analysis[
                "primary_source_found"
            ]
        ),
        "all_expected_sources_found": (
            source_analysis[
                "all_expected_found"
            ]
        ),
        "extra_source_count": len(
            source_analysis[
                "extra_sources"
            ]
        ),
        "missing_source_count": len(
            source_analysis[
                "missing_sources"
            ]
        ),
    }


def main():

    print("=" * 70)
    print(
        "MSc RAG — GENERATION QUALITY EVALUATION"
    )
    print("=" * 70)

    print(
        f"\nEvaluation cases: "
        f"{len(GENERATION_QUALITY_DATASET)}"
    )

    print(
        f"Relevance threshold: "
        f"{RELEVANCE_THRESHOLD}"
    )

    print(
        f"Maximum context results: "
        f"{MAX_CONTEXT_RESULTS}"
    )

    client = QdrantClient(
        path=QDRANT_PATH
    )

    evaluation_results = []

    for item in GENERATION_QUALITY_DATASET:

        result = evaluate_item(
            client,
            item,
        )

        evaluation_results.append(
            result
        )

    client.close()

    # ==================================================
    # FINAL AUTOMATIC SUMMARY
    # ==================================================

    print("\n" + "=" * 70)
    print(
        "AUTOMATIC QUALITY SUMMARY"
    )
    print("=" * 70)

    total = len(
        evaluation_results
    )

    if total == 0:
        print("No evaluation cases.")
        return

    average_concept_coverage = (
        sum(
            result["concept_coverage"]
            for result in evaluation_results
        )
        / total
    )

    primary_source_accuracy = (
        sum(
            1
            for result in evaluation_results
            if result["primary_source_found"]
        )
        / total
    )

    total_extra_sources = sum(
        result["extra_source_count"]
        for result in evaluation_results
    )

    total_missing_sources = sum(
        result["missing_source_count"]
        for result in evaluation_results
    )

    abstention_cases = [
        result
        for result in evaluation_results
        if result["abstention_correct"]
        is not None
    ]

    correct_abstentions = sum(
        1
        for result in abstention_cases
        if result["abstention_correct"]
    )

    print(
        f"Cases evaluated          : "
        f"{total}"
    )

    print(
        f"Average concept coverage : "
        f"{average_concept_coverage:.2%}"
    )

    print(
        f"Primary source accuracy  : "
        f"{primary_source_accuracy:.2%}"
    )

    print(
        f"Extra retrieved sources  : "
        f"{total_extra_sources}"
    )

    print(
        f"Missing expected sources : "
        f"{total_missing_sources}"
    )

    if abstention_cases:

        abstention_accuracy = (
            correct_abstentions
            / len(abstention_cases)
        )

        print(
            f"Abstention accuracy      : "
            f"{abstention_accuracy:.2%}"
        )

    print("\n" + "=" * 70)
    print(
        "IMPORTANT"
    )
    print("=" * 70)

    print(
        "Correctness, grounding, relevance, "
        "conciseness, and topic drift require "
        "semantic evaluation."
    )

    print(
        "The automatic metrics above are "
        "supporting diagnostics, not final "
        "generation-quality scores."
    )


if __name__ == "__main__":
    main()