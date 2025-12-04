import requests  # Pour effectuer des requêtes HTTP
import json      # Pour manipuler manuellement le JSON si nécessaire

# - Récupérer du JSON depuis une API (GitHub, JSONPlaceholder)
# - Comprendre response.json() vs json.loads(response.text)
# - Lire des objets JSON imbriqués
# - Lire une liste d’objets JSON

# 1) Récupération depuis API GitHub

response = requests.get('https://api.github.com/users/github')

# Méthode 1 : utiliser response.json()
# Cette méthode parse automatiquement le JSON en dict/list Python.
data = response.json()
print("Login :", data['login'])
print("Nombre de repos publics :", data['public_repos'])

# Méthode 2 : json.loads(response.text)
# Utile si on veut parse la réponse manuellement.
data = json.loads(response.text)

# 2) Navigation dans un JSON imbriqué

response = requests.get('https://jsonplaceholder.typicode.com/users/1')
user = response.json()

# Le JSON est un dict contenant d’autres dicts (structure hiérarchique)
print("Nom complet :", user['name'])
print("Ville :", user['address']['city'])            # dict à l’intérieur d’un dict
print("Latitude :", user['address']['geo']['lat'])  # dict à 3 niveaux

# 3) Liste d’objets JSON

# Cet endpoint renvoie une LISTE de posts (liste de dicts)
posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()

# Afficher les 5 premiers
for post in posts[:5]:
    print(f"{post['id']} - {post['title']}")