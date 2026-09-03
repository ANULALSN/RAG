from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue


QDRANT_PATH = "data/processed/qdrant"
COLLECTION_NAME = "msc_knowledge"

MATERIAL_ID = "02c4b56c-fbba-4f1e-a27d-cb4e9cdfc7f9"


def main():

    print("=" * 70)
    print("MATERIAL VECTOR INSPECTION")
    print("=" * 70)

    client = QdrantClient(
        path=QDRANT_PATH
    )

    try:

        result = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="material_id",
                        match=MatchValue(
                            value=MATERIAL_ID
                        ),
                    )
                ]
            ),
            limit=5,
            with_payload=True,
            with_vectors=False,
        )

        points = result[0]

        print(
            f"Matching points: {len(points)}"
        )

        for index, point in enumerate(
            points,
            start=1,
        ):

            payload = point.payload

            print("\n" + "-" * 70)
            print(f"POINT {index}")
            print("-" * 70)

            print(
                f"Point ID    : {point.id}"
            )

            print(
                f"Subject ID  : "
                f"{payload.get('subject_id')}"
            )

            print(
                f"Material ID : "
                f"{payload.get('material_id')}"
            )

            print(
                f"Document    : "
                f"{payload.get('document')}"
            )

            print(
                f"Slide       : "
                f"{payload.get('slide')}"
            )

            print(
                f"Chunk index : "
                f"{payload.get('chunk_index')}"
            )

            print(
                f"Title       : "
                f"{payload.get('title')}"
            )

            text = payload.get(
                "text",
                "",
            )

            print(
                f"Text        : "
                f"{text[:200]}..."
            )

    finally:
        client.close()


if __name__ == "__main__":
    main()