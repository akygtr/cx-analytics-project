import re
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# module-level so both functions can use them without reloading each call
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """Light cleaning: removes encoding artifacts, normalizes inch notation,
    collapses whitespace. PRESERVES numbers, punctuation, case (mostly),
    and stylistic emphasis like '...' and '!!!'.

    Designed for downstream models (DistilBERT, BERTopic) that handle their
    own tokenization and benefit from rich text.
    """
    if not isinstance(text, str):
        return ""
    # normalize unicode (handles 'ombré' -> 'ombre' or similar mangling)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # fix doubled apostrophes (inch notation: 5'2'' -> 5'2')
    text = re.sub(r"'{2,}", "'", text)
    # collapse multiple spaces, tabs, newlines into single space
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_text(text):
    """Aggressive cleaning for TF-IDF, topic modeling, and bag-of-words features.
    Lowercases, strips punctuation/numbers, removes stopwords, lemmatizes.
    Returns space-separated tokens.
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    text = text.lower()
    # keep only letters and spaces (numbers and punctuation gone)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    # remove stopwords, very short tokens, lemmatize the rest
    tokens = [lemmatizer.lemmatize(t) for t in tokens
              if t not in stop_words and len(t) > 2]
    return " ".join(tokens)
