from app.orchestration.rag_pipeline import RAGPipeline


rag = RAGPipeline()

question = "What is Velocity?"

result = rag.ask(
    question,
    subject_id="big-data",
)

print("=" * 70)
print("RAG SOURCE TEST")
print("=" * 70)

print("\nAnswer:")
print(result["answer"])

print("\nAbstained:", result["abstained"])
print("Best Score:", result["best_score"])

print("\nSources:")

for source in result.get("sources", []):
    print("-" * 70)
    print("ID          :", source.get("id"))
    print("Document    :", source.get("document"))
    print("Subject ID  :", source.get("subject_id"))
    print("Material ID :", source.get("material_id"))
    print("Slide       :", source.get("slide"))
    print("Title       :", source.get("title"))

rag.close()