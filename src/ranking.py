import json
import math

class BM25:
    def __init__(self, index, k1=1.5, b=0.75):
        self.index = index  # Dictionnaire {doc_id: [tokens]}
        self.k1 = k1
        self.b = b
        self.N = len(index)  # Nombre total de documents
        self.avgdl = sum(len(tokens) for tokens in index.values()) / self.N  # Longueur moyenne des documents
        self.idf = self._compute_idf()

    def _compute_idf(self):
        """Calcule l'IDF (Inverse Document Frequency) pour chaque mot-clé."""
        df = {}  # Nombre de documents contenant chaque token
        for tokens in self.index.values():
            for token in set(tokens):  # Un mot est compté une seule fois par document
                df[token] = df.get(token, 0) + 1

        idf = {token: math.log((self.N - df[token] + 0.5) / (df[token] + 0.5) + 1) for token in df}
        return idf

    def score(self, query_tokens, doc_id):
        """Calcule le score BM25 d'un document par rapport à une requête."""
        if doc_id not in self.index:
            return 0

        doc_tokens = self.index[doc_id]
        doc_len = len(doc_tokens)
        score = 0

        for token in query_tokens:
            if token in self.idf:
                f = doc_tokens.count(token)  # Fréquence du token dans le document
                idf = self.idf[token]
                score += idf * ((f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))))

        return score
    
    def exact_match_score(query_tokens, doc_tokens):
        """Retourne 1 si tous les mots de la requête sont dans le document, sinon 0."""
        return 1 if all(token in doc_tokens for token in query_tokens) else 0
    
    def compute_document_score(doc_id, query_tokens, indexes, bm25_models, weight_factors):
        """
        Calcule un score global en combinant plusieurs critères.
        - indexes : Dictionnaires des index (title, description, reviews, etc.)
        - bm25_models : Modèles BM25 pour chaque index.
        - weight_factors : Poids de chaque critère.
        """
        score = 0

        # Score BM25 sur le titre et la description
        if doc_id in indexes["title"]:
            score += weight_factors["title"] * bm25_models["title"].score(query_tokens, doc_id)

        if doc_id in indexes["description"]:
            score += weight_factors["description"] * bm25_models["description"].score(query_tokens, doc_id)

        # Score basé sur les avis (nombre d’avis positifs)
        if doc_id in indexes["reviews"]:
            num_reviews, avg_rating = indexes["reviews"][doc_id]
            score += weight_factors["reviews"] * (num_reviews * avg_rating / 5)  # Note sur 5 normalisée

        # Score de match exact
        if doc_id in indexes["title"]:
            score += weight_factors["exact_match"] * exact_match_score(query_tokens, indexes["title"][doc_id])

        # Boost pour l’origine du produit si mentionné dans la requête
        if doc_id in indexes["origin"]:
            for token in query_tokens:
                if token in indexes["origin"][doc_id]:  # Le produit correspond au pays dans la requête
                    score += weight_factors["origin_boost"]

        return score


#def rank_documents(query_tokens, indexes, bm25_models, weight_factors):
#    scores = {}
#    
#    for doc_id in indexes["title_index"]:
#        score = weight_factors["title"] * bm25_models["title"].score(query_tokens, doc_id)
#        score += weight_factors["description"] * bm25_models["description"].score(query_tokens, doc_id)
#        scores[doc_id] = score
#
#    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
