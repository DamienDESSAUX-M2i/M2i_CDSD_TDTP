import requests  # Pour envoyer la requête POST
import json      # Pour l'alternative avec json.dumps

url = 'https://jsonplaceholder.typicode.com/posts'

# Données à envoyer pour créer un nouveau post
nouveau_post = {
    'title': 'Mon titre',
    'body': 'Contenu de mon post',
    'userId': 1
}

# Méthode 1 : POST avec json=


# requests.post(url, json=...) :
# - Convertit automatiquement le dict Python en JSON
# - Ajoute l’en-tête "Content-Type: application/json"
response = requests.post(url, json=nouveau_post)

print("Code statut :", response.status_code)  # 201 = Created
print("Post créé :", response.json())


# Méthode 2 : POST avec data= + json.dumps

# json.dumps(...) transforme un dict → JSON string
# Ici on doit préciser le header Content-Type manuellement
response = requests.post(
    url,
    data=json.dumps(nouveau_post),
    headers={'Content-Type': 'application/json'}
)

print("Version data= :", response.json())