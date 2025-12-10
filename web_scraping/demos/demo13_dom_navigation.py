"""
Démo 13 : Navigation dans l'arbre DOM avec BeautifulSoup

Objectifs :
- Parcourir les enfants directs d'un élément
- Parcourir tous les descendants
- Accéder au parent
- Naviguer entre éléments frères (siblings)
- Utiliser find_next_sibling et find_previous_sibling
"""

from bs4 import BeautifulSoup

print("=== DÉMO 13 : Navigation dans l'arbre DOM ===")
print("-" * 60)

html = """
<div class="parent">
    <h2>Titre</h2>
    <p>Paragraphe 1</p>
    <p>Paragraphe 2</p>
    <ul><li>Item 1</li>
        <li>Item 2</li>
    </ul>
</div>
"""

html2 = """
<div class="parent"><h2>Titre</h2><p>Paragraphe 1</p><p>Paragraphe 2</p><ul><li>Item 1</li><li>Item 2</li></ul></div>
"""

# Parsing du HTML
soup = BeautifulSoup(html, "lxml")
div = soup.find("div", class_="parent")

# 1) Enfants directs de <div class="parent">
print("[1] Noms des enfants directs de div.parent :")
children = list(div.children)
for child in children:
    # child peut être une balise ou du texte (sauts de ligne, espaces)
    if child.name:  # On ignore les textes/espaces
        print("-", child.name)
print("-" * 60)

# 2) Tous les descendants (en profondeur)
print("[2] Nombre total de descendants de div.parent :")
descendants = list(div.descendants)
print("-" * 60)
print("les descendants :")
print(descendants)
print("-" * 60)
print(len(descendants))
print("Aperçu des types des premiers descendants :")
for d in descendants[:5]:
    print(" ", type(d), "->", repr(getattr(d, "name", d)))
print("-" * 60)

# 3) Parent d'un élément
print("[3] Parent de la balise <h2> :")
h2 = soup.find("h2")
print("Nom de la balise parent de <h2> :", h2.parent.name)
print("-" * 60)

# 4) Siblings (frères et soeurs)
print("[4] Navigation entre frères (siblings) :")
p1 = soup.find("p")  # Premier <p>

# p1.next_sibling est souvent un saut de ligne (\n), donc on saute deux fois
print("Premier <p> :", p1)
print("Prochain sibling significatif (p1.next_sibling.next_sibling) :")
print(p1.next_sibling.next_sibling)
print("-" * 60)

# Méthodes utiles
print("[5] Méthodes find_next_sibling et find_previous_sibling :")
next_p = p1.find_next_sibling("p")
prev = p1.find_previous_sibling()

print("Prochain <p> avec find_next_sibling('p') :", next_p)
print("Frère précédent de p1 (peut être None) :", prev)
print("-" * 60)

