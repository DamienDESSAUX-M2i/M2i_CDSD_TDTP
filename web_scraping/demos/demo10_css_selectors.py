"""
Démo 10 : Utilisation de select() et des sélecteurs CSS

Objectifs :
- Sélectionner des éléments avec des sélecteurs CSS
- Combiner balises, classes, id et relations
- Utiliser des sélecteurs d'attributs et des pseudo-classes simples
"""

from bs4 import BeautifulSoup

print("=== DÉMO 10 : Sélecteurs CSS avec select() ===")
print("-" * 60)

html = """
<div id="header">
    <p class="item intro">Texte 1</p>
    <p class="item">Texte 2</p>
    <div>
        <p>Texte dans div</p>
    </div>
    <a href="http://example.com" target="_blank">Lien externe</a>
    <ul>
        <li>Premier</li>
        <li>Second</li>
        <li>Troisième</li>
    </ul>
</div>
"""

soup = BeautifulSoup(html, "lxml")

# 1) Sélecteur de classe
print("[1] Sélecteur de classe (.item) :")
print(soup.select(".item"))
print("-" * 60)

# 2) Sélecteur d'ID
print("[2] Sélecteur d'ID (#header) :")
print(soup.select("#header"))
print("-" * 60)

# 3) Sélecteur de balise
print("[3] Sélecteur de balise (p) :")
print(soup.select("p"))
print("-" * 60)

# 4) Combinaisons
print("[4] Combinaisons de sélecteurs :")
print("div p :", soup.select("div p"))
print("div > p :", soup.select("div > p"))
print("p.intro :", soup.select("p.intro"))
print("-" * 60)

# 5) Attributs
print("[5] Sélecteurs d'attributs :")
print('a[href^="http"] :', soup.select('a[href^="http"]'))
print('a[target="_blank"] :', soup.select('a[target="_blank"]'))
print("-" * 60)

# 6) Pseudo-classes
print("[6] Pseudo-classes :")
print("li:first-child :", soup.select("li:first-child"))
print("li:nth-child(3) :", soup.select("li:nth-child(3)"))
print("-" * 60)

