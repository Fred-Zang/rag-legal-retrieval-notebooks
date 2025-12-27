# -*- coding: utf-8 -*-
"""
benchmark_queries_v2.py

But
----
Définir un benchmark "article-aware" pour un RAG juridique :
la pertinence est évaluée principalement par la cible attendue (meta.num),
plutôt que par une simple présence de mots-clés dans le texte.

Pourquoi
--------
Un oracle par mots-clés (relevant_keywords) est fragile :
- il sur-note des faux positifs (mots génériques présents partout),
- il sous-note des passages pertinents sémantiques sans les mots exacts.
En juridique, il est plus robuste de vérifier que le chunk provient
d’un article attendu (ex: L1233-3, L1471-1, etc.).

Comment
-------
Chaque requête contient :
- un identifiant
- une question
- une liste de préfixes meta.num acceptés (ex: "L1234", "L1471")
Optionnel : des mots-clés fallback (utile si meta.num est manquant).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class BenchmarkQueryV2:
    """Spécification d’une requête de benchmark avec oracle par meta.num."""
    qid: str
    question: str
    relevant_num_prefixes: List[str]
    relevant_keywords_fallback: Optional[List[str]] = None


def get_benchmark_queries_v2() -> List[BenchmarkQueryV2]:
    """
    Retourne la liste des requêtes V2 (oracle article-aware).

    Remarque importante
    -------------------
    Les préfixes ci-dessous sont volontairement "larges" (préfixes),
    pour un POC : on veut détecter que le retrieval tombe dans la bonne zone
    du code (ex: L1234* pour préavis/indemnité de préavis).
    """
    return [
        BenchmarkQueryV2(
            qid="Q1",
            question="Dans quels cas un CDI peut-il être rompu sans préavis ?",
            relevant_num_prefixes=[
                "L1234",  # Préavis / indemnité compensatrice de préavis (zone la plus discriminante)
            ],
            relevant_keywords_fallback=[
                "préavis",
                "indemnité compensatrice",
                "faute grave",
                "faute lourde",
            ],
        ),
        BenchmarkQueryV2(
            qid="Q2",
            question="Qu'est-ce qu'un licenciement pour motif économique ?",
            relevant_num_prefixes=[
                "L1233",  # Zone licenciement économique (ex: L1233-3)
            ],
            relevant_keywords_fallback=[
                "motif économique",
                "difficultés économiques",
                "mutations technologiques",
                "suppression",
                "transformation d'emploi",
            ],
        ),
        BenchmarkQueryV2(
            qid="Q3",
            question="Un salarié peut-il contester un licenciement ?",
            relevant_num_prefixes=[
                "L1471",  # Prescription / délais prud’homaux (ex: L1471-1) => très discriminant
                "L1235",  # Contentieux/conséquences du licenciement (large mais utile en POC)
            ],
            relevant_keywords_fallback=[
                "prud'hom",  # couvre prud'homme / prud'hommes
                "saisine",
                "délai",
                "prescription",
                "contestation",
            ],
        ),
    ]


