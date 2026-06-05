from typing import List, Dict

DOCUMENTS = [
    "Python est un langage de programmation interprete, interactif et oriente objet. Il a ete cree par Guido van Rossum et publie pour la premiere fois en 1991. Python est connu pour sa syntaxe claire et lisible, ce qui en fait un excellent choix pour les debutants. Le langage supporte plusieurs paradigmes de programmation, notamment la programmation procedurale, orientee objet et fonctionnelle.",

    "Les listes en Python sont des collections ordonnees et modifiables. On les cree avec des crochets: ma_liste = [1, 2, 3]. Les listes peuvent contenir des elements de differents types. On peut ajouter des elements avec append(), inserer avec insert(), et supprimer avec remove() ou pop(). Les listes supportent l'indexation negative, le slicing, et de nombreuses methodes utiles comme sort(), reverse(), et extend().",

    "Les dictionnaires Python stockent des paires cle-valeur. On les cree ainsi: mon_dict = {'nom': 'Alice', 'age': 30}. Les cles doivent etre uniques et immuables (strings, nombres, tuples). On accede aux valeurs avec dict['cle'] ou dict.get('cle'). Les dictionnaires sont tres efficaces pour les lookups et sont largement utilises en Python. Ils supportent des operations comme keys(), values(), items(), update(), et pop().",

    "Les fonctions en Python se definissent avec le mot-cle def. Syntaxe: def ma_fonction(param1, param2): return resultat. Les fonctions peuvent avoir des parametres par defaut, des parametres avec nom, et des parametres variables (*args, **kwargs). Python supporte aussi les fonctions lambda (anonymes), les decorateurs, et les closures. Les fonctions sont des objets de premiere classe en Python.",

    "Les classes en Python permettent la programmation orientee objet. On les definit avec le mot-cle class. Une classe contient des attributs (variables) et des methodes (fonctions). Le constructeur __init__ initialise les objets. Python supporte l'heritage (simple et multiple), le polymorphisme, et l'encapsulation. Les attributs peuvent etre publics, proteges (_attr) ou prives (__attr).",

    "Les modules Python sont des fichiers .py contenant du code reutilisable. On les importe avec import ou from module import fonction. Python possede une vaste bibliotheque standard (math, os, sys, datetime, etc.). On peut aussi installer des packages externes avec pip. Les packages sont des collections de modules organises dans des repertoires avec un fichier __init__.py.",

    "La gestion des exceptions en Python utilise try/except/finally. Syntaxe: try: code_risque except ExceptionType: gestion_erreur finally: nettoyage. Python a de nombreuses exceptions built-in comme ValueError, TypeError, KeyError. On peut creer ses propres exceptions en heritant de Exception. Les exceptions permettent de gerer les erreurs proprement sans crasher le programme.",

    "Les comprehensions Python sont des syntaxes concises pour creer des listes, dictionnaires, ou ensembles. Liste: [x*2 for x in range(10) if x%2==0]. Dict: {k: v for k, v in items}. Set: {x for x in data}. Les comprehensions sont plus rapides et lisibles que les boucles for equivalentes. Elles supportent les conditions if et les boucles imbriquees.",

    "Le RAG (Retrieval-Augmented Generation) est une technique qui combine la recherche de documents avec la generation de texte par un LLM. Le systeme recupere d'abord des documents pertinents dans une base de connaissances vectorielle, puis utilise ces documents comme contexte pour generer une reponse precise et ancree dans des sources fiables. Le RAG reduit les hallucinations et permet de citer les sources.",

    "Les embeddings sont des representations vectorielles de texte qui capturent la semantique. Ils sont generes par des modeles d'apprentissage profond comme sentence-transformers ou OpenAI embeddings. Les embeddings transforment du texte en vecteurs denses dans un espace multidimensionnel ou des textes semantiquement similaires sont proches. Ils permettent de calculer la similarite cosinus entre textes.",

    "ChromaDB est une base de donnees vectorielle open-source concue pour les applications d'IA. Elle permet de stocker des embeddings et d'effectuer des recherches de similarite rapidement. ChromaDB supporte la persistance, les metadonnees, les filtres, et peut fonctionner en mode client-serveur. Elle s'integre facilement avec LangChain et d'autres frameworks RAG. ChromaDB utilise HNSW pour les recherches rapides.",

    "LangChain est un framework pour developper des applications basees sur des LLMs. Il fournit des abstractions pour les chains (sequences d'operations), les agents (decision making), les retrievers, et les memory systems. LangChain supporte de nombreux LLMs (OpenAI, Anthropic, HuggingFace) et vector stores. Il facilite la creation de pipelines RAG complexes avec des composants reutilisables.",

    "Le chunking est le processus de decoupage de documents en morceaux plus petits. C'est crucial pour le RAG car les LLMs ont des limites de contexte. Un bon chunking preserve la coherence semantique. Les strategies incluent: fixed-size (taille fixe), recursive (hierarchique), semantic (base sur le sens). Les parametres importants sont chunk_size (taille) et chunk_overlap (chevauchement).",

    "Les metriques d'evaluation RAG incluent: Precision@K (proportion de docs pertinents dans top-K), Recall@K (proportion de docs pertinents trouves), MRR (Mean Reciprocal Rank), faithfulness (fidelite au contexte), answer relevancy (pertinence de la reponse). RAGAS est un framework populaire pour evaluer les systemes RAG avec des metriques automatiques basees sur des LLMs.",

    "FastAPI est un framework web moderne pour Python. Il permet de creer des APIs REST performantes avec validation automatique via Pydantic, documentation OpenAPI automatique, et support async/await. FastAPI est ideal pour deployer des modeles ML et des systemes RAG en production. Il supporte les middlewares, l'authentification, et s'integre bien avec uvicorn pour le serving.",
]

METADATAS = [
    {"source": "python_intro.md", "topic": "python", "subtopic": "basics", "difficulty": "easy"},
    {"source": "python_lists.md", "topic": "python", "subtopic": "data_structures", "difficulty": "easy"},
    {"source": "python_dicts.md", "topic": "python", "subtopic": "data_structures", "difficulty": "easy"},
    {"source": "python_functions.md", "topic": "python", "subtopic": "functions", "difficulty": "medium"},
    {"source": "python_classes.md", "topic": "python", "subtopic": "oop", "difficulty": "medium"},
    {"source": "python_modules.md", "topic": "python", "subtopic": "modules", "difficulty": "medium"},
    {"source": "python_exceptions.md", "topic": "python", "subtopic": "exceptions", "difficulty": "medium"},
    {"source": "python_comprehensions.md", "topic": "python", "subtopic": "advanced", "difficulty": "medium"},
    {"source": "rag_intro.md", "topic": "ml", "subtopic": "rag", "difficulty": "medium"},
    {"source": "embeddings.md", "topic": "ml", "subtopic": "embeddings", "difficulty": "medium"},
    {"source": "chromadb.md", "topic": "ml", "subtopic": "vectorstores", "difficulty": "medium"},
    {"source": "langchain.md", "topic": "ml", "subtopic": "frameworks", "difficulty": "medium"},
    {"source": "chunking.md", "topic": "ml", "subtopic": "rag", "difficulty": "hard"},
    {"source": "evaluation.md", "topic": "ml", "subtopic": "metrics", "difficulty": "hard"},
    {"source": "fastapi.md", "topic": "ml", "subtopic": "deployment", "difficulty": "medium"},
]


def get_documents() -> List[str]:
    return DOCUMENTS


def get_metadatas() -> List[Dict]:
    return METADATAS
