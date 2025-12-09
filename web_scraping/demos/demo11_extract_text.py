"""
Démo 11 : Extraction de texte avec BeautifulSoup

Objectifs :
- Récupérer le texte complet d'un bloc HTML
- Utiliser get_text() avec différentes options
- Faire la différence entre .string et .strings
"""

from bs4 import BeautifulSoup

print("=== DÉMO 11 : Extraction de texte ===")
print("-" * 60)

html = """
<div class="article">
    <h2>Titre de l'article</h2>
    <p>Premier paragraphe avec <strong>texte en gras</strong>.</p>
    <p>Deuxième paragraphe.</p>
</div>
"""

soup = BeautifulSoup(html, "lxml")

div = soup.find("div", class_="article")

# 1) .text et .get_text() (équivalents dans ce contexte)
print("[1] Texte complet de la div avec .text :")
print(div.text)
print("-" * 60)

print("[2] Texte complet de la div avec .get_text() :")
print(div.get_text())
print("-" * 60)

# 2) get_text avec séparateur
print("[3] Texte avec séparateur ' | ' :")
print(div.get_text(separator=" | "))
print("-" * 60)

# 3) get_text avec strip=True
print("[4] Texte avec strip=True (espaces enlevés aux extrémités) :")
print(div.get_text(strip=True))
print("-" * 60)

# 4) .string sur le <h2>
h2 = soup.find("h2")
print("[5] Texte direct du <h2> avec .string :")
print(h2.string)
print("-" * 60)

# 5) .strings : itérateur sur tous les fragments de texte
print("[6] Fragments de texte avec .strings :")
for text in div.strings:
    print(repr(text))
print("-" * 60)
