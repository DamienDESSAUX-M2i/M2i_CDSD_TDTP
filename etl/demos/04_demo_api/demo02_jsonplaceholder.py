import requests 



# URL de base de l'API de test JSONPlaceholder.
BASE_URL = "https://jsonplaceholder.typicode.com"


# Construction de l'URL complète de l'endpoint /posts.
# Cet endpoint renvoie une liste de posts (articles de blog fictifs).
posts_url = f"{BASE_URL}/posts"


# Envoi d'une requête GET pour récupérer tous les posts.
response = requests.get(posts_url)

# print(response.json())

# On s'assure que la requête a réussi.
# Si le code de statut n'indique pas un succès (2xx), une exception est levée.
response.raise_for_status()

# Conversion du corps de la réponse au format JSON en objet Python.
# Ici, l'API renvoie une liste de posts, donc :
# - posts sera une list
# - chaque élément de cette liste sera un dict représentant un post
posts = response.json()

# Afficher le nombre total de posts récupérés.
print(f"Nombre de posts : {len(posts)}")

print("=== Premier post ===")
print(posts[0])

# On peut aussi accéder à des champs spécifiques du premier post.
first_post = posts[0]
print("=== Détails du premier post ===")
print(f"ID du post     : {first_post['id']}")
print(f"ID de l'auteur : {first_post['userId']}")
print(f"Titre          : {first_post['title']}")
print(f"Contenu        : {first_post['body']}")