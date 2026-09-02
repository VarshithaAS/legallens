import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_textrank_scores(sentences):
    """
    Calculate TextRank importance scores
    for each sentence.
    """

    if not sentences:
        return {}

    # If there is only one sentence
    if len(sentences) == 1:
        return {0: 1.0}

    vectorizer = TfidfVectorizer()

    try:
        matrix = vectorizer.fit_transform(sentences)

    except ValueError:
        return {
            i: 0.0
            for i in range(len(sentences))
        }

    # Calculate similarity between sentences
    similarity_matrix = matrix * matrix.T

    # Create a graph
    graph = nx.from_scipy_sparse_array(
        similarity_matrix
    )

    # Apply PageRank
    scores = nx.pagerank(graph)

    return scores