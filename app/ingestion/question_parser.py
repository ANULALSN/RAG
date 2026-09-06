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


def parse_section_weightages(
    text: str,
) -> dict[str, int]:
    """
    Extract section-level question weightage.

    Normal OCR:
        (4x2 = 8 weightage)
        (4x3 = 12 weightage)
        (2x5 = 10 weightage)

    Some OCR output may read:
        (43 = 12 weightage)

    where "4x3" was interpreted as "43".

    Returns:
        {
            "A": 2,
            "B": 3,
            "C": 5,
        }
    """

    section_weightages = {}

    # --------------------------------------
    # Find section positions
    # --------------------------------------

    section_matches = list(
        SECTION_PATTERN.finditer(text)
    )

    for index, section_match in enumerate(
        section_matches
    ):

        section = (
            section_match.group(1)
            .upper()
        )

        start = section_match.end()

        if index + 1 < len(section_matches):
            end = section_matches[
                index + 1
            ].start()
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

            # Basic consistency check.
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

            # Only accept the OCR interpretation
            # when the arithmetic is valid.
            if (
                question_count
                * weightage_per_question
                == total_weightage
            ):
                section_weightages[section] = (
                    weightage_per_question
                )

    return section_weightages


def parse_questions(
    pages: list[dict],
) -> list[dict]:

    questions = []

    current_section = None
    current_question = None

    section_first_question = {
        "A": 1,
        "B": 8,
        "C": 15,
    }

    # --------------------------------------
    # Extract section weightages
    # --------------------------------------

    full_text = "\n".join(
        page.get("text", "")
        for page in pages
    )

    section_weightages = parse_section_weightages(
        full_text
    )

    # --------------------------------------
    # Process pages
    # --------------------------------------

    for page in pages:

        page_number = page["page"]
        text = page.get("text", "")

        # --------------------------------------
        # Remove OCR-split weightage summaries
        # before splitting into lines.
        # --------------------------------------

        text = re.sub(
            r"\([^)]*weightage\s*\)",
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines:

            # --------------------------------------
            # Detect section
            # --------------------------------------

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

            # --------------------------------------
            # Ignore section instructions
            # --------------------------------------

            if line.lower().startswith(
                "answer any "
            ):
                continue

            # --------------------------------------
            # Ignore normal weightage summary
            # --------------------------------------

            if WEIGHTAGE_PATTERN.search(line):
                continue

            # --------------------------------------
            # Ignore OCR-split weightage ending
            # --------------------------------------

            if line.lower() == "weightage)":
                continue

            # --------------------------------------
            # Detect numbered question
            # --------------------------------------

            question_match = QUESTION_PATTERN.match(
                line
            )

            if question_match:

                if current_question is not None:
                    questions.append(
                        current_question
                    )

                question_number = int(
                    question_match.group(1)
                )

                question_text = (
                    question_match.group(2)
                    .strip()
                    .lstrip("|:")
                    .strip()
                )

                # Remove any weightage text that
                # remains on the same line.
                question_text = re.sub(
                    r"\(\s*\d+\s*x\s*\d+\s*=\s*\d+\s*weightage\s*\)",
                    "",
                    question_text,
                    flags=re.IGNORECASE,
                ).strip()

                current_question = {
                    "question_number": question_number,
                    "section": current_section,
                    "text": question_text,
                    "page": page_number,
                    "weightage": section_weightages.get(
                        current_section
                    ),
                }

                continue

            # --------------------------------------
            # Recover OCR-missing question number
            # --------------------------------------

            if (
                current_question is None
                and current_section is not None
            ):

                expected_number = (
                    section_first_question[
                        current_section
                    ]
                )

                if not questions:
                    next_number = expected_number
                else:
                    previous = questions[-1]

                    if (
                        previous["section"]
                        == current_section
                    ):
                        next_number = (
                            previous[
                                "question_number"
                            ]
                            + 1
                        )
                    else:
                        next_number = expected_number

                current_question = {
                    "question_number": next_number,
                    "section": current_section,
                    "text": line.lstrip("|:").strip(),
                    "page": page_number,
                    "weightage": section_weightages.get(
                        current_section
                    ),
                }

                continue

            # --------------------------------------
            # Continuation of current question
            # --------------------------------------

            if current_question is not None:

                current_question["text"] += (
                    " " + line
                )

    # ------------------------------------------
    # Save final question
    # ------------------------------------------

    if current_question is not None:
        questions.append(current_question)

    return questions