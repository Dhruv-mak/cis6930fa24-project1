import spacy
from redactors.concept import concept_redactor
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

def test_concept_redactor():
    text = "The global economy is facing unprecedented challenges. Economic growth has slowed significantly. This is completely unrelated sentence."
    expected_redacted_text = "█████████████████████████████████████████████████████████████████████████████████████This is completely unrelated sentence."

    nlp = spacy.load("en_core_web_trf")
    Doc.set_extension("stream", default=sys.stdout, force=True)
    Doc.set_extension("input_file", default="input.txt", force=True)
    Token.set_extension("redact", default=False, force=True)
    Doc.set_extension("concept", default=["economy"], force=True)
    
    nlp.add_pipe("concept_redactor", last=True)
    
    doc = nlp(text)

    redacted_text = redact_doc(doc)
    
    print(f"redacted_text = {redacted_text}")
    print(f"expected_redacted_text = {expected_redacted_text}")
    
    assert redacted_text == expected_redacted_text

if __name__ == "__main__":
    test_concept_redactor()
