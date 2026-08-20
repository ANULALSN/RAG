import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

REQUEST_TIMEOUT = 120


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
        headers={
            "Content-Type": "application/json"
        },
        method="POST",
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["response"].strip()

    except urllib.error.URLError as error:

        raise RuntimeError(
            f"Ollama request failed: {error}"
        ) from error