"""
Démo 17 : Nettoyage de données extraites du HTML

Objectifs :
- Nettoyer les espaces multiples dans une chaîne
- Extraire un prix numérique depuis un texte
- Extraire une note depuis un texte avec pattern
- Supprimer des symboles spécifiques grâce aux regex
"""

from bs4 import BeautifulSoup
import re # https://docs.python.org/fr/3.14/library/re.html

print("=== DÉMO 17 : Nettoyage de données ===")
print("-" * 60)

html = """
<div>
    <p>  Texte avec   espaces  multiples  </p>
    <p>Prix: £51.77</p>
    <p>★★★★☆ (4/5)</p>
</div>
"""

soup = BeautifulSoup(html, "lxml")

# 1) Nettoyer les espaces multiples
print("[1] Nettoyage des espaces multiples :")
text = soup.find("p").get_text(strip=True)
text_clean = " ".join(text.split())
print("Texte brut  :", repr(text))
print("Texte clean :", repr(text_clean))
print("-" * 60)

# 2) Extraire le prix (nombre flottant) depuis le texte
print("[2] Extraction du prix :")
price_text = soup.find_all("p")[1].text
price = float(re.findall(r"[\d.]+", price_text)[0])
print("Texte du prix :", repr(price_text))
print("Prix extrait   :", price)
print("-" * 60)

# 3) Extraire la note (x/5)
print("[3] Extraction de la note :")
rating_text = soup.find_all("p")[2].text
rating = int(re.search(r"(\d)/5", rating_text).group(1))
print("Texte de la note :", repr(rating_text))
print("Note extraite    :", rating, "/5")
print("-" * 60)

# 4) Supprimer symboles (★, ☆, £) du premier texte
print("[4] Suppression de symboles dans le texte :")
clean_text = re.sub(r"[★☆£]", "", text)
print("Texte original :", repr(text))
print("Texte nettoyé  :", repr(clean_text))
print("-" * 60)
