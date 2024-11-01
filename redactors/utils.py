from spacy.tokens import Doc
import logging
import re


def get_line_and_column(text: str, index: int) -> tuple[int, int]:
    """Calculate the line number and column for a given index in the text."""
    line_number = text[:index].count("\n") + 1
    line_start = text.rfind("\n", 0, index) + 1
    column = index - line_start + 1
    return line_number, column


def log_redactions(
    text: str, redactions: list[tuple[int, int]], filename: str, stream
) -> None:
    filename = filename.split("/")[-1]
    for start, end in redactions:
        original = text[start:end]
        line_number, column = get_line_and_column(text, start)
        print(
            f"file:{filename} from line:{line_number},col:{column} to line:{line_number},col{column + len(original)} - '{original}'", file = stream
        )


def find_redactions_from_regex(text: str, regexp) -> list[tuple[int, int]]:
    """Find all occurrences of given regex in the text and return their span indices."""
    return [match.span() for match in re.finditer(regexp, text)]
