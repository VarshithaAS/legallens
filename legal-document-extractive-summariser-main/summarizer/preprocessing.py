import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Download required NLTK data if needed
try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOP_WORDS = set(stopwords.words("english"))


try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


lemmatizer = WordNetLemmatizer()


def split_sentences(text):
    """
    Split document text into sentences.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def preprocess_sentence(sentence):
    """
    Clean and normalize one sentence.
    """

    # Convert to lowercase
    sentence = sentence.lower()

    # Keep alphabetic words
    words = re.findall(
        r"[a-zA-Z]+",
        sentence
    )

    cleaned_words = []

    for word in words:

        # Remove stop words
        if word in STOP_WORDS:
            continue

        # Remove very short words
        if len(word) < 2:
            continue

        # Lemmatization
        word = lemmatizer.lemmatize(word)

        cleaned_words.append(word)

    return " ".join(cleaned_words)


def preprocess_document(text):
    """
    Complete preprocessing pipeline.
    """

    sentences = split_sentences(text)

    original_sentences = []
    cleaned_sentences = []

    for sentence in sentences:

        # Ignore extremely short sentences
        if len(sentence) < 20:
            continue

        cleaned = preprocess_sentence(
            sentence
        )

        if cleaned:

            original_sentences.append(
                sentence
            )

            cleaned_sentences.append(
                cleaned
            )

    return (
        original_sentences,
        cleaned_sentences
    )