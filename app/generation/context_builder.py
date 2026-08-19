def build_context(results: list) -> tuple[str, list[dict]]:
    """
    Build LLM context and deterministic source metadata
    from retrieved Qdrant results.
    """

    sections = []
    sources = []

    for index, result in enumerate(results, start=1):
        payload = result.payload

        source = {
            "id": index,
            "document": payload.get("document", "Unknown"),
            "subject": payload.get("subject", "Unknown"),
            "module": payload.get("module", "Unknown"),
            "slide": payload.get("slide", "Unknown"),
            "title": payload.get("title", ""),
        }

        sources.append(source)

        sections.append(
            f"SOURCE [{index}]\n"
            f"Document: {source['document']}\n"
            f"Subject: {source['subject']}\n"
            f"Module: {source['module']}\n"
            f"Slide: {source['slide']}\n"
            f"Title: {source['title']}\n\n"
            f"{payload.get('text', '')}"
        )

    context = "\n\n".join(sections)

    return context, sources