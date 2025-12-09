"""
Démo 06 : Respecter le site cible avec du rate limiting

Objectifs :
- Envoyer plusieurs requêtes à la suite
- Introduire une pause entre chaque requête
- Montrer l'utilisation de time.sleep et random.uniform
"""

import time
import random
import requests

# Liste d'URLs à scrapper (exemple)
urls = [
    'https://example.com',
    'https://www.iana.org/domains/reserved',
    'https://www.python.org'
]

print("=== Scraping avec pause fixe de 2 secondes ===")
for url in urls:
    response = requests.get(url)
    print(f"Scraped: {url} (code HTTP {response.status_code})")

    # Attendre 2 secondes entre chaque requête
    time.sleep(2)

print("\n=== Scraping avec pause aléatoire entre 1 et 3 secondes ===")
for url in urls:
    response = requests.get(url)
    print(f"Scraped: {url} (code HTTP {response.status_code})")

    delay = random.uniform(1, 3)
    print(f"Pause de {delay:.2f} secondes...")
    time.sleep(delay)
