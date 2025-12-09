"""
Démo 07 : Introduction à BeautifulSoup

Objectifs :
- Récupérer une page web avec requests
- Parser le HTML avec BeautifulSoup et lxml
- Vérifier le type de l'objet obtenu
"""

from bs4 import BeautifulSoup
import requests

# URL de démonstration : page simple et stable
url = "https://example.com"

print("=== DÉMO 07 : Introduction à BeautifulSoup ===")
print(f"URL cible : {url}")
print("-" * 60)

# 1) Récupération de la page HTML
response = requests.get(url)

print("[1] Code HTTP de la réponse :", response.status_code)
print("-" * 60)

# 2) Parsing du HTML avec le parser 'lxml'
soup = BeautifulSoup(response.text, "lxml")

print("[2] Aperçu des 300 premiers caractères du HTML :")
print(response.text[:300])
print("-" * 60)

# 3) Vérifier le type de l'objet soup
print("[3] Type de l'objet 'soup' :")
print(type(soup))
print("-" * 60)


