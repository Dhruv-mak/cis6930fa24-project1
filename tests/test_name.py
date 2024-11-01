import spacy
from redactors.name import name_redactor
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

def test_name_redactor():
    text = "My name is John Doe."
    expected_redacted_text = "My name is ███████."
    
    nlp = spacy.load("en_core_web_trf")
    Doc.set_extension("stream", default=sys.stdout, force=True)
    Doc.set_extension("input_file", default="input.txt", force=True)
    Token.set_extension("redact", default=False, force=True)
    nlp.add_pipe("name_redactor", last=True)
    doc = nlp(text)
    
    redacted_text = redact_doc(doc)
    
    assert redacted_text == expected_redacted_text