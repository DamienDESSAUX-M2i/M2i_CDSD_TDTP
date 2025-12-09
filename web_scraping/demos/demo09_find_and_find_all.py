"""
Démo 09 : Utilisation de find() et find_all()

Objectifs :
- Utiliser find() pour récupérer un seul élément
- Utiliser find_all() pour récupérer plusieurs éléments
- Filtrer par balise, classe, id et attributs
"""

from bs4 import BeautifulSoup

print("=== DÉMO 09 : find() et find_all() ===")
print("-" * 60)

# HTML de démonstration
html = """
<html>
<body>
    <h1 id="header">Titre</h1>
    <p class="intro">Intro 1</p>
    <p class="intro">Intro 2</p>
    <p>Autre paragraphe</p>
    <div data-id="123">Contenu div</div>
    <a href="https://example.com">Lien externe</a>
    <ul>
        <li>Un</li>
        <li>Deux</li>
        <li>Trois</li>
    </ul>
</body>
</html>
"""

soup = BeautifulSoup(html, "lxml")

# ======================
# Partie 1 : find()
# ======================
print("[1] Utilisation de find() :")
print("Premier <p> :", soup.find("p"))
print("<p> avec class='intro' :", soup.find("p", class_="intro"))
print("Élément avec id='header' :", soup.find(id="header"))
print("<a> avec href='https://example.com' :", soup.find("a", href="https://example.com"))
print("<div> avec data-id='123' :", soup.find("div", attrs={"data-id": "123"}))
print("-" * 60)

# ======================
# Partie 2 : find_all()
# ======================
print("[2] Utilisation de find_all() :")
print("Tous les <p> :", soup.find_all("p"))
print("Tous les éléments avec class='intro' :", soup.find_all(class_="intro"))
print("Tous les <p>, <div> ou <span> :", soup.find_all(["p", "div", "span"]))
print("Premiers <li> (limit=2) :", soup.find_all("li", limit=2))
print("-" * 60)

