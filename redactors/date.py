from spacy.language import Language
from spacy.tokens import Doc
from redactors.utils import log_redactions, find_redactions_from_regex
import re
DATE_REGEX = re.compile(
    r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|'
    r'(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)'
    r'(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}|'
    r'\d{4}[-\./]\d{2}[-\./]\d{2}', 
    re.IGNORECASE
)

@Language.component("date_redactor")
def date_redactor(doc: Doc) -> Doc:
    """
    A spaCy pipeline component that identifies date entities in a document and marks them for redaction.
    """
    text = doc.text
    redactions = find_redactions_from_regex(text, DATE_REGEX)
    log_redactions(text, redactions, doc._.input_file, doc._.stream)
    mark_tokens_for_date_redaction(doc, redactions)
    return doc

def mark_tokens_for_date_redaction(doc: Doc, redactions: list[tuple[int, int]]) -> None:
    """Mark tokens for redaction based on date spans and named entities."""
    for token in doc:
        token._.redact = (
            any(start <= token.idx < end for start, end in redactions)
            # or token.ent_type_ == "DATE"
        )