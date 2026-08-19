import json
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text:latest"

texts = [
    "What is database normalization?",
    "Normalization reduces redundancy in relational databases.",
    "Machine learning algorithms can learn patterns from data."
]


def embed(text: str):
    payload = json.dumps({
        "model": MODEL,
        "input": text
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    start = time.perf_counter()

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    elapsed = time.perf_counter() - start

    return result["embeddings"][0], elapsed


print("=" * 60)
print("NOMIC EMBEDDING BENCHMARK")
print("=" * 60)

for i, text in enumerate(texts, start=1):
    vector, elapsed = embed(text)

    print(f"\nTest {i}")
    print(f"Text: {text}")
    print(f"Time: {elapsed:.4f} seconds")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")

print("\nBenchmark complete.")