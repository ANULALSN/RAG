import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text:latest"


def embed_text(text: str) -> list[float]:
    """Generate a single embedding using the local Ollama model."""

    payload = json.dumps(
        {
            "model": EMBED_MODEL,
            "input": text,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["embeddings"][0]