"""
Démo 02 : Requête HTTP GET simple avec requests

Objectifs :
- Envoyer une requête GET
- Vérifier le code de statut HTTP
- Inspecter le HTML, le contenu binaire et les en-têtes
"""


import requests

# URL cible (à adapter selon vos tests)
url = "https://example.com/"

# Requête GET simple
response = requests.get(url)

# Vérifier le statut
print("Code HTTP :", response.status_code)  # 200 = OK

# Contenu HTML sous forme de texte (chaîne de caractères)
html = response.text
print("\n=== Aperçu du HTML (500 premiers caractères) ===")
print(html[:500])

# Contenu binaire (utile pour les images, PDF, etc.)
content = response.content
print("\nTaille du contenu binaire (octets) :", len(content))

# Encodage détecté par requests
print("\nEncodage détecté :", response.encoding)

# Headers de la réponse (métadonnées HTTP)
print("\n=== Headers de la réponse ===")
for key, value in response.headers.items():
    print(f"{key}: {value}")