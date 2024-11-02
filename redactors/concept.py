import sys
from spacy.language import Language
from spacy.tokens import Doc
# import nltk
# from nltk.corpus import wordnet
from transformers import pipeline
from redactors.utils import log_redactions
import requests

# def get_similar_words(concept):
#     related_words = set()
#     synsets = wordnet.synsets(concept)
#     for syn in synsets:
#         for lemma in syn.lemmas():
#             related_words.add(lemma.name())
#     related_words.add(concept)
#     return related_words

def get_similar_from_api(concept):
    result = requests.get(f"https://api.datamuse.com/words", params={
        "ml": concept,
        "max": 30
    })
    if result.status_code == 200:
        return [item["word"] for item in result.json()]
    else:
        return []


@Language.component("concept_redactor")
def concept_redactor(doc: Doc) -> Doc:
    concepts = doc._.concept
    redactions = []
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)
    candidate_labels = list(concepts)
    for concept in concepts:
        candidate_labels.extend(get_similar_from_api(concept))
    
    for sent in doc.sents:
        if any(concept.lower() in sent.text.lower() for concept in candidate_labels):
            for token in sent:
                token._.redact = True
            start_char = sent.start_char
            end_char = sent.end_char
            redactions.append((start_char, end_char))
            continue
        result = classifier(sent.text, candidate_labels=candidate_labels)
        if any(
            result["labels"][i] in candidate_labels and result["scores"][i] > 0.3
            for i in range(len(result["labels"]))
        ):
            for token in sent:
                token._.redact = True
            start_char = sent.start_char
            end_char = sent.end_char
            redactions.append((start_char, end_char))
    
    log_redactions(doc.text, redactions, doc._.input_file, doc._.stream)
    return doc