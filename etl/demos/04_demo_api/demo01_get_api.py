import requests  # Bibliothèque tierce qui simplifie les requêtes HTTP (GET, POST, etc.)



# Envoi d'une requête GET simple vers l'URL racine de l'API GitHub.
response = requests.get("https://api.github.com")

# Afficher le code de statut HTTP.
# Exemples :
# - 200 : OK (succès)
# - 404 : Not Found
# - 500 : Erreur serveur
print(f"Statut : {response.status_code}")

# Afficher le contenu brut de la réponse (sous forme de chaîne de caractères).
# Utile pour voir exactement ce que renvoie le serveur.
print("=== Contenu brut (.text) ===")
print(response.text)


# Tenter d'interpréter le corps de la réponse comme du JSON.
# .json() parse le JSON et renvoie un objet Python (dict ou list).
# Si la réponse n'est pas du JSON valide, .json() lève une exception.
print("=== Contenu parsé en JSON (.json()) ===")
print(response.json())

print("=== Headers de la réponse ===")
print(response.headers)

# Vérifier le succès de la requête avec le code de statut.
# Convention HTTP : les codes 2xx (200, 201, 204, ...) signifient "succès".
if response.status_code == 200:
    print("Succès : la requête s'est bien déroulée.")
else:
    print("Erreur : la requête a échoué.")

    # Alternative plus "Pythonique" : laisser requests lever une exception
# si le code de statut indique une erreur (4xx ou 5xx).
# - Si tout va bien (2xx ou 3xx), rien ne se passe.
# - En cas d'erreur, une exception HTTPError est levée.
response.raise_for_status()