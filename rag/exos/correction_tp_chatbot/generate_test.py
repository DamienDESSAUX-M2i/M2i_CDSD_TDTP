test_dataset_solution = [
    # Questions factuelles - Python basics
    {
        "id": 1,
        "question": "Qui a cree Python et en quelle annee?",
        "expected_answer": "Python a ete cree par Guido van Rossum et publie pour la premiere fois en 1991.",
        "relevant_docs": ["python_intro.md"],
        "category": "factual",
        "difficulty": "easy"
    },
    {
        "id": 2,
        "question": "Comment creer une liste en Python?",
        "expected_answer": "On cree une liste avec des crochets: ma_liste = [1, 2, 3]",
        "relevant_docs": ["python_lists.md"],
        "category": "factual",
        "difficulty": "easy"
    },
    {
        "id": 3,
        "question": "Comment acceder a une valeur dans un dictionnaire?",
        "expected_answer": "On accede aux valeurs avec dict['cle'] ou dict.get('cle')",
        "relevant_docs": ["python_dicts.md"],
        "category": "factual",
        "difficulty": "easy"
    },
    
    # Questions how-to - Python
    {
        "id": 4,
        "question": "Comment definir une fonction avec des parametres par defaut?",
        "expected_answer": "On utilise def ma_fonction(param1, param2=valeur_defaut): return resultat",
        "relevant_docs": ["python_functions.md"],
        "category": "how_to",
        "difficulty": "medium"
    },
    {
        "id": 5,
        "question": "Comment gerer les exceptions en Python?",
        "expected_answer": "Avec try/except/finally: try: code_risque except ExceptionType: gestion_erreur finally: nettoyage",
        "relevant_docs": ["python_exceptions.md"],
        "category": "how_to",
        "difficulty": "medium"
    },
    {
        "id": 6,
        "question": "Comment creer une list comprehension?",
        "expected_answer": "Syntaxe: [x*2 for x in range(10) if x%2==0] pour creer une liste",
        "relevant_docs": ["python_comprehensions.md"],
        "category": "how_to",
        "difficulty": "medium"
    },
    
    # Questions conceptuelles - Python
    {
        "id": 7,
        "question": "Quels sont les paradigmes de programmation supportes par Python?",
        "expected_answer": "Python supporte la programmation procedurale, orientee objet et fonctionnelle.",
        "relevant_docs": ["python_intro.md"],
        "category": "conceptual",
        "difficulty": "easy"
    },
    {
        "id": 8,
        "question": "Quelle est la difference entre append() et extend() pour les listes?",
        "expected_answer": "append() ajoute un element, extend() ajoute plusieurs elements d'un iterable.",
        "relevant_docs": ["python_lists.md"],
        "category": "conceptual",
        "difficulty": "medium"
    },
    
    # Questions factuelles - ML/RAG
    {
        "id": 9,
        "question": "Qu'est-ce que le RAG?",
        "expected_answer": "Le RAG est une technique qui combine la recherche de documents avec la generation par LLM pour reduire les hallucinations.",
        "relevant_docs": ["rag_intro.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    {
        "id": 10,
        "question": "Que sont les embeddings?",
        "expected_answer": "Les embeddings sont des representations vectorielles de texte qui capturent la semantique dans un espace multidimensionnel.",
        "relevant_docs": ["embeddings.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    
    # Questions how-to - ML/RAG
    {
        "id": 11,
        "question": "Comment ChromaDB effectue-t-il les recherches rapides?",
        "expected_answer": "ChromaDB utilise HNSW (Hierarchical Navigable Small World) pour effectuer des recherches de similarite rapides.",
        "relevant_docs": ["chromadb.md"],
        "category": "how_to",
        "difficulty": "hard"
    },
    {
        "id": 12,
        "question": "Quels sont les parametres importants du chunking?",
        "expected_answer": "Les parametres importants sont chunk_size (taille) et chunk_overlap (chevauchement).",
        "relevant_docs": ["chunking.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    
    # Questions conceptuelles - ML/RAG
    {
        "id": 13,
        "question": "Pourquoi le chunking est-il important pour le RAG?",
        "expected_answer": "Le chunking est crucial car les LLMs ont des limites de contexte, et un bon chunking preserve la coherence semantique.",
        "relevant_docs": ["chunking.md"],
        "category": "conceptual",
        "difficulty": "hard"
    },
    {
        "id": 14,
        "question": "Quels types de composants LangChain fournit-il?",
        "expected_answer": "LangChain fournit des chains (sequences), agents (decision making), retrievers, et memory systems.",
        "relevant_docs": ["langchain.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    
    # Questions sur l'evaluation
    {
        "id": 15,
        "question": "Quelles sont les metriques d'evaluation RAG?",
        "expected_answer": "Les metriques incluent Precision@K, Recall@K, MRR, faithfulness, et answer relevancy.",
        "relevant_docs": ["evaluation.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    {
        "id": 16,
        "question": "Qu'est-ce que RAGAS?",
        "expected_answer": "RAGAS est un framework pour evaluer les systemes RAG avec des metriques automatiques basees sur des LLMs.",
        "relevant_docs": ["evaluation.md"],
        "category": "factual",
        "difficulty": "medium"
    },
    
    # Questions deployment
    {
        "id": 17,
        "question": "Quels sont les avantages de FastAPI?",
        "expected_answer": "FastAPI offre validation automatique via Pydantic, documentation OpenAPI automatique, et support async/await.",
        "relevant_docs": ["fastapi.md"],
        "category": "factual",
        "difficulty": "easy"
    },
    
    # Questions complexes multi-docs
    {
        "id": 18,
        "question": "Comment construire un systeme RAG complet avec LangChain et ChromaDB?",
        "expected_answer": "Il faut utiliser ChromaDB pour stocker les embeddings, LangChain pour orchestrer le retrieval et la generation, et implementer le chunking approprie.",
        "relevant_docs": ["rag_intro.md", "chromadb.md", "langchain.md", "chunking.md"],
        "category": "conceptual",
        "difficulty": "hard"
    },
    {
        "id": 19,
        "question": "Quelle est la relation entre embeddings et recherche de similarite?",
        "expected_answer": "Les embeddings transforment le texte en vecteurs, permettant de calculer la similarite cosinus pour trouver des textes semantiquement proches.",
        "relevant_docs": ["embeddings.md", "chromadb.md"],
        "category": "conceptual",
        "difficulty": "medium"
    },
    
    # Question hors sujet
    {
        "id": 20,
        "question": "Quelle est la capitale de la France?",
        "expected_answer": "Information non disponible dans la documentation.",
        "relevant_docs": [],
        "category": "out_of_scope",
        "difficulty": "easy"
    },
    
    # Questions supplementaires
    {
        "id": 21,
        "question": "Comment importer un module en Python?",
        "expected_answer": "On importe avec import ou from module import fonction.",
        "relevant_docs": ["python_modules.md"],
        "category": "how_to",
        "difficulty": "easy"
    },
    {
        "id": 22,
        "question": "Quelles sont les strategies de chunking?",
        "expected_answer": "Les strategies incluent fixed-size (taille fixe), recursive (hierarchique), et semantic (base sur le sens).",
        "relevant_docs": ["chunking.md"],
        "category": "factual",
        "difficulty": "hard"
    },
]

# Verification et statistiques
assert len(test_dataset_solution) >= 20, "Minimum 20 questions requises"

df_test = pd.DataFrame(test_dataset_solution)
print(f"{len(test_dataset_solution)} questions creees\n")
print("Categories:")
print(df_test['category'].value_counts())
print("\nDifficultes:")
print(df_test['difficulty'].value_counts())

# Sauvegarder
with open("test_dataset_solution.json", "w", encoding="utf-8") as f:
    json.dump(test_dataset_solution, f, ensure_ascii=False, indent=2)