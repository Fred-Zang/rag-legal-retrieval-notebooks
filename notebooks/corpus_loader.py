# -*- coding: utf-8 -*-

"""
CORPUS LOADER – SOURCE UNIQUE DU CORPUS JURIDIQUE

Responsabilité :
- Parcourir les fichiers XML Légifrance
- Extraire le texte brut des documents
- Construire un corpus homogène
- Appliquer un filtrage métier minimal

Ce module est volontairement agnostique :
- aucun retriever (BM25, dense, etc.)
- aucune métrique
- aucune logique de benchmark

Il garantit que toutes les expériences de retrieval
reposent sur exactement le même périmètre documentaire.
"""

import os
import xml.etree.ElementTree as ET

# Racine des données Légifrance
DATA_ROOT = r"D:\-- Projet RAG Avocats --\data_main\data"


def extract_text_from_xml(xml_path):
    """
    Extrait de manière robuste tout le texte d'un fichier XML.

    Hypothèse volontairement simple pour un POC pédagogique :
    - tout le texte est concaténé
    - aucune tentative fine de parsing juridique
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        texts = []
        for elem in root.iter():
            if elem.text:
                texts.append(elem.text.strip())
        return " ".join(texts)
    except Exception:
        return None


def load_documents(data_root):
    """
    Parcourt récursivement les fichiers XML et construit le corpus.

    Retour :
    - liste de dictionnaires {doc_id, text}
    """
    documents = []

    for root_dir, _, files in os.walk(data_root):
        for file in files:
            if file.lower().endswith(".xml"):
                full_path = os.path.join(root_dir, file)
                text = extract_text_from_xml(full_path)

                # Filtre minimal pour éviter les documents trop pauvres
                if text and len(text) > 200:
                    documents.append({
                        "doc_id": full_path,
                        "text": text
                    })

    return documents


def filter_documents_by_substring(documents, required_substring):
    """
    Filtre le corpus en ne conservant que les documents
    contenant une sous-chaîne donnée (ex: 'Code du travail').

    Objectif :
    - Réduire le bruit inter-code
    - Conserver un périmètre métier cohérent
    """
    required = required_substring.lower()
    return [
        doc for doc in documents
        if required in doc["text"].lower()
    ]


# =========================
# Chargement effectif
# =========================

documents_raw = load_documents(DATA_ROOT)
print(f"Corpus brut chargé : {len(documents_raw)} documents")

documents = filter_documents_by_substring(
    documents_raw,
    "Code du travail"
)

print(f"Corpus filtré 'Code du travail' : {len(documents)} documents")
