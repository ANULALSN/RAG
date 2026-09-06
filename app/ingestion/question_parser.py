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

    for page in pages:

        page_number = page["page"]
        text = page.get("text", "")

        # --------------------------------------
        # Remove OCR-split weightage summaries
        # before splitting into lines.
        #
        # Example:
        # (43 = 12
        # weightage)
        #
        # becomes empty.
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

            section_match = SECTION_PATTERN.search(line)

            if section_match:

                if current_question is not None:
                    questions.append(current_question)
                    current_question = None

                current_section = (
                    section_match.group(1).upper()
                )

                continue

            # --------------------------------------
            # Ignore section instructions
            # --------------------------------------

            if line.lower().startswith("answer any "):
                continue

            # --------------------------------------
            # Ignore weightage summary lines
            # --------------------------------------

            if WEIGHTAGE_PATTERN.search(line):
                continue

            if line.lower() == "weightage)":
                continue

            # --------------------------------------
            # Detect numbered question
            # --------------------------------------

            question_match = QUESTION_PATTERN.match(line)

            if question_match:

                if current_question is not None:
                    questions.append(current_question)

                question_number = int(
                    question_match.group(1)
                )

                question_text = (
                    question_match.group(2)
                    .strip()
                    .lstrip("|:")
                    .strip()
                )

                # Remove any weightage text that may
                # still be present on the same line.
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
                    "weightage": None,
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
                    "weightage": None,
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