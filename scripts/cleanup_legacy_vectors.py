from app.retrieval.qdrant_store import get_qdrant_client
from qdrant_client.models import PointIdsList


COLLECTION_NAME = "msc_knowledge"

client = get_qdrant_client()

try:
    # --------------------------------------------------
    # 1. Read every vector
    # --------------------------------------------------

    all_points = []
    offset = None

    while True:

        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        all_points.extend(points)

        if offset is None:
            break

    print("=" * 70)
    print("LEGACY VECTOR CLEANUP")
    print("=" * 70)

    print("Total vectors before:", len(all_points))

    # --------------------------------------------------
    # 2. Find legacy vectors
    # --------------------------------------------------

    legacy_points = []

    for point in all_points:

        payload = point.payload or {}

        if not payload.get("material_id"):
            legacy_points.append(point)

    print("Legacy vectors found:", len(legacy_points))

    if not legacy_points:
        print("Nothing to delete.")

    else:

        print("\nLegacy vector examples:")

        for point in legacy_points[:10]:

            payload = point.payload or {}

            print("-" * 70)
            print("Point ID    :", point.id)
            print("Document    :", payload.get("document"))
            print("Subject ID  :", payload.get("subject_id"))
            print("Material ID :", payload.get("material_id"))
            print("Slide       :", payload.get("slide"))
            print("Title       :", payload.get("title"))

        # --------------------------------------------------
        # 3. Delete ONLY legacy vectors
        # --------------------------------------------------

        legacy_ids = [
            point.id
            for point in legacy_points
        ]

        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=PointIdsList(
                points=legacy_ids
            ),
            wait=True,
        )

        print("\nLegacy vectors deleted.")

        # --------------------------------------------------
        # 4. Verify
        # --------------------------------------------------

        remaining = client.count(
            collection_name=COLLECTION_NAME,
            exact=True,
        ).count

        print("Vectors remaining:", remaining)

finally:
    client.close()