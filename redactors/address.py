from spacy.language import Language
from spacy.tokens import Doc
from redactors.utils import log_redactions
import pyap

@Language.component("address_redactor")
def address_redactor(doc: Doc) -> Doc:
    """
    A spaCy pipeline component that identifies addresses in a document and marks them for redaction.
    """
    addresses = pyap.parse(doc.text, country='US')

    redactions = []
    for address in addresses:
        address_text = address.data_as_dict['full_address']
        start = doc.text.find(address_text)
        end = start + len(address_text)
        redactions.append((start, end))
    
    # Handle spaCy entities
    spacy_add = []
    for token in doc:
        if token.ent_type_ in {"GPE", "LOC", "FAC"}:
            spacy_add.append((token.idx, token.idx + len(token.text)))
        token._.redact = (
            token.ent_type_ in {"GPE", "LOC", "FAC"}
            or any(start <= token.idx < end for start, end in redactions)
        )
    
    redactions.extend(spacy_add)
    
    log_redactions(doc.text, redactions, doc._.input_file, doc._.stream)

    return doc
