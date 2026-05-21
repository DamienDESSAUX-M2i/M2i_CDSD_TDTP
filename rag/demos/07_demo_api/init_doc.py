from rag_system import RAGSystem

MISTRAL_API_KEY = "n1gnUla1CUVYBINxBo2Qh23wOI7kbtLg"

rag = RAGSystem(mistral_api_key=MISTRAL_API_KEY)


documents = [
    "Python est un langage de programmation créé par Guido van Rossum en 1991. Il est connu pour sa syntaxe claire et sa lisibilité.",
    "Les listes en Python sont des collections ordonnées et modifiables. On les crée avec des crochets : ma_liste = [1, 2, 3]. On peut ajouter des éléments avec append().",
    "Les dictionnaires Python stockent des paires clé-valeur. Exemple: mon_dict = {'nom': 'Alice', 'age': 30}. On accède aux valeurs avec dict['cle'].",
    "Le RAG (Retrieval-Augmented Generation) combine retrieval et generation. Il recherche d'abord des documents pertinents, puis utilise ces documents pour générer une réponse avec un LLM.",
    "ChromaDB est une base de données vectorielle open-source pour les applications d'IA. Elle permet de stocker des embeddings et d'effectuer des recherches de similarité.",
]

metadatas = [
    {"source": "python_intro.md", "topic": "python"},
    {"source": "python_lists.md", "topic": "python"},
    {"source": "python_dicts.md", "topic": "python"},
    {"source": "rag.md", "topic": "ml"},
    {"source": "chromadb.md", "topic": "ml"},
]


num_chunks = rag.index_documents(documents, metadatas)
