# -*- coding: utf-8 -*-

"""
METRICS – RETRIEVAL EVALUATION

Ce module regroupe les métriques utilisées pour évaluer
les moteurs de retrieval (BM25, dense, hybride).

Il est volontairement simple et explicable.
"""

import math


# =========================================================
# 1. DÉTECTION DE PERTINENCE
# =========================================================

def is_relevant(document_text, relevant_keywords):
    """
    Détermine si un document est pertinent
    selon la présence de mots-clés.

    Hypothèse :
    - oracle volontairement simple
    - utilisé uniquement pour le benchmark
    """
    text = document_text.lower()
    return any(keyword.lower() in text for keyword in relevant_keywords)


# =========================================================
# 2. RECALL@K
# =========================================================

def recall_at_k(results, relevant_keywords, k):
    """
    Recall@k :
    - 1 si au moins un document pertinent est présent dans le top-k
    - 0 sinon
    """
    top_k = results[:k]
    for doc, _ in top_k:
        if is_relevant(doc["text"], relevant_keywords):
            return 1
    return 0


# =========================================================
# 3. MEAN RECIPROCAL RANK (MRR)
# =========================================================

def reciprocal_rank(results, relevant_keywords):
    """
    MRR :
    - 1 / rang du premier document pertinent
    - 0 s'il n'y en a aucun
    """
    for rank, (doc, _) in enumerate(results, start=1):
        if is_relevant(doc["text"], relevant_keywords):
            return 1 / rank
    return 0


# =========================================================
# 4. nDCG@K
# =========================================================

def ndcg_at_k(results, relevant_keywords, k):
    """
    nDCG@k (version binaire, normalisée) :

    - DCG : somme des gains des documents pertinents selon leur rang
    - IDCG : DCG idéal (documents pertinents en tête)
    - Score normalisé entre 0 et 1

    Hypothèse :
    - pertinence binaire (pertinent / non pertinent)
    - oracle basé sur mots-clés
    """
    dcg = 0.0
    relevances = []

    # DCG réel
    for i, (doc, _) in enumerate(results[:k], start=1):
        if is_relevant(doc["text"], relevant_keywords):
            dcg += 1 / math.log2(i + 1)
            relevances.append(1)

    # Aucun document pertinent trouvé
    if not relevances:
        return 0.0

    # IDCG : documents pertinents idéalement classés en tête
    idcg = 0.0
    for i in range(1, len(relevances) + 1):
        idcg += 1 / math.log2(i + 1)

    return dcg / idcg

