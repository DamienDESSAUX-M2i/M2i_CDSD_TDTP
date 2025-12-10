"""
Démo 16 : Extraction d'images et téléchargement

Objectifs :
- Récupérer toutes les balises <img> d'une page
- Construire les URLs absolues des images
- Optionnel : télécharger une image localement

Remarque :
- Le chemin 'data/output/image.jpg' doit exister.
  Créez les dossiers 'data' et 'output' avant de lancer la démo.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

print("=== DÉMO 16 : Extraction d'images ===")
print("-" * 60)

# Site de démonstration pour livres, souvent utilisé en scraping
url = "http://books.toscrape.com"
print("URL cible :", url)
print("-" * 60)

# 1) Récupération de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# 2) Toutes les images
images = soup.find_all("img")
print("[1] Nombre d'images trouvées :", len(images))
print("-" * 60)

# 3) Extraire src et alt, construire URL absolue
image_urls = []
for img in images:
    src = img.get("src")
    alt = img.get("alt", "No description")

    absolute_url = urljoin(url, src)

    image_urls.append(
        {
            "src": absolute_url,
            "alt": alt,
        }
    )

print("[2] Exemple de quelques images extraites :")
for info in image_urls[:5]:
    print(" src :", info["src"])
    print(" alt :", info["alt"])
    print("-" * 20)
print("-" * 60)

# 4) Fonction de téléchargement d'une image
def download_image(image_url, save_path):
    response = requests.get(image_url)
    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)

# 5) Exemple : télécharger la première image
if image_urls:
    first_image_url = image_urls[0]["src"]
    save_path = "data/output/image.jpg"
    print("[3] Téléchargement de la première image :")
    print(" URL :", first_image_url)
    print(" Chemin local :", save_path)
    download_image(first_image_url, save_path)
    print("Téléchargement terminé.")
else:
    print("[3] Aucune image à télécharger.")
print("-" * 60)
