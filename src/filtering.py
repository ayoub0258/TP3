def filter_documents_any_token(query_tokens, documents):
    """Retourne les documents contenant au moins un token de la requête."""
    return {doc_id: doc_text for doc_id, doc_text in documents.items() if any(token in doc_text for token in query_tokens)}

def filter_documents_all_tokens(query_tokens, documents):
    """Retourne les documents contenant tous les tokens de la requête (hors stopwords)."""
    return {doc_id: doc_text for doc_id, doc_text in documents.items() if all(token in doc_text for token in query_tokens)}
