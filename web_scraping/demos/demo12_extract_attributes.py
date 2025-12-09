"""
Démo 12 : Extraction d'attributs HTML

Objectifs :
- Accéder aux attributs via []
- Utiliser get() pour gérer les attributs optionnels
- Récupérer le dictionnaire complet des attributs
"""

from bs4 import BeautifulSoup

print("=== DÉMO 12 : Extraction d'attributs ===")
print("-" * 60)

html = """
<a href="https://example.com" class="external" target="_blank" title="Example">
    Lien
</a>
<img src="image.jpg" alt="Mon image" width="300" data-id="img1">
"""

soup = BeautifulSoup(html, "lxml")

# 1) Lien <a>
link = soup.find("a")

print("[1] Attributs du lien <a> :")
href = link["href"]
classes = link["class"]
title = link["title"]

print("href   :", href)
print("class  :", classes)
print("title  :", title)
print("-" * 60)

# Utilisation de get() pour éviter une exception si l'attribut manque
print("[2] Récupération avec get() :")
print("target :", link.get("target"))
print("missing (avec valeur par défaut) :", link.get("missing", "N/A"))
print("-" * 60)

# Tous les attributs du lien
print("[3] Tous les attributs du lien (link.attrs) :")
print(link.attrs)
print("-" * 60)

# 2) Image <img>
img = soup.find("img")

print("[4] Attributs de l'image <img> :")
print("src     :", img["src"])
print("alt     :", img["alt"])
print("data-id :", img.get("data-id"))
print("-" * 60)
