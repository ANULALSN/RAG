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
            "subject_id": payload.get("subject_id", "Unknown"),
            "material_id": payload.get("material_id", "Unknown"),
            "slide": payload.get("slide", "Unknown"),
            "title": payload.get("title", ""),
        }

        sources.append(source)

        sections.append(
            f"SOURCE [{index}]\n"
            f"Document: {source['document']}\n"
            f"Subject ID: {source['subject_id']}\n"
            f"Material ID: {source['material_id']}\n"
            f"Slide: {source['slide']}\n"
            f"Title: {source['title']}\n\n"
            f"{payload.get('text', '')}"
        )

    context = "\n\n".join(sections)

    return context, sources