import json
import urllib.request

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text:latest"

QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"


DOCUMENTS = [
    {
        "id": 1,
        "subject": "DBMS",
        "unit": "Unit 1",
        "document": "DBMS Notes",
        "page": 10,
        "text": (
            "A database is an organized collection of related data "
            "that allows users to store, retrieve, update, and manage information."
        ),
    },
    {
        "id": 2,
        "subject": "DBMS",
        "unit": "Unit 2",
        "document": "DBMS Notes",
        "page": 25,
        "text": (
            "Database normalization is the process of organizing data "
            "in relational databases to reduce redundancy and improve data integrity."
        ),
    },
    {
        "id": 3,
        "subject": "DBMS",
        "unit": "Unit 2",
        "document": "DBMS Notes",
        "page": 26,
        "text": (
            "First Normal Form requires each table cell to contain "
            "a single atomic value."
        ),
    },
    {
        "id": 4,
        "subject": "Machine Learning",
        "unit": "Unit 1",
        "document": "ML Notes",
        "page": 8,
        "text": (
            "Machine learning algorithms learn patterns from data "
            "and use those patterns to make predictions."
        ),
    },
    {
        "id": 5,
        "subject": "Computer Networks",
        "unit": "Unit 1",
        "document": "CN Notes",
        "page": 12,
        "text": (
            "The OSI model divides network communication into seven "
            "layers, each with a specific responsibility."
        ),
    },
]


def embed(text: str):
    payload = json.dumps({
        "model": EMBED_MODEL,
        "input": text,
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["embeddings"][0]


def main():
    client = QdrantClient(path=QDRANT_PATH)

    print("Embedding documents...")

    points = []

    for document in DOCUMENTS:
        vector = embed(document["text"])

        points.append(
            PointStruct(
                id=document["id"],
                vector=vector,
                payload=document,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"Inserted {len(points)} documents.")

    query = "What is database normalization?"

    print(f"\nQuery: {query}")

    query_vector = embed(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
    ).points

    print("\nTop results:\n")

    for rank, result in enumerate(results, start=1):
        print(f"Rank {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Subject: {result.payload['subject']}")
        print(f"Unit: {result.payload['unit']}")
        print(f"Document: {result.payload['document']}")
        print(f"Page: {result.payload['page']}")
        print(f"Text: {result.payload['text']}")
        print("-" * 60)

    client.close()


if __name__ == "__main__":
    main()