from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


# Store Qdrant data inside our project.
QDRANT_PATH = Path("data/processed/qdrant")

COLLECTION_NAME = "msc_knowledge"
VECTOR_SIZE = 768


def get_client() -> QdrantClient:
    """
    Create a local persistent Qdrant client.

    No Docker, server, cloud account, or API key is required.
    """
    QDRANT_PATH.mkdir(parents=True, exist_ok=True)

    return QdrantClient(path=str(QDRANT_PATH))


def create_collection() -> None:
    """
    Create the MSc knowledge collection if it doesn't exist.
    """
    client = get_client()

    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        print(f"Created collection: {COLLECTION_NAME}")

    else:
        print(f"Collection already exists: {COLLECTION_NAME}")

    client.close()


if __name__ == "__main__":
    create_collection()