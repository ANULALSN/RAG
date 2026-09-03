from app.retrieval.qdrant_store import get_qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue


COLLECTION_NAME = "msc_knowledge"
MATERIAL_ID = "495bbe09-4118-4825-9660-94ad1fe6f66a"

client = get_qdrant_client()

query_filter = Filter(
    must=[
        FieldCondition(
            key="material_id",
            match=MatchValue(value=MATERIAL_ID),
        )
    ]
)

points, _ = client.scroll(
    collection_name=COLLECTION_NAME,
    scroll_filter=query_filter,
    limit=1000,
    with_payload=True,
    with_vectors=False,
)

print("=" * 70)
print("MATERIAL VECTOR CHECK")
print("=" * 70)

print("Total vectors:", len(points))

slide_14 = [
    point
    for point in points
    if point.payload.get("slide") == 14
]

print("Slide 14 vectors:", len(slide_14))

for point in slide_14:
    payload = point.payload or {}

    print("\n" + "-" * 70)
    print("Point ID    :", point.id)
    print("Document    :", payload.get("document"))
    print("Subject ID  :", payload.get("subject_id"))
    print("Material ID :", payload.get("material_id"))
    print("Slide       :", payload.get("slide"))
    print("Title       :", payload.get("title"))
    print("Source Type :", payload.get("source_type"))

client.close()