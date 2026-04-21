import requests
import sys
import time

def call_server(server_url):
    print(f"Tentative de connexion à {server_url}")

    try:
        response = requests.get(server_url, timeout=5)
        print(f"Succès! Status: {response.status_code}")
        print(f"Réponse:\n{response.text}")
        return True
    except Exception as e:
        print(f"Erreur: {e}")
        return False

if __name__ == '__main__':
    server_url = sys.argv[1] if len(sys.argv) > 1 else 'http://server:8000'

    # Attendre un peu que le serveur démarre
    time.sleep(2)

    # Essayer de se connecter
    success = call_server(server_url)
    sys.exit(0 if success else 1)