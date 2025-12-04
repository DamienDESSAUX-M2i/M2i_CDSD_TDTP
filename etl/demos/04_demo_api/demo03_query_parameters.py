import requests 


BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_URL = f"{BASE_URL}/posts"

# Méthode 1 : passer les paramètres directement dans l'URL
print("=== Méthode 1 : paramètres dans l'URL ===")

# Ici, on demande les posts pour userId=1
# L'URL contient directement la query string : ?userId=1
response = requests.get(f"{POSTS_URL}?userId=1")

# Vérifier que la requête a réussi
response.raise_for_status()

# Afficher l'URL finale réellement appelée (peut être utile pour debug)
print(f"URL appelée : {response.url}")

# Récupérer la réponse JSON (liste de posts filtrés par userId=1)
posts_user1 = response.json()
print(f"Nombre de posts pour userId=1 : {len(posts_user1)}")

# Méthode 2 : utiliser un dictionnaire "params" (recommandé)
print("\n=== Méthode 2 : dictionnaire 'params' ===")

# On prépare un dictionnaire Python contenant les paramètres souhaités.
# Ici, on filtre sur un userId précis ET un id de post précis.
params = {
    "userId": 1,  # filtrer par utilisateur
    "id": 5       # filtrer par ID de post
}

# On passe le dictionnaire avec le mot-clé params=.
# requests se charge de construire la query string correctement.
response = requests.get(POSTS_URL, params=params)

# Vérifier le succès de la requête
response.raise_for_status()

# Afficher l'URL finale (avec les paramètres encodés)
print(f"URL appelée avec params : {response.url}")

# Récupérer les posts correspondant aux filtres
filtered_posts = response.json()
print(f"Nombre de posts correspondant à userId=1 et id=5 : {len(filtered_posts)}")
if filtered_posts:
    print("Post renvoyé :")
    print(filtered_posts[0])

# Filtrer plusieurs valeurs pour un même paramètre
# Pour certains APIs, on peut passer une liste pour un même paramètre.
# requests transformera : {'userId': [1, 2]}
# en URL : ?userId=1&userId=2
params_multi = {
    "userId": [1, 2]
}

response = requests.get(POSTS_URL, params=params_multi)
response.raise_for_status()

print(f"URL appelée avec plusieurs userId : {response.url}")

posts_multi = response.json()
print(f"Nombre de posts pour userId=1 OU userId=2 : {len(posts_multi)}")


# Pour illustrer, afficher les premiers IDs de posts récupérés
print("IDs des 5 premiers posts renvoyés :")
for post in posts_multi[:5]:
    print(f"- post id={post['id']} (userId={post['userId']})")