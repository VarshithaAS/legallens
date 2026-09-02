import re

from nltk.corpus import stopwords


# Common English words that should not
# be considered important keywords
STOP_WORDS = set(
    stopwords.words("english")
)


# Important legal terms
LEGAL_KEYWORDS = [
    "agreement",
    "contract",
    "party",
    "payment",
    "rent",
    "termination",
    "liability",
    "obligation",
    "law",
    "court",
    "rights",
    "duty",
    "legal",
    "notice",
    "breach",
    "clause",
    "property",
    "confidential",
    "dispute",
    "jurisdiction",
    "compensation",
    "damages",
    "settlement",
    "ownership",
    "employment",
    "license",
    "consent",
    "penalty",
    "indemnity"
]


def extract_keywords(text, limit=10):
    """
    Extract important keywords from a legal document.
    """

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )

    frequency = {}

    for word in words:

        if word in STOP_WORDS:
            continue

        frequency[word] = (
            frequency.get(word, 0) + 1
        )

    # Give extra importance to legal terms
    for word in LEGAL_KEYWORDS:

        if word in frequency:
            frequency[word] += 5

    # Sort by frequency
    sorted_words = sorted(
        frequency.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        word
        for word, score in sorted_words[:limit]
    ]