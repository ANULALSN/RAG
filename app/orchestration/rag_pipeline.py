from qdrant_client import QdrantClient

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


class RAGPipeline:

    def __init__(self):
        self.client = QdrantClient(
            path=QDRANT_PATH
        )

    def ask(self, question: str):
        """Run the complete RAG pipeline."""

        # ---------------------------------------------
        # 1. Embed question
        # ---------------------------------------------

        query_vector = embed_text(
            question
        )

        # ---------------------------------------------
        # 2. Retrieve
        # ---------------------------------------------

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=5,
        ).points

        best_score = (
            results[0].score
            if results
            else 0.0
        )

        # ---------------------------------------------
        # 3. Relevance gate
        # ---------------------------------------------

        if best_score < RELEVANCE_THRESHOLD:

            return {
                "answer": ABSTENTION_MESSAGE,
                "abstained": True,
                "best_score": best_score,
                "sources": [],
            }

        # ---------------------------------------------
        # 4. Select context
        # ---------------------------------------------

        relevant_results = [
            result
            for result in results
            if result.score >= RELEVANCE_THRESHOLD
        ][:MAX_CONTEXT_RESULTS]

        # ---------------------------------------------
        # 5. Build context
        # ---------------------------------------------

        context, sources = build_context(
            relevant_results
        )

        # ---------------------------------------------
        # 6. Build grounded prompt
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
        # 7. Generate
        # ---------------------------------------------

        answer = generate_answer(
            prompt
        )

        # ---------------------------------------------
        # 8. Return structured result
        # ---------------------------------------------

        return {
            "answer": answer,
            "abstained": False,
            "best_score": best_score,
            "sources": sources,
        }

    def close(self):
        self.client.close()