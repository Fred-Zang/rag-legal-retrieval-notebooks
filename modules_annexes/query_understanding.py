# -*- coding: utf-8 -*-

"""
« Les difficultés observées ne viennent pas du retrieval lui-même, 
mais du décalage entre le langage utilisateur et le langage juridique. 
J’ai donc introduit une couche explicite de dictionnaire métier, versionnée et mesurable, 
pour normaliser les intentions avant toute recherche. »

QUERY UNDERSTANDING – RUPTURE SANS PRÉAVIS

Objectif :
- Interpréter une requête utilisateur en langage naturel
- Identifier une intention juridique métier
- Enrichir la requête avec des concepts juridiques pertinents
- Sans LLM, sans heuristique opaque

Cette brique alimente ensuite le retrieval (BM25, dense, hybride).
"""

import yaml
import re


# =========================================================
# 1. CHARGEMENT DU DICTIONNAIRE MÉTIER
# =========================================================

def load_juridical_dictionary(path):
    """
    Charge le dictionnaire juridique YAML.

    Retour :
    - dictionnaire Python
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


dictionary = load_juridical_dictionary("juridical_dictionary.yml")


# =========================================================
# 2. NORMALISATION DE LA REQUÊTE UTILISATEUR
# =========================================================

def normalize_text(text):
    """
    Normalisation simple :
    - minuscules
    - suppression des caractères spéciaux
    """
    text = text.lower()
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# =========================================================
# 3. DÉTECTION D’INTENTION
# =========================================================

def detect_intention(query, dictionary):
    """
    Détecte si la requête correspond à une intention métier connue.

    Retour :
    - clé d'intention (ex: 'rupture_sans_preavis')
    - None sinon
    """
    normalized_query = normalize_text(query)

    for intent_key, intent_data in dictionary.items():
        for phrase in intent_data["intentions_utilisateur"]:
            if phrase in normalized_query:
                return intent_key

    return None


# =========================================================
# 4. ENRICHISSEMENT DE LA REQUÊTE
# =========================================================

def enrich_query(query, intent_key, dictionary):
    """
    Enrichit la requête avec les concepts juridiques associés
    à l’intention détectée.

    Retour :
    - requête enrichie (str)
    """
    intent_data = dictionary[intent_key]

    enriched_terms = (
        intent_data["concepts_juridiques_centrals"]
        + intent_data["termes_juridiques_textes"]
    )

    enriched_query = query + " " + " ".join(enriched_terms)
    return enriched_query


# =========================================================
# 5. PIPELINE COMPLET
# =========================================================

def process_user_query(query, dictionary):
    """
    Pipeline complet de compréhension de requête.
    """
    intent = detect_intention(query, dictionary)

    if intent is None:
        return {
            "intent_detected": None,
            "enriched_query": query,
            "notes": "Aucune intention métier détectée"
        }

    enriched_query = enrich_query(query, intent, dictionary)

    return {
        "intent_detected": intent,
        "enriched_query": enriched_query,
        "codes_cibles": dictionary[intent]["codes_cibles"],
        "articles_cibles": dictionary[intent]["articles_cibles"]
    }


# =========================================================
# 6. EXEMPLE D’UTILISATION
# =========================================================

if __name__ == "__main__":

    user_query = "Dans quels cas un CDI peut-il être rompu sans préavis ?"

    result = process_user_query(user_query, dictionary)

    print("\n=== RÉSULTAT QUERY UNDERSTANDING ===")
    for k, v in result.items():
        print(f"{k} : {v}")
