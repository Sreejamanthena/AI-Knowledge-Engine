# nlp_utils.py
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy

# Download necessary resources
nltk.download('stopwords', quiet=True)
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


def preprocess_text(text: str) -> str:
    """Basic text cleaning"""
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.lower().strip()


def tokenize_text(text: str):
    return text.split()


def remove_stopwords(tokens):
    return [word for word in tokens if word not in stop_words]


def stemming(tokens):
    return [stemmer.stem(w) for w in tokens]


def lemmatization_spacy(text: str):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]


def word_frequency(tokens):
    return Counter(tokens)


def full_nlp_pipeline(text: str):
    """Combine all NLP steps for analysis"""
    cleaned = preprocess_text(text)
    tokens = tokenize_text(cleaned)
    no_stop = remove_stopwords(tokens)
    stems = stemming(no_stop)
    lemmas = lemmatization_spacy(cleaned)
    freq = word_frequency(no_stop)

    return {
        "cleaned_text": cleaned,
        "tokens": tokens,
        "without_stopwords": no_stop,
        "stems": stems,
        "lemmas": lemmas,
        "word_frequency": dict(freq)
    }
