"""
Démo 08 : Premier parsing d'un contenu HTML local

Objectifs :
- Parser une chaîne HTML stockée dans une variable
- Accéder à des balises simples (title, h1, p)
- Utiliser prettify() pour afficher un HTML indenté
"""

from bs4 import BeautifulSoup

print("=== DÉMO 08 : Premier parsing d'un HTML local ===")
print("-" * 60)

# HTML de démonstration (contenu local, pas de requête réseau)
html = """
<html>
<head><title>Ma Page</title></head>
<body>
    <h1 class="main-title">Titre Principal</h1>
    <p class="intro">Premier paragraphe.</p>
    <p>Deuxième paragraphe.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    <a href="https://example.com" class="external">Lien</a>
</body>
</html>
"""

# 1) Parsing du HTML avec BeautifulSoup
soup = BeautifulSoup(html, "lxml")

print("[1] Accès direct à quelques balises :")
print("soup.title        ->", soup.title)
print("soup.title.string ->", soup.title.string)
print("soup.h1           ->", soup.h1)
print("soup.p            ->", soup.p)
print("-" * 60)

# 2) Affichage "joli" du HTML avec prettify()
print("[2] HTML 'prettifié' avec soup.prettify() :")
print(soup.prettify())
print("-" * 60)


