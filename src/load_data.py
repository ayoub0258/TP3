import json

def load_json(file_path):
    """Charge un fichier JSON et retourne son contenu sous forme de dictionnaire."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

import json
import os

def load_all_indexes():
    """Charge et reformate les fichiers JSON pour structurer les index correctement."""
    index_files = [
        "brand_index.json",
        "description_index.json",  # Besoin de reformater
        "domain_index.json",
        "title_index.json",  # Besoin de reformater
        "origin_index.json",
        "origin_synonyms.json",
        "reviews_index.json"  # Besoin de reformater
    ]
    
    indexes = {}

    for file in index_files:
        file_path = f"data/{file}"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Reformater title, description et review pour une structure plus exploitable
            if file in ["title_index.json", "description_index.json", "reviews_index.json"]:
                reformatted_data = {}
                for keyword, urls in data.items():
                    for url, positions in urls.items():
                        if url not in reformatted_data:
                            reformatted_data[url] = []
                        reformatted_data[url].append(keyword)
                indexes[file.replace(".json", "")] = reformatted_data
            else:
                indexes[file.replace(".json", "")] = data

        except FileNotFoundError:
            print(f"⚠️ Fichier {file} introuvable.")
        except json.JSONDecodeError:
            print(f"❌ Erreur de parsing JSON dans {file}.")

    return indexes

