"""
Démo 05 : Utilisation d'une session requests pour garder les cookies

Objectifs :
- Créer une session HTTP persistante
- Simuler une connexion (login)
- Réutiliser la même session pour plusieurs requêtes

"""

import requests

# Créer une session
session = requests.Session()

# Les cookies et headers sont persistés d'une requête à l'autre
session.headers.update({'User-Agent': 'My Scraper 1.0'})

# Première requête (authentification par exemple)
# Les paramètres username/password sont purement fictifs ici.
response1 = session.post(
    #'https://httpbin.org/post',
    'http://localhost:8080/post',
    data={'username': 'user', 'password': 'pass'}
)

print("Code HTTP de la tentative de login :", response1.status_code)

# Requêtes suivantes gardent les cookies de la session
# response2 = session.get('https://httpbin.org/cookies/set?session_id=12345')
# response3 = session.get('https://httpbin.org/cookies')

response2 = session.get('http://localhost:8080/cookies/set?session_id=12345')
response3 = session.get('http://localhost:8080/cookies')

print("\nCode HTTP /session_id :", response2.status_code)
print("Code HTTP /cookies  :", response3.status_code)

# Voir les cookies stockés dans la session
print("\n=== Cookies de la session ===")
print(session.cookies.get_dict())

# Fermer la session proprement (bonne pratique)
session.close()
