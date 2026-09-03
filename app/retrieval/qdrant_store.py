from functools import lru_cache

from qdrant_client import QdrantClient


QDRANT_PATH = "data/processed/qdrant"


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    """
    Return the single shared local Qdrant client
    for this application process.
    """

    return QdrantClient(
        path=QDRANT_PATH
    )