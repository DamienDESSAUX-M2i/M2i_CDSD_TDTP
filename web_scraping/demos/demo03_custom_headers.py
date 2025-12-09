"""
Démo 03 : Personnaliser les headers HTTP et le User-Agent

Objectifs :
- Envoyer une requête avec des en-têtes personnalisés
- Se faire passer pour un vrai navigateur
- Visualiser les headers effectivement envoyés
"""

import requests

# URL cible
url = "https://www.wikipedia.org"

# Headers personnalisés (reprennent exactement ceux du support)
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/'
}

# Envoi de la requête avec les headers personnalisés
response = requests.get(url, headers=headers)

print("Code HTTP :", response.status_code)

# Afficher une partie du HTML pour vérifier que la page a bien été récupérée
print("\n=== Aperçu du HTML (300 premiers caractères) ===")
print(response.text[:300])

# Afficher le User-Agent effectivement envoyé
print("\n=== User-Agent envoyé ===")
print(response.request.headers.get("User-Agent"))

# Afficher quelques headers envoyés
print("\n=== Quelques headers envoyés ===")
for key in ["Accept", "Accept-Language", "Referer"]:
    print(f"{key}: {response.request.headers.get(key)}")
