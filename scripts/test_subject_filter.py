from app.retrieval.qdrant_store import get_qdrant_client
from app.retrieval.embeddings import embed_text
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)


COLLECTION_NAME = "msc_knowledge"


client = get_qdrant_client()

question = "What is Veracity?"

query_vector = embed_text(question)

query_filter = Filter(
    must=[
        FieldCondition(
            key="subject_id",
            match=MatchValue(
                value="big-data"
            ),
        )
    ]
)

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    query_filter=query_filter,
    limit=10,
).points


print("=" * 70)
print("SUBJECT FILTER TEST")
print("=" * 70)

print(f"Results: {len(results)}")

for index, result in enumerate(results, start=1):

    payload = result.payload or {}

    print("\n" + "-" * 70)
    print(f"RESULT {index}")
    print("-" * 70)

    print("Score      :", result.score)
    print("Subject ID :", payload.get("subject_id"))
    print("Material ID:", payload.get("material_id"))
    print("Document   :", payload.get("document"))
    print("Slide      :", payload.get("slide"))
    print("Title      :", payload.get("title"))
client.close()