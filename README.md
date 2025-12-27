# 🧠 RAG_Legal__retrieval_notebook — Support de lecture (démarche, benchmarks, roadmap)

<span style="color:#8B949E;">Repo fourni à titre de <b>lecture</b> pour illustrer une démarche RAG (retrieval & évaluation) dans un temps contraint.</span>

---

## 📌 Mémorandum (à lire en premier)

> <span style="color:#4EA1FF; font-weight:700;">Contexte</span>  
> Ce dépôt est un **support de lecture** : il vise à présenter clairement notre **méthode**, notre **progression** et nos **choix techniques** (retrieval, évaluation, itérations) dans un délai court (période de fin d’année / phase de pré-échange).

- <span style="color:#FFA657; font-weight:700;">Données non incluses</span> : le corpus d’exploration est volumineux (~60 Mo) et **n’est pas versionné** ici.  
- <span style="color:#FFA657; font-weight:700;">Source non alignée client</span> : les essais ont été réalisés sur un corpus de référence (type Légifrance) **uniquement pour prototyper la méthode**, et non sur un équivalent “LegiMaroc”.  
- <span style="color:#7EE787; font-weight:700;">Objectif</span> : permettre une lecture rapide des raisonnements, hypothèses, métriques, résultats et limites.  
- <span style="color:#7EE787; font-weight:700;">Suite logique</span> : une version **rejouable** (et industrialisable) sera construite **sur le corpus client** (ou un corpus public strictement équivalent) dès cadrage.

---

> <span style="color:#7EE787; font-weight:700;">Intention & implication</span>  
> Ce dépôt a été construit en mode <b>speed-tests</b> sur une période très courte (fin d’année), avec un objectif clair : <b>illustrer notre implication</b> et notre manière d’attaquer un projet RAG juridique (cadrage, itérations, métriques, enseignements) à partir de la description de mission reçue.  
> <br/>
> <span style="color:#8B949E;">
> Une étude sérieuse démarre selon nous par l’analyse du <b>vrai corpus client</b> (ou d’un extrait représentatif) : formats, structure, métadonnées, versions/dates, typologies, évolutions — afin de définir une stratégie d’extraction/chunking robuste.  
> Ici, nous avons utilisé un <b>extrait Légifrance</b> uniquement comme “matière” pour dérouler la roadmap et valider la mécanique (retrieval + évaluation), sans prétendre à une qualité “déploiement” ni à des résultats optimaux sur ce corpus de substitution.
> </span>

---

## 🚀 Parcours de lecture rapide (5–10 minutes)

<span style="color:#8B949E;">
<b>Note de lecture :</b> certains notebooks démarrent volontairement “brut” (cellules/outputs) car ils proviennent de tests itératifs.  
Pour une lecture confortable, repérer les titres et sections Markdown, puis dérouler dans l’ordre ci-dessous.
</span>

1) 🧭 **Roadmap & questions (fil conducteur)**  
→ [`notebooks/Z_Roadmap-Questions.ipynb`](./notebooks/Z_Roadmap-Questions.ipynb)  
<span style="color:#8B949E;">Notre fil conducteur posé dès le début : étapes, hypothèses, jalons, et questions de cadrage apparues au fil des tests.</span>

2) 🧱 **Analyse corpus (fondations RAG : structure/qualité/extraction/chunking — vision “production”)**  
→ [`notebooks/Z_analyse_corpus_juridique_icons.ipynb`](./notebooks/Z_analyse_corpus_juridique_icons.ipynb)  
<span style="color:#8B949E;">Idées d’analyse fondamentale à mener sur le <b>vrai dataset client</b> (non réalisée ici sur l’extrait de substitution), pour sécuriser l’extraction/chunking et la maintenabilité.</span>

3) 🧪 **Bilan technique des étapes 01 → 10 (progression retrieval + métriques + enseignements)**  
→ [`notebooks/Z_bilan_scripts_1-10.ipynb`](./notebooks/Z_bilan_scripts_1-10.ipynb)  
<span style="color:#8B949E;">Synthèse “step by step” : pourquoi chaque étape existe, ce que nous mesurons, ce que nous validons, et ce que cela implique pour une exécution sur le corpus client.</span>

Ensuite, si besoin : lecture détaillée de la série de scripts **01 → 10** dans l’ordre.

---

## ✅ Ce que ce dépôt démontre

- 🧭 Une approche **itérative et mesurable** : baseline → améliorations → comparaison → conclusions.  
- 🧱 Un cadrage “RAG-ready” : filtres, chunking, indexation, retrieval (BM25 / dense / hybride), **évaluation**.  
- 🧰 Une séparation volontaire de briques **réutilisables** (modules annexes) pour itérer vite, proprement.  
- 🧪 Une attention particulière à la **qualité du corpus** (métadonnées, versions, typologies, structure) en vue d’une mise en production robuste.

---

## 📚 Série principale : notebooks 01 → 10 (dans l’ordre)

> Chaque notebook correspond à une étape et reflète le code testé à l’instant T.  
> Les sorties/observations présentes sont celles obtenues sur le corpus d’exploration (non inclus).

1. 01 — **BM25 simple (baseline)**  
   → [`notebooks/01_BM25_simple_presentation.ipynb`](./notebooks/01_BM25_simple_presentation.ipynb)

2. 02 — **Benchmark BM25 (protocole & métriques)**  
   → [`notebooks/02_Benchmark_BM25_presentation.ipynb`](./notebooks/02_Benchmark_BM25_presentation.ipynb)

3. 03 — **BM25 avec filtres (contraintes métier)**  
   → [`notebooks/03_Benchmark_filtre_BM25_presentation.ipynb`](./notebooks/03_Benchmark_filtre_BM25_presentation.ipynb)

4. 04 — **Dense retrieval (embeddings)**  
   → [`notebooks04_Dense_Retrieval_embeddings_presentation.ipynb`](./notebooks/04_Dense_Retrieval_embeddings_presentation.ipynb)

5. 05 — **BM25 + “query understanding” (expansion/enrichissement)**  
   → [`notebooks/05_BM25_Query_Understanding_presentation.ipynb`](./notebooks/05_BM25_Query_Understanding_presentation.ipynb)

6. 06 — **BM25 filtré + query understanding**  
   → [`notebooks/06_BM25_filtered_query_understanding_presentation.ipynb`](./notebooks/06_BM25_filtered_query_understanding_presentation.ipynb)

7. 07 — **Dense + query understanding**  
   → [`notebooks/07_Dense_with_Query_Understanding_presentation.ipynb`](./notebooks/07_Dense_with_Query_Understanding_presentation.ipynb)

8. 08 — **Chunking XML → chunks exploitables (pré-indexation)**  
   → [`notebooks/08_corpus_chunker_xml_presentation.ipynb`](./notebooks/08_corpus_chunker_xml_presentation.ipynb)

9. 09 — **Benchmark BM25 sur chunks (JSONL chunké)**  
   → [`notebooks/09_Benchmark_BM25_on_JSONL_chunks_presentation.ipynb`](./notebooks/09_Benchmark_BM25_on_JSONL_chunks_presentation.ipynb)

10. 10 — **Hybride BM25 + Dense via RRF sur chunks (fusion de rankings)**  
   → [`notebooks/10_Benchmark_Hybride_RRF_BM25_Dense_chunks_presentation.ipynb`](./notebooks/10_Benchmark_Hybride_RRF_BM25_Dense_chunks_presentation.ipynb)

---

## 🧩 Modules .py, .yml et jsonl construits pour le besoin des tests

> Ces fichiers `.py` ont été volontairement séparés comme briques annexes (réutilisables) pour itérer rapidement dans le temps imparti.

- [`modules_annexes/corpus_chunks_extrait.jsonl`](./modules_annexes/corpus_chunks_extrait.jsonl) — extrait **représentatif** (100 chunks) du corpus JSONL **chunké** : 1 ligne = 1 chunk avec `doc_id`, `text` et métadonnées (utilisé pour illustrer le format et faciliter la lecture ici sans publier le corpus complet ~13 180 lignes trop volumineux).
- [`modules_annexes/corpus_loader.py`](./modules_annexes/corpus_loader.py) — point d’entrée unique de chargement du corpus (XML ou JSONL chunké) + filtre simple, sans logique retrieval.
- [`modules_annexes/benchmark_queries.py`](./modules_annexes/benchmark_queries.py) — jeu de requêtes “V1” (questions + intentions + mots-clés) servant d’oracle simple et stable pour comparer les runs.
- [`modules_annexes/juridical_dictionary.yml`](./modules_annexes/juridical_dictionary.yml) — dictionnaire métier versionné (intentions → concepts/termes/codes/articles cibles) utilisé pour normaliser le langage utilisateur.
- [`modules_annexes/metrics.py`](./modules_annexes/metrics.py) — métriques d’évaluation retrieval (Recall@k, MRR, nDCG@k) avec pertinence binaire basée sur mots-clés (oracle V1).
- [`modules_annexes/query_understanding.py`](./modules_annexes/query_understanding.py) — pipeline de “query understanding” sans LLM : détection d’intention via dictionnaire + enrichissement de requête avant retrieval.
- [`modules_annexes/corpus_loader_jsonl.py`](./modules_annexes/corpus_loader_jsonl.py) — chargeur dédié au corpus JSONL chunké (1 ligne = 1 chunk) en conservant doc_id/text + métadonnées utiles.
- [`modules_annexes/benchmark_queries_v2.py`](./modules_annexes/benchmark_queries_v2.py) — benchmark “article-aware” (oracle par `meta.num` via préfixes d’articles) + fallback mots-clés si la métadonnée manque.


---

## ♻️ Rejouabilité (volontairement hors scope ici)

<span style="color:#8B949E;">
Ce dépôt n’a pas vocation à être “one-click runnable” à ce stade, car :
</span>

- le corpus d’exploration n’est pas versionné,
- et les données utilisées ne sont pas l’équivalent cible côté client.

Une version rejouable pourra être mise en place selon les contraintes retenues :
- exécution locale (venv/conda),
- ou notebook Colab,
- ou conteneur (Docker) si besoin d’un environnement stable,
dès que le corpus client et le cadrage (schémas/versions/typologies) seront disponibles.

---

## 🔒 Notes d’anonymisation

Ce dépôt est destiné à rester **anonyme** conformément aux contraintes côté client :  
- pas de données, pas d’identifiants, pas d’informations sensibles,  
- pas de références nominatives (personnes/projets/organisations) dans le contenu final.
