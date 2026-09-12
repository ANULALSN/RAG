from app.db.database import SessionLocal
from app.db.question_repository import list_questions
from app.retrieval.embeddings import embed_text
from app.analysis.question_similarity import (
    cosine_similarity,
    classify_similarity,
)


PAPER_2022_ID = "1fd280e8-4147-463e-8067-80848f1e43f2"
PAPER_2024_ID = "8afe9b9c-331e-463e-97a6-51f69a3feee4"


def main():
    db = SessionLocal()

    try:
        questions_2022 = list_questions(db, PAPER_2022_ID)
        questions_2024 = list_questions(db, PAPER_2024_ID)

        all_questions = questions_2022 + questions_2024

        print(
            f"Generating embeddings for "
            f"{len(all_questions)} questions..."
        )

        embeddings = {}

        for index, question in enumerate(all_questions, start=1):
            print(
                f"Embedding {index}/{len(all_questions)} "
                f"- Q{question.question_number}"
            )

            embeddings[question.id] = embed_text(
                question.text
            )

        print("\nComparing questions...")
        print("=" * 90)

        comparisons = []

        for q22 in questions_2022:
            for q24 in questions_2024:
                score = cosine_similarity(
                    embeddings[q22.id],
                    embeddings[q24.id],
                )

                comparisons.append(
                    {
                        "score": score,
                        "classification": classify_similarity(score),
                        "q22": q22,
                        "q24": q24,
                    }
                )

        comparisons.sort(
            key=lambda item: item["score"],
            reverse=True,
        )
        
        
        repeated_candidates = [
            item
            for item in comparisons
            if item["classification"] == "repeated"
        ]

        print("\nREPEATED QUESTION CANDIDATES")
        print("=" * 90)

        for item in repeated_candidates:
            q22 = item["q22"]
            q24 = item["q24"]

            print(
                f"\nScore: {item['score']:.3f}"
            )

            print(
                f"2022 Q{q22.question_number}: "
                f"{q22.text}"
            )

            print(
                f"2024 Q{q24.question_number}: "
                f"{q24.text}"
            )

        print(
            f"\nTotal repeated candidates: "
            f"{len(repeated_candidates)}"
        )

        print("\nTOP QUESTION SIMILARITIES")
        print("=" * 90)

        for item in comparisons[:20]:
            q22 = item["q22"]
            q24 = item["q24"]

            print(
                f"\nScore: {item['score']:.3f}"
                f" | {item['classification'].upper()}"
            )

            print(
                f"2022 Q{q22.question_number}: "
                f"{q22.text}"
            )

            print(
                f"2024 Q{q24.question_number}: "
                f"{q24.text}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()