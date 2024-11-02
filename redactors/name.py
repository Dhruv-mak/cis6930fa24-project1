from spacy.language import Language
from spacy.tokens import Doc
from redactors.utils import log_redactions
from names_dataset import NameDataset
from commonregex import email as EMAIL_REGEX
import re


def check_name(x) -> bool:
    if x["first_name"] is None and x["last_name"] is None:
        return False
    if x["first_name"] is not None:
        for probs in x["first_name"]["country"].values():
            if probs > 0.4:
                return True
    if x["last_name"] is not None:
        for probs in x["last_name"]["country"].values():
            if probs > 0.4:
                return True
    return False


@Language.component("name_redactor")
def name_redactor(doc: Doc) -> Doc:
    """
    A spaCy pipeline component that identifies names in a document and marks them for redaction.
    """
    email_list = EMAIL_REGEX.findall(doc.text)
    names_dict = set()
    nd = NameDataset()
    for email in email_list:
        email_id = email.split("@")[0]
        if "." in email_id:
            for x in email_id.split("."):
                names_dict.add(x)
        if "_" in email_id:
            for x in email_id.split("_"):
                names_dict.add(x)

    names_to_remove = []
    for name in names_dict:
        x = nd.search(name)
        if not check_name(x):
            names_to_remove.append(name)

    for name in names_to_remove:
        names_dict.remove(name)

    redactions = []
    for name in names_dict:
        for match in re.finditer(re.escape(name), doc.text):
            start, end = match.span()
            redactions.append((start, end))

    for redaction in redactions:
        for token in doc:
            if redaction[0] <= token.idx < redaction[1]:
                token._.redact = True

    for token in doc:
        if token.ent_type_ == "PERSON":
            token._.redact = True
            redactions.append((token.idx, token.idx + len(token.text)))

    log_redactions(doc.text, redactions, doc._.input_file, doc._.stream)

    return doc
