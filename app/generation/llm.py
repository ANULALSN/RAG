import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"


def generate_answer(prompt: str) -> str:
    """Generate an answer using the local Qwen model."""

    payload = json.dumps(
        {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
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

    return result["response"].strip()