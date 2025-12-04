import os                        # Pour lire les variables d'environnement
from dotenv import load_dotenv   # Pour charger le fichier .env
import requests                  # Pour faire une requête HTTP

# 1) Charger le fichier .env présent à la racine du projet
#    Exemple de contenu .env  :
#    API_KEY=DEMO_API_KEY_123456
#    API_URL=https://httpbin.org/get
load_dotenv()

# 2) Récupérer les variables d'environnement
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

print("API_KEY lue depuis .env :", API_KEY)
print("API_URL lue depuis .env :", API_URL)

# Vérification de sécurité : on s'assure qu'elles sont bien définies
if not API_KEY or not API_URL:
    raise RuntimeError("API_KEY ou API_URL non définies. Vérifiez votre fichier .env.")


# 3) Utiliser ces valeurs dans une requête HTTP
# Ici, on appelle l'URL API_URL (par défaut : https://httpbin.org/get)
# et on passe la clé API en paramètre pour vérifier qu'elle est bien transmise.
params = {
    "apikey": API_KEY,
    "demo": "env_test"
}

response = requests.get(API_URL, params=params)
response.raise_for_status()

data = response.json()

print("\n=== Résultat renvoyé par httpbin ===")
print("URL appelée :", data["url"])
print("Arguments (data['args']) :", data["args"])