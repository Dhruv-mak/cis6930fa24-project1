import nltk
import spacy
from transformers import AutoModel, AutoTokenizer

if __name__ == "__main__":
    nltk.download('wordnet')
    nltk.download('punkt')
    
    
    model_name = "facebook/bart-large-mnli"
    AutoTokenizer.from_pretrained(model_name)
    AutoModel.from_pretrained(model_name)