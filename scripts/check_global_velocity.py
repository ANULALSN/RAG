from app.retrieval.qdrant_store import get_qdrant_client
from app.retrieval.embeddings import embed_text


COLLECTION_NAME = "msc_knowledge"

client = get_qdrant_client()

question = "What is Velocity?"
query_vector = embed_text(question)

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=10,
).points

print("=" * 70)
print("GLOBAL VELOCITY RETRIEVAL CHECK")
print("=" * 70)

print("Results:", len(results))

for index, result in enumerate(results, start=1):

    payload = result.payload or {}

    print("\n" + "-" * 70)
    print(f"RESULT {index}")
    print("-" * 70)

    print("Point ID    :", result.id)
    print("Score       :", result.score)
    print("Document    :", payload.get("document"))
    print("Subject ID  :", payload.get("subject_id"))
    print("Material ID :", payload.get("material_id"))
    print("Slide       :", payload.get("slide"))
    print("Title       :", payload.get("title"))
    print("Source Type :", payload.get("source_type"))

client.close()