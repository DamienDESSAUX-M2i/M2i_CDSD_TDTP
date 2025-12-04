import requests

#url = "https://httpbin.org/bearer"
url = "http://localhost:8080/bearer" # si httpbin.org est down j'utilise mon container

# 1) Appel SANS header Authorization → doit échouer (401)

response = requests.get(url)
print("Sans token, statut :", response.status_code)
print("Réponse :", response.text)
print()

# 2) Appel AVEC header Authorization: Bearer <token>

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.DEMO"  # Token factice

headers = {
    "Authorization": f"Bearer {access_token}"
}


response = requests.get(url, headers=headers)

print("Avec token, statut :", response.status_code)

# Si tout va bien, on devrait avoir authenticated = True
try:
    data = response.json()
    print("Réponse JSON :", data)
    print("Authenticated =", data.get("authenticated"))
except ValueError:
    print("La réponse n'est pas un JSON valide :", response.text)

# Remarque :
# Dans une vraie API (propre backend, API publique, etc.), le principe est identique :
# - Le serveur vérifie le token
# - Si valide → accès autorisé
# - Si invalide/expiré → 401 Unauthorized