from app.retrieval.qdrant_store import get_qdrant_client

from app.retrieval.embeddings import embed_text
from app.generation.context_builder import build_context
from app.generation.llm import generate_answer

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)


COLLECTION_NAME = "msc_knowledge"

RELEVANCE_THRESHOLD = 0.70
MAX_CONTEXT_RESULTS = 2

ABSTENTION_MESSAGE = (
    "I don't have enough information in the provided course material."
)


class RAGPipeline:

    def __init__(self):
        self.client = get_qdrant_client()

    def ask(
        self,
        question: str,
        subject_id: str | None = None,
    ):
        """
        Run the complete RAG pipeline.

        If subject_id is provided, retrieval is restricted
        to vectors belonging to that subject.

        If subject_id is None, existing global retrieval
        behavior is preserved.
        """

        # ---------------------------------------------
        # 1. Embed question
        # ---------------------------------------------

        query_vector = embed_text(
            question
        )

        # ---------------------------------------------
        # 2. Build optional subject filter
        # ---------------------------------------------

        query_filter = None

        if subject_id:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="subject_id",
                        match=MatchValue(
                            value=subject_id
                        ),
                    )
                ]
            )

        # ---------------------------------------------
        # 3. Retrieve
        # ---------------------------------------------

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=query_filter,
            limit=5,
        ).points

        best_score = (
            results[0].score
            if results
            else 0.0
        )

        # ---------------------------------------------
        # 4. Relevance gate
        # ---------------------------------------------

        if best_score < RELEVANCE_THRESHOLD:

            return {
                "answer": ABSTENTION_MESSAGE,
                "abstained": True,
                "best_score": best_score,
                "sources": [],
            }

        # ---------------------------------------------
        # 5. Select context
        # ---------------------------------------------

        relevant_results = [
            result
            for result in results
            if result.score >= RELEVANCE_THRESHOLD
        ][:MAX_CONTEXT_RESULTS]

        # ---------------------------------------------
        # 6. Build context
        # ---------------------------------------------

        context, sources = build_context(
            relevant_results
        )

        # ---------------------------------------------
        # 7. Build grounded prompt
        # ---------------------------------------------

        prompt = f"""
You are an academic assistant answering questions
from a course.

Use ONLY the information contained in the
course material.

STRICT RULES:

1. Answer ONLY the question asked.
2. Use only information explicitly supported
   by the course material.
3. Do NOT use outside knowledge.
4. Do NOT introduce information from related topics.
5. Do NOT repeat information.
6. Give the shortest complete answer possible.
7. Keep the answer academically clear.
8. If the course material does not contain enough
   information, reply exactly:

I don't have enough information in the provided course material.

QUESTION:
{question}

COURSE MATERIAL:
{context}

ANSWER:
"""

        # ---------------------------------------------
        # 8. Generate
        # ---------------------------------------------

        answer = generate_answer(
            prompt
        )

        # ---------------------------------------------
        # 9. Return structured result
        # ---------------------------------------------

        return {
            "answer": answer,
            "abstained": False,
            "best_score": best_score,
            "sources": sources,
        }

    def close(self):
        self.client.close()