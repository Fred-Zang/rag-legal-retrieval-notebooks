# -*- coding: utf-8 -*-

"""
CORPUS LOADER — SOURCE UNIQUE POUR CHARGER LE CORPUS JURIDIQUE

But
---
Centraliser la logique de chargement du corpus pour éviter la duplication de code
dans les scripts de retrieval/benchmark.

Ce module permet de charger :
1) Un corpus XML (parcours récursif d'un dossier + extraction de texte)
2) Un corpus JSONL "chunké" (sortie du Script 8 : 1 ligne = 1 chunk)

Pourquoi
--------
Dans un POC RAG, on veut pouvoir comparer "avant/après" (chunking, filtres, retrievers)
sans modifier 10 scripts. L'objectif est donc d'avoir un seul point d'entrée stable :
- même structure de documents en sortie
- options de filtrage minimales et explicables

Sortie (format homogène)
------------------------
Chaque document (XML) ou chunk (JSONL) est renvoyé sous forme de dict, avec au minimum :
- doc_id : identifiant (chemin du XML ou doc_id du chunk)
- text   : texte principal à indexer

Si disponible (JSONL chunké), on conserve aussi :
- chunk_id, chunk_index, doc_type, meta, links_count, etc.

Notes
-----
- Ce module ne fait pas de BM25, pas d'embeddings, pas de métriques.
- Aucun code n'est exécuté à l'import (important pour Spyder et la réutilisation).
"""

from __future__ import annotations

import json
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, Iterable, List, Optional, Sequence


# =========================================================
# 1) XML — utilitaires
# =========================================================

def strip_xml_namespaces(root: ET.Element) -> None:
    """
    Supprime les namespaces XML "in-place" pour simplifier les recherches XPath.

    Exemple :
    - {http://...}CONTENU  --> CONTENU
    """
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]


def extract_text_from_xml(xml_path: str, remove_namespaces: bool = True) -> str:
    """
    Extrait de manière robuste tout le texte d'un fichier XML.

    Stratégie (POC volontairement simple) :
    - parsing ElementTree
    - optionnel : suppression des namespaces
    - concaténation de tous les text nodes (elem.text + elem.tail)
    - normalisation légère des espaces

    Paramètres
    ----------
    xml_path : str
        Chemin vers le fichier XML.
    remove_namespaces : bool
        Si True, supprime les namespaces avant extraction.

    Retour
    ------
    str
        Texte extrait (potentiellement bruité si XML très riche).
        Pour un usage "propre", préférer le corpus chunké JSONL (script 8).
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        if remove_namespaces:
            strip_xml_namespaces(root)

        parts: List[str] = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                parts.append(elem.text.strip())
            if elem.tail and elem.tail.strip():
                parts.append(elem.tail.strip())

        text = " ".join(parts)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    except ET.ParseError:
        return ""
    except OSError:
        return ""


# =========================================================
# 2) Chargement corpus XML
# =========================================================

def iter_xml_files(data_root: str, limit_files: Optional[int] = None) -> Iterable[str]:
    """
    Itère sur les fichiers .xml d'un répertoire (récursif).

    Paramètres
    ----------
    data_root : str
        Dossier racine à parcourir.
    limit_files : int | None
        Limite de fichiers (debug rapide).

    Yields
    ------
    str
        Chemins complets vers les fichiers XML.
    """
    count = 0
    for root_dir, _, files in os.walk(data_root):
        for name in files:
            if not name.lower().endswith(".xml"):
                continue
            full_path = os.path.join(root_dir, name)
            yield full_path

            count += 1
            if limit_files is not None and count >= limit_files:
                return


def load_documents_from_xml(
    data_root: str,
    min_text_len: int = 200,
    limit_files: Optional[int] = None,
    remove_namespaces: bool = True,
) -> List[Dict[str, Any]]:
    """
    Charge un corpus XML (documents bruts, non chunkés).

    Paramètres
    ----------
    data_root : str
        Racine des données XML.
    min_text_len : int
        Longueur minimale du texte pour conserver un document.
    limit_files : int | None
        Limite de fichiers XML parcourus (debug).
    remove_namespaces : bool
        Si True, supprime les namespaces XML avant extraction.

    Retour
    ------
    List[dict]
        Liste de documents : {"doc_id": <path>, "text": <texte>}
    """
    documents: List[Dict[str, Any]] = []

    for xml_path in iter_xml_files(data_root, limit_files=limit_files):
        text = extract_text_from_xml(xml_path, remove_namespaces=remove_namespaces)
        if text and len(text) >= min_text_len:
            documents.append({"doc_id": xml_path, "text": text})

    return documents


# =========================================================
# 3) Chargement corpus JSONL (chunks)
# =========================================================

def load_documents_from_jsonl(
    jsonl_path: str,
    min_text_len: int = 50,
    limit_lines: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Charge un corpus JSONL produit par le Script 8 (chunks).

    Paramètres
    ----------
    jsonl_path : str
        Chemin vers le JSONL (1 ligne = 1 chunk).
    min_text_len : int
        Longueur minimale du texte pour conserver un chunk.
    limit_lines : int | None
        Limite de lignes (debug rapide).

    Retour
    ------
    List[dict]
        Liste de chunks (dict). On conserve tous les champs présents,
        mais on garantit au minimum 'doc_id' et 'text'.
    """
    if not os.path.exists(jsonl_path):
        raise FileNotFoundError(f"JSONL introuvable : {jsonl_path}")

    chunks: List[Dict[str, Any]] = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if limit_lines is not None and len(chunks) >= limit_lines:
                break

            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            doc_id = obj.get("doc_id")
            text = obj.get("text")

            if not doc_id or not isinstance(text, str):
                continue
            if len(text) < min_text_len:
                continue

            chunks.append(obj)

    return chunks


# =========================================================
# 4) Filtrage métier minimal (optionnel)
# =========================================================

def filter_documents_by_substring(
    documents: Sequence[Dict[str, Any]],
    required_substring: Optional[str],
    search_in: Sequence[str] = ("text", "meta.titre", "doc_id"),
) -> List[Dict[str, Any]]:
    """
    Filtre un corpus en ne conservant que les documents/chunks
    contenant une sous-chaîne (case-insensitive).

    Paramètres
    ----------
    documents : Sequence[dict]
        Documents ou chunks.
    required_substring : str | None
        Sous-chaîne à rechercher. Si None ou vide => aucun filtre.
    search_in : Sequence[str]
        Champs à inspecter :
        - "text"       : contenu indexé
        - "doc_id"     : chemin/identifiant source
        - "meta.titre" : titre métier si présent (chunks JSONL)

    Retour
    ------
    List[dict]
        Sous-ensemble filtré.
    """
    if not required_substring:
        return list(documents)

    needle = required_substring.lower()

    def get_field(doc: Dict[str, Any], key: str) -> str:
        if key == "text":
            return str(doc.get("text") or "")
        if key == "doc_id":
            return str(doc.get("doc_id") or "")
        if key == "meta.titre":
            meta = doc.get("meta") or {}
            return str(meta.get("titre") or "")
        return ""

    out: List[Dict[str, Any]] = []
    for doc in documents:
        haystack = " ".join(get_field(doc, k) for k in search_in).lower()
        if needle in haystack:
            out.append(doc)

    return out


# =========================================================
# 5) API unique (recommandée)
# =========================================================

def load_documents(
    source: str,
    path: str,
    min_text_len: int = 200,
    limit: Optional[int] = None,
    remove_namespaces: bool = True,
) -> List[Dict[str, Any]]:
    """
    Point d'entrée unique pour charger le corpus.

    Paramètres
    ----------
    source : str
        "xml" ou "jsonl"
    path : str
        Dossier racine (xml) ou fichier JSONL (jsonl)
    min_text_len : int
        Seuil minimal de texte.
    limit : int | None
        Limite de fichiers (xml) ou de lignes (jsonl) pour debug.
    remove_namespaces : bool
        (xml) suppression des namespaces.

    Retour
    ------
    List[dict]
        Documents/chunks chargés.
    """
    src = source.strip().lower()
    if src == "xml":
        return load_documents_from_xml(
            data_root=path,
            min_text_len=min_text_len,
            limit_files=limit,
            remove_namespaces=remove_namespaces,
        )
    if src == "jsonl":
        return load_documents_from_jsonl(
            jsonl_path=path,
            min_text_len=min_text_len,
            limit_lines=limit,
        )

    raise ValueError("source doit être 'xml' ou 'jsonl'")
