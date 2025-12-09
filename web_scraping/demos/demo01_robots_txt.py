"""
Démo 01 : Lecture et interprétation de robots.txt

Objectifs :
- Télécharger le fichier robots.txt d'un site
- L'afficher dans la console
- Tester si un chemin est autorisé pour un user-agent donné
"""

import requests
from urllib.robotparser import RobotFileParser

# IMPORTANT :
# Changez cette URL par un site que vous avez le droit de scraper
BASE_URL = "https://www.python.org"
ROBOTS_URL = f"{BASE_URL}/robots.txt"

def afficher_robots_txt():
    """Télécharge et affiche le contenu de robots.txt."""
    print(f"Récupération de {ROBOTS_URL} ...")
    response = requests.get(ROBOTS_URL)

    # Status HTTP (200 = OK, 404 = non trouvé, etc.)
    print("Code HTTP :", response.status_code)

    # Affichage brut du fichier robots.txt
    print("\n=== Contenu de robots.txt ===")
    print(response.text)

def tester_acces():
    """
    Utilise urllib.robotparser pour savoir si un chemin
    est autorisé pour un user-agent donné.
    """
    rp = RobotFileParser()
    rp.set_url(ROBOTS_URL)

    # Télécharge et analyse robots.txt
    rp.read()

    # Exemple de chemins à tester
    path_autorise = f"{BASE_URL}/"
    path_potentiellement_interdit = f"{BASE_URL}/admin/"

    # Test avec un user-agent générique "*"
    print("\n=== Vérification des droits d'accès ===")
    print(f"Peut-on accéder à {path_autorise} ?",
          rp.can_fetch("*", path_autorise))
    print(f"Peut-on accéder à {path_potentiellement_interdit} ?",
          rp.can_fetch("*", path_potentiellement_interdit))
    
if __name__ == "__main__":
    afficher_robots_txt()
    tester_acces()