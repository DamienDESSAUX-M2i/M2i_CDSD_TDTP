import pickle
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "intent_model.pkl"

data = [
    ("bonjour", "salutation"),
    ("salut", "salutation"),
    ("bonsoir", "salutation"),
    ("hello", "salutation"),
    ("bonjour je vous contacte", "salutation"),
    ("j'ai un problème avec mon compte", "support"),
    ("mon application plante", "support"),
    ("je n'arrive pas à me connecter", "support"),
    ("erreur lors du paiement", "support"),
    ("le site ne fonctionne plus", "support"),
    ("je veux acheter ce produit", "achat"),
    ("quel est le prix", "achat"),
    ("je souhaite commander", "achat"),
    ("avez-vous une offre", "achat"),
    ("je voudrais passer commande", "achat"),
    ("je suis mécontent du service", "plainte"),
    ("votre service est nul", "plainte"),
    ("je veux faire une réclamation", "plainte"),
    ("je suis très déçu", "plainte"),
    ("ma commande est arrivée cassée", "plainte"),
]

texts = [text for text, label in data]
labels = [label for text, label in data]

model = Pipeline([
    ("vectorizer", CountVectorizer(ngram_range=(1, 2))),
    ("classifier", MultinomialNB()),
])

model.fit(texts, labels)

with open(MODEL_PATH, "wb") as file:
    pickle.dump(model, file)

print(f"Modèle sauvegardé dans : {MODEL_PATH}")
 