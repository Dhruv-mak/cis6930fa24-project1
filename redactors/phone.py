from spacy.language import Language
from spacy.tokens import Doc
from commonregex import phone as PHONE_REGEX
from redactors.utils import log_redactions, find_redactions_from_regex


@Language.component("phone_redactor")
def phone_redactor(doc: Doc) -> Doc:
    """
    A spaCy pipeline component that identifies date entities in a document and marks them for redaction.
    """
    text = doc.text
    redactions = find_redactions_from_regex(text, PHONE_REGEX)
    log_redactions(text, redactions, doc._.input_file, doc._.stream)
    mark_tokens_for_phone_redaction(doc, redactions)
    return doc

def mark_tokens_for_phone_redaction(doc: Doc, redactions: list[tuple[int, int]]) -> None:
    for token in doc:
        token._.redact = (
            any(start <= token.idx < end for start, end in redactions)
        )