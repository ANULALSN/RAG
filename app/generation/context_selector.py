def select_context(results: list, max_results: int = 2) -> list:
    """
    Select the most useful retrieved chunks for generation.

    Retrieval can return closely related but unnecessary chunks.
    This function keeps the strongest results while avoiding
    redundant context.
    """

    if not results:
        return []

    selected = []

    for result in results:

        payload = result.payload

        # Skip empty chunks
        text = payload.get("text", "").strip()

        if not text:
            continue

        # Avoid duplicate slides
        slide = payload.get("slide")

        if any(
            item.payload.get("slide") == slide
            for item in selected
        ):
            continue

        selected.append(result)

        if len(selected) >= max_results:
            break

    return selected