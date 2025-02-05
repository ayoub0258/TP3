from preprocessing import tokenize, remove_stopwords
from load_data import load_json

def expand_query(query_tokens, synonyms):
    """Ajoute des synonymes aux tokens de la requête."""
    expanded_tokens = set(query_tokens)
    for token in query_tokens:
        if token in synonyms:
            expanded_tokens.update(synonyms[token])  # Ajouter les synonymes
    
    return list(expanded_tokens)

def process_query(query, synonyms):
    """Applique tokenization, normalisation et expansion de requête."""
    tokens = tokenize(query)
    tokens = remove_stopwords(tokens)
    return expand_query(tokens, synonyms)