import requests 

# - Envoyer des headers HTTP personnalisés (User-Agent, Accept, etc.)
# - Vérifier ce que le serveur a bien reçu en lisant la réponse

# Headers que l'on souhaite envoyer au serveur.
# Ce sont des métadonnées sur la requête.
headers = {
    "User-Agent": "TotoMonApplicationETL/1.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Language": "fr-FR"
}

# httpbin.org/get renvoie un JSON contenant :
# - "args"    : les paramètres de la query string
# - "headers" : les en-têtes effectivement reçus
# - "url"     : l'URL appelée
response = requests.get("https://httpbin.org/get", headers=headers)

# S'assurer que la requête s'est bien passée (code 2xx)
response.raise_for_status()

data = response.json()

print("=== URL appelée ===")
print(data["url"])

print("\n=== Headers renvoyés par httpbin (ce qu'il a reçu) ===")
for name, value in data["headers"].items():
    print(f"{name}: {value}")

# Exemple : affichage d'un header précis
print("\nUser-Agent vu par le serveur :")
print(data["headers"].get("User-Agent"))