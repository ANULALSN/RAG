from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.retrieval.qdrant_store import get_qdrant_client


COLLECTION_NAME = "msc_knowledge"

MATERIAL_ID = "495bbe09-4118-4825-9660-94ad1fe6f66a"


def main():

    client = get_qdrant_client()

    print("=" * 70)
    print("CLEANING MATERIAL VECTORS")
    print("=" * 70)

    print(f"Material ID: {MATERIAL_ID}")

    material_filter = Filter(
        must=[
            FieldCondition(
                key="material_id",
                match=MatchValue(
                    value=MATERIAL_ID
                ),
            )
        ]
    )

    # --------------------------------------------------
    # Count existing vectors
    # --------------------------------------------------

    count_result = client.count(
        collection_name=COLLECTION_NAME,
        count_filter=material_filter,
        exact=True,
    )

    print(
        f"Existing vectors: {count_result.count}"
    )

    if count_result.count == 0:

        print(
            "No vectors found for this material."
        )

        return

    # --------------------------------------------------
    # Delete all vectors belonging to this material
    # --------------------------------------------------

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=material_filter,
        wait=True,
    )

    print(
        "Material vectors deleted successfully."
    )

    # --------------------------------------------------
    # Verify deletion
    # --------------------------------------------------

    count_after = client.count(
        collection_name=COLLECTION_NAME,
        count_filter=material_filter,
        exact=True,
    )

    print(
        f"Vectors remaining: {count_after.count}"
    )

    print("=" * 70)

    client.close()


if __name__ == "__main__":
    main()