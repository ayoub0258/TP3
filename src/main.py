from load_data import load_all_indexes
from query_processing import process_query
from filtering import filter_documents_any_token, filter_documents_all_tokens
from ranking import BM25, rank_documents

indexes = load_all_indexes()
print("🔹 Clés chargées :", indexes.keys())

# Vérifier avec les bonnes clés
for key in ["title_index", "description_index", "reviews_index"]:
    if key in indexes:
        print(f"🔹 Exemple de {key} index :", list(indexes[key].items())[:3])
    else:
        print(f"⚠️ Clé {key} introuvable dans les indexes.")

synonyms = indexes["origin_synonyms"]

# Initialiser BM25
bm25_models = {
    "title": BM25(indexes["title_index"]),
    "description": BM25(indexes["description_index"])
}

# Poids des critères
weight_factors = {
    "title": 5.0,
    "description": 1.0
}

# Requête utilisateur
query = "Looking for USA electronics"
query_tokens = process_query(query, synonyms)

# Filtrage des documents
filtered_docs = filter_documents_any_token(query_tokens, indexes["title_index"])

# Ranking
ranked_docs = rank_documents(query_tokens, indexes, bm25_models, weight_factors)

print("Documents classés :", ranked_docs[:10])
