import re


SECTION_PATTERN = re.compile(
    r"Section\s+([ABC])\s*:",
    re.IGNORECASE,
)

QUESTION_PATTERN = re.compile(
    r"^\s*(\d{1,3})\s*[\.\)]\s*[|:]?\s*(.*)$"
)

WEIGHTAGE_PATTERN = re.compile(
    r"\(\s*(\d+)\s*x\s*(\d+)\s*=\s*(\d+)\s*weightage\s*\)",
    re.IGNORECASE,
)

SECTION_QUESTION_RANGES = {
    "A": (1, 7),
    "B": (8, 14),
    "C": (15, 18),
}


def parse_section_weightages(
    text: str,
) -> dict[str, int]:
    """
    Extract section-level question weightage.

    Examples:
        (4x2 = 8 weightage)
        (4x3 = 12 weightage)
        (2x5 = 10 weightage)

    OCR may sometimes read:
        (43 = 12 weightage)

    Returns:
        {
            "A": 2,
            "B": 3,
            "C": 5,
        }
    """

    section_weightages = {}

    section_matches = list(
        SECTION_PATTERN.finditer(text)
    )

    for index, section_match in enumerate(
        section_matches
    ):

        section = section_match.group(1).upper()

        start = section_match.end()

        if index + 1 < len(section_matches):
            end = section_matches[index + 1].start()
        else:
            end = len(text)

        section_text = text[start:end]

        # ----------------------------------
        # Normal weightage format
        # ----------------------------------

        weightage_match = WEIGHTAGE_PATTERN.search(
            section_text
        )

        if weightage_match:

            question_count = int(
                weightage_match.group(1)
            )

            weightage_per_question = int(
                weightage_match.group(2)
            )

            total_weightage = int(
                weightage_match.group(3)
            )

            if (
                question_count
                * weightage_per_question
                == total_weightage
            ):
                section_weightages[section] = (
                    weightage_per_question
                )

            continue

        # ----------------------------------
        # OCR fallback
        #
        # Example:
        # "(43 = 12 weightage)"
        #
        # Intended:
        # "(4x3 = 12 weightage)"
        # ----------------------------------

        ocr_weightage_match = re.search(
            r"\(\s*(\d+)\s*(\d+)\s*=\s*(\d+)\s*weightage\s*\)",
            section_text,
            re.IGNORECASE,
        )

        if ocr_weightage_match:

            question_count = int(
                ocr_weightage_match.group(1)
            )

            weightage_per_question = int(
                ocr_weightage_match.group(2)
            )

            total_weightage = int(
                ocr_weightage_match.group(3)
            )

            if (
                question_count
                * weightage_per_question
                == total_weightage
            ):
                section_weightages[section] = (
                    weightage_per_question
                )

    return section_weightages


def clean_question_text(text: str) -> str:
    """
    Clean OCR artifacts from question text.
    """

    text = text.strip()

    text = re.sub(
        r"\(\s*\d+\s*x\s*\d+\s*=\s*\d+\s*weightage\s*\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def is_ocr_garbage(line: str) -> bool:
    """
    Detect obvious OCR garbage that should not become
    a question.

    Example:
        2a Mw PF YN
    """

    cleaned = line.strip()

    if not cleaned:
        return True

    # Known style of OCR corruption seen between
    # Section A questions in the 2024 paper.
    if re.fullmatch(
        r"[0-9A-Za-z]{1,3}(?:\s+[A-Za-z]{1,3}){2,}",
        cleaned,
    ):
        return True

    return False


def parse_questions(
    pages: list[dict],
) -> list[dict]:

    questions = []

    current_section = None
    current_question = None

    # --------------------------------------
    # Extract full text
    # --------------------------------------

    full_text = "\n".join(
        page.get("text", "")
        for page in pages
    )

    section_weightages = parse_section_weightages(
        full_text
    )

    # --------------------------------------
    # Process each page
    # --------------------------------------

    for page in pages:

        page_number = page["page"]
        text = page.get("text", "")

        # --------------------------------------
        # Remove weightage summaries.
        #
        # Do this before processing lines so
        # "(4 x 2 = 8 weightage)" does not become
        # part of a question.
        # --------------------------------------

        text = re.sub(
            r"\([^)]*weightage\s*\)",
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        # --------------------------------------
        # Keep blank lines.
        #
        # Blank lines are useful for OCR output
        # where Section A question numbers have
        # disappeared but each question remains
        # in its own paragraph.
        # --------------------------------------

        raw_lines = text.splitlines()

        lines = []

        for raw_line in raw_lines:

            line = raw_line.strip()

            if line:
                lines.append(line)
            else:
                # Preserve paragraph boundaries.
                if lines and lines[-1] != "":
                    lines.append("")

        # --------------------------------------
        # Process lines
        # --------------------------------------

        for line in lines:

            # ----------------------------------
            # Blank line
            # ----------------------------------

            if not line:

                # If the current question has text,
                # keep it as a completed question.
                #
                # This is especially important for
                # OCR output from Section A.
                if (
                    current_question is not None
                    and current_section == "A"
                ):
                    questions.append(
                        current_question
                    )
                    current_question = None

                continue

            # ----------------------------------
            # Detect section
            # ----------------------------------

            section_match = SECTION_PATTERN.search(
                line
            )

            if section_match:

                if current_question is not None:
                    questions.append(
                        current_question
                    )
                    current_question = None

                current_section = (
                    section_match.group(1).upper()
                )

                continue

            # ----------------------------------
            # Ignore section instructions
            # ----------------------------------

            if line.lower().startswith(
                "answer any "
            ):
                continue

            if line.lower().startswith(
                "section "
            ):
                continue

            # ----------------------------------
            # Ignore weightage lines
            # ----------------------------------

            if WEIGHTAGE_PATTERN.search(line):
                continue

            if line.lower() == "weightage)":
                continue

            # ----------------------------------
            # Ignore obvious OCR garbage
            # ----------------------------------

            if is_ocr_garbage(line):
                continue

            # ----------------------------------
            # Detect numbered question
            # ----------------------------------

            question_match = QUESTION_PATTERN.match(
                line
            )

            if question_match:

                detected_number = int(
                    question_match.group(1)
                )

                question_text = (
                    question_match.group(2)
                    .strip()
                    .lstrip("|:")
                    .strip()
                )

                # ----------------------------------
                # Repair OCR question number based
                # on the known section range.
                #
                # Example:
                # Section C:
                # OCR → 5.
                # Actual → 15.
                # ----------------------------------

                if current_section is not None:

                    range_start, range_end = (
                        SECTION_QUESTION_RANGES[
                            current_section
                        ]
                    )

                    if (
                        current_section == "C"
                        and detected_number == 5
                    ):
                        detected_number = 15

                    # If OCR produces a number outside
                    # the valid range for the section,
                    # do not blindly trust it.
                    elif not (
                        range_start
                        <= detected_number
                        <= range_end
                    ):
                        detected_number = None

                else:
                    detected_number = detected_number

                # ----------------------------------
                # If the detected number is valid,
                # start a new question.
                # ----------------------------------

                if detected_number is not None:

                    if current_question is not None:
                        questions.append(
                            current_question
                        )

                    current_question = {
                        "question_number": (
                            detected_number
                        ),
                        "section": current_section,
                        "text": clean_question_text(
                            question_text
                        ),
                        "page": page_number,
                        "weightage": (
                            section_weightages.get(
                                current_section
                            )
                        ),
                    }

                    continue

            # ----------------------------------
            # Section A OCR recovery
            #
            # In the 2024 paper, Q2-Q7 have lost
            # their numbers but remain as separate
            # paragraphs.
            # ----------------------------------

            if current_section == "A":

                range_start, range_end = (
                    SECTION_QUESTION_RANGES["A"]
                )

                existing_section_questions = [
                    question
                    for question in questions
                    if question["section"] == "A"
                ]

                if current_question is not None:
                    existing_section_questions.append(
                        current_question
                    )

                next_number = (
                    range_start
                    + len(existing_section_questions)
                )

                if next_number <= range_end:

                    if current_question is not None:
                        questions.append(
                            current_question
                        )

                    current_question = {
                        "question_number": next_number,
                        "section": "A",
                        "text": clean_question_text(
                            line
                        ),
                        "page": page_number,
                        "weightage": (
                            section_weightages.get(
                                "A"
                            )
                        ),
                    }

                    continue

            # ----------------------------------
            # Continuation of a numbered question
            # ----------------------------------

            if current_question is not None:

                current_question["text"] += (
                    " " + clean_question_text(line)
                )

    # --------------------------------------
    # Save final question
    # --------------------------------------

    if current_question is not None:
        questions.append(current_question)

    # --------------------------------------
    # Final cleanup
    #
    # Remove accidental duplicates and keep
    # question order.
    # --------------------------------------

    cleaned_questions = []

    seen = set()

    for question in questions:

        key = (
            question["section"],
            question["question_number"],
        )

        if key in seen:
            continue

        seen.add(key)
        cleaned_questions.append(question)

    cleaned_questions.sort(
        key=lambda question: (
            question["question_number"]
        )
    )

    return cleaned_questions