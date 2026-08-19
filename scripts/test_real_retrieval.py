from qdrant_client import QdrantClient

from app.retrieval.embeddings import embed_text


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"


QUERIES = [
    "What is Big Data?",
    "What are the waves of managing data?",
    "What are the characteristics of Big Data?",
    "What is Volume in Big Data?",
]


def main():
    client = QdrantClient(path=QDRANT_PATH)

    print("=" * 70)
    print("REAL MSc RAG — RETRIEVAL TEST")
    print("=" * 70)

    for query in QUERIES:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        query_vector = embed_text(query)

        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=5,
        ).points

        for rank, result in enumerate(results, start=1):

            payload = result.payload

            print("\n" + "-" * 70)
            print(f"Rank: {rank}")
            print(f"Score: {result.score:.4f}")
            print(f"Subject: {payload.get('subject')}")
            print(f"Module: {payload.get('module')}")
            print(f"Document: {payload.get('document')}")
            print(f"Slide: {payload.get('slide')}")
            print(f"Chunk: {payload.get('chunk_index')}")
            print(f"Title: {payload.get('title')}")
            print(f"Text: {payload.get('text')[:400]}")

    client.close()


if __name__ == "__main__":
    main()