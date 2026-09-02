from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_tfidf_scores(sentences):
    """
    Calculate a TF-IDF importance score
    for each sentence.
    """

    if not sentences:
        return {}

    vectorizer = TfidfVectorizer()

    try:
        matrix = vectorizer.fit_transform(sentences)

    except ValueError:
        return {
            i: 0.0
            for i in range(len(sentences))
        }

    scores = {}

    for i in range(matrix.shape[0]):

        # Add the TF-IDF values
        # of all words in the sentence
        score = float(
            matrix.getrow(i).sum()
        )

        scores[i] = score

    return scores