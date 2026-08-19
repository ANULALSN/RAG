def build_context(results: list) -> str:
    """Convert retrieved Qdrant results into LLM context."""

    sections = []

    for index, result in enumerate(results, start=1):
        payload = result.payload

        sections.append(
            f"SOURCE {index}\n"
            f"Document: {payload.get('document', 'Unknown')}\n"
            f"Subject: {payload.get('subject', 'Unknown')}\n"
            f"Module: {payload.get('module', 'Unknown')}\n"
            f"Slide: {payload.get('slide', 'Unknown')}\n"
            f"Title: {payload.get('title', '')}\n\n"
            f"{payload.get('text', '')}"
        )

    return "\n\n".join(sections)