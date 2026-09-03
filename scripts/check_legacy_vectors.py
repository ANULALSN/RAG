from app.retrieval.qdrant_store import get_qdrant_client


COLLECTION_NAME = "msc_knowledge"

client = get_qdrant_client()

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


legacy_points = [
    point
    for point in all_points
    if not (point.payload or {}).get("subject_id")
]


valid_points = [
    point
    for point in all_points
    if (point.payload or {}).get("subject_id")
]


print("=" * 70)
print("QDRANT VECTOR AUDIT")
print("=" * 70)

print("Total vectors :", len(all_points))
print("Legacy vectors:", len(legacy_points))
print("Valid vectors :", len(valid_points))

print("\nLegacy sample:")

for point in legacy_points[:10]:
    payload = point.payload or {}

    print(
        f"ID={point.id} | "
        f"Document={payload.get('document')} | "
        f"Slide={payload.get('slide')} | "
        f"Subject ID={payload.get('subject_id')} | "
        f"Material ID={payload.get('material_id')}"
    )

client.close()