import re


EXAM_SESSION_PATTERN = re.compile(
    r"(?:DEGREE\s+EXAMINATION|EXAMINATION)\s*,?\s*"
    r"([A-Z]+\s+\d{4})",
    re.IGNORECASE,
)

COURSE_CODE_PATTERN = re.compile(
    r"\b([A-Z]{2,}\d[A-Z0-9]*)\s*-\s*([A-Z][A-Z0-9\s&]+)",
    re.IGNORECASE,
)


def extract_question_paper_metadata(
    pages: list[dict],
) -> dict:

    if not pages:
        return {
            "exam_session": None,
            "course_code": None,
            "exam_title": None,
        }

    # --------------------------------------
    # Use the first page for paper metadata
    # --------------------------------------

    first_page_text = pages[0].get("text", "")

    if not first_page_text.strip():
        return {
            "exam_session": None,
            "course_code": None,
            "exam_title": None,
        }

    lines = [
        line.strip()
        for line in first_page_text.splitlines()
        if line.strip()
    ]

    # --------------------------------------
    # Extract exam session
    # --------------------------------------

    exam_session = None

    session_match = EXAM_SESSION_PATTERN.search(
        first_page_text
    )

    if session_match:
        exam_session = session_match.group(1).upper()

    # --------------------------------------
    # Extract course code and title
    # --------------------------------------

    course_code = None
    exam_title = None

    for line in lines:

        course_match = COURSE_CODE_PATTERN.search(line)

        if course_match:

            course_code = course_match.group(1).upper()

            exam_title = (
                course_match.group(2)
                .strip()
                .upper()
            )

            exam_title = re.sub(
                r"\s+",
                " ",
                exam_title,
            )

            break

    return {
        "exam_session": exam_session,
        "course_code": course_code,
        "exam_title": exam_title,
    }