import spacy
from redactors.date import date_redactor
from spacy.tokens import Doc, Token
import sys

def redact_doc(doc: Doc) -> str:
    redacted_text = []
    for token in doc:
        if token._.get("redact"):
            redacted_text.append("█" * len(token.text))
        else:
            redacted_text.append(token.text_with_ws)
    return "".join(redacted_text)

def test_date_redactor():
    text = "The event is scheduled for 2021-05-21. Another date is 05/21/2021."
    expected_redacted_text = "The event is scheduled for ██████████. Another date is ██████████."
    nlp = spacy.load("en_core_web_trf")
    Doc.set_extension("stream", default=sys.stdout, force=True)
    Doc.set_extension("input_file", default="input.txt", force=True)
    Token.set_extension("redact", default=False, force=True)
    nlp.add_pipe("date_redactor", last=True)
    doc = nlp(text)

    redacted_text = []
    for token in doc:
        if token._.get("redact"):
            redacted_text.append("█" * len(token.text))
        else:
            redacted_text.append(token.text_with_ws)
    
    print(f"redacted_text = {"".join(redacted_text)}")
    print(f"expected_redacted_text = {expected_redacted_text}")
    
    assert "".join(redacted_text) == expected_redacted_text