# -*- coding: utf-8 -*-

"""
BENCHMARK QUERIES – RAG JURIDIQUE (POC)

Ce fichier définit :
- les questions utilisateur de référence
- les critères de pertinence associés

Il constitue la base commune à toutes les expériences
de retrieval (BM25, dense, hybride, avec ou sans query understanding).

IMPORTANT :
- Ce fichier ne doit PAS être modifié entre deux runs comparés.
"""

benchmark_queries = [

    {
        "id": "Q1",
        "question": "Dans quels cas un CDI peut-il être rompu sans préavis ?",
        "intent": "rupture_sans_preavis",
        "relevant_keywords": [
            "faute grave",
            "faute lourde",
            "sans préavis",
            "privation de préavis",
            "L1234"
        ],
        "notes": "Cas de rupture immédiate du CDI"
    },

    {
        "id": "Q2",
        "question": "Qu'est-ce qu'un licenciement pour motif économique ?",
        "intent": "licenciement_economique",
        "relevant_keywords": [
            "licenciement pour motif économique",
            "motif économique",
            "L1233"
        ],
        "notes": "Définition juridique du motif économique"
    },

    {
        "id": "Q3",
        "question": "Un salarié peut-il contester un licenciement ?",
        "intent": "contestation_licenciement",
        "relevant_keywords": [
            "contestation",
            "contestations",
            "sanctions",
            "irrégularités",
            "recours",
            "conseil de prud'hommes"
        ],
        "notes": "Voies de recours contre un licenciement"
    }
]
