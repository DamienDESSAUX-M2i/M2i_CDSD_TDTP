"""
Démo 15 : Extraction de liens sur une page

Objectifs :
- Récupérer tous les liens <a> d'une page
- Extraire les href
- Distinguer liens internes et externes
- Construire des URLs absolues et supprimer les doublons
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

print("=== DÉMO 15 : Extraction de liens ===")
print("-" * 60)

# Site de démonstration pour le scraping (site de test)
url = "http://quotes.toscrape.com"
print("URL cible :", url)
print("-" * 60)

# 1) Récupération de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# 2) Tous les liens <a>
all_links = soup.find_all("a")

print("[1] Nombre total de balises <a> trouvées :", len(all_links))
print("-" * 60)

# 3) Extraire les href non nuls
hrefs = [link.get("href") for link in all_links if link.get("href")]

print("[2] Exemple de quelques href extraits :")
for h in hrefs[:10]:
    print(" ", h)
print("-" * 60)

# 4) Fonction utilitaire pour savoir si un lien est externe
def is_external(link, base_domain):
    return urlparse(link).netloc and urlparse(link).netloc != base_domain

base_domain = urlparse(url).netloc

# Liens externes parmi les href (tels quels)
external_links = [link for link in hrefs if is_external(link, base_domain)]

# 5) Construire des URLs absolues à partir des href (internes ou relatifs)
absolute_links = [urljoin(url, href) for href in hrefs]

# 6) Supprimer les doublons
unique_links = list(set(absolute_links))

print("[3] Statistiques :")
print(f"Total liens (balises <a>)      : {len(all_links)}")
print(f"Liens externes (sur href bruts) : {len(external_links)}")
print(f"Liens uniques (absolus)        : {len(unique_links)}")
print("-" * 60)

print("[4] Exemple de quelques liens absolus uniques :")
for link in unique_links[:10]:
    print(" ", link)
print("-" * 60)
