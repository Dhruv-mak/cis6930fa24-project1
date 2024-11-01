import spacy
from redactors.phone import phone_redactor
from spacy.tokens import Doc, Token
import sys

def redact_doc(doc):
    redacted_text = []
    for token in doc:
        if token._.get("redact"):
            redacted_text.append("█" * len(token.text))
        else:
            redacted_text.append(token.text_with_ws)
    return "".join(redacted_text)
  
def test_phone_redactor():
    text = "Call me at 555-555-5555."
    expected_redacted_text = "Call me at ████████████."
    
    nlp = spacy.load("en_core_web_trf")
    Doc.set_extension("stream", default=sys.stdout, force=True)
    Doc.set_extension("input_file", default="input.txt", force=True)
    Token.set_extension("redact", default=False, force=True)
    nlp.add_pipe("phone_redactor", last=True)
    doc = nlp(text)
    
    redacted_text = redact_doc(doc)
    
    assert redacted_text == expected_redacted_text