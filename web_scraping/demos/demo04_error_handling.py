"""
Démo 04 : Gestion des erreurs HTTP et réseau avec requests

Objectifs :
- Encapsuler une requête dans une fonction robuste
- Gérer les erreurs de timeout, connexion, HTTP 4xx/5xx
- Retourner None en cas d'erreur
"""

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

# On réutilise des headers proches de ceux vus précédemment
headers = {
    'User-Agent': 'My Scraper 1.0',
}


def fetch_page(url, timeout=10):
    """Récupère une page avec gestion d'erreurs."""
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout
        )
        # Lève une exception si le code HTTP est 4xx ou 5xx
        response.raise_for_status()
        return response.text

    except Timeout:
        print(f"Timeout pour {url}")
        return None

    except ConnectionError:
        print(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        print(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        print(f"Erreur générale: {e}")
        return None


if __name__ == "__main__":
    # URL valide
    url_ok = "https://www.wikipedia.org"
    # URL volontairement incorrecte pour déclencher une erreur
    url_invalide = "https://domaine_qui_n_existe_pas_du_tout.xyz"

    print("=== Test avec une URL valide ===")
    html_ok = fetch_page(url_ok)
    if html_ok:
        print("La page valide a bien été récupérée (longueur) :", len(html_ok))

    print("\n=== Test avec une URL invalide ===")
    html_ko = fetch_page(url_invalide)
    if html_ko is None:
        print("Aucune page récupérée, comme prévu.")
