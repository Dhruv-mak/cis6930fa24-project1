import sys
from typing import List
from spacy.language import Language
from spacy.tokens import Doc
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from redactors.utils import log_redactions
from typing import Union

# Load the model and tokenizer
model = AutoModel.from_pretrained("avsolatorio/NoInstruct-small-Embedding-v0")
tokenizer = AutoTokenizer.from_pretrained("avsolatorio/NoInstruct-small-Embedding-v0")

def get_embedding(text: Union[str, List[str]], mode: str = "sentence"):
    model.eval()
    
    assert mode in ("query", "sentence"), f"mode={mode} was passed but only `query` and `sentence` are the supported modes."

    if isinstance(text, str):
        text = [text]

    inp = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        output = model(**inp)

    # The model is optimized to use the mean pooling for queries,
    # while the sentence / document embedding uses the [CLS] representation.

    if mode == "query":
        vectors = output.last_hidden_state * inp["attention_mask"].unsqueeze(2)
        vectors = vectors.sum(dim=1) / inp["attention_mask"].sum(dim=-1).view(-1, 1)
    else:
        vectors = output.last_hidden_state[:, 0, :]

    return vectors

@Language.component("concept_redactor")
def concept_redactor(doc: Doc) -> Doc:
    """
    A spaCy pipeline component that identifies sentences associated with a concept in a document and marks their tokens for redaction.
    """
    concepts = doc._.concept
    redactions = []
    
    for sent in doc.sents:
        sentence_embedding = get_embedding(sent.text, mode="sentence")
        concept_embeddings = get_embedding(concepts, mode="query")

        scores = F.cosine_similarity(sentence_embedding, concept_embeddings, dim=-1)
        print(f"max score: {scores.max().item()}")
        print(sent.text)

        if scores.max().item() > 0.33:
            for token in sent:
                token._.redact = True
            redactions.append((sent.start_char, sent.end_char))
    
    log_redactions(doc.text, redactions, doc._.input_file, doc._.stream)
    return doc
