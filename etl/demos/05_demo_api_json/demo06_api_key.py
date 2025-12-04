import requests

API_KEY = "DEMO_API_KEY_123456"  # Clé factice, pour la démonstration uniquement

# 1) API Key dans les paramètres (recommandé)

print("=== 1) API Key dans les paramètres (query string) ===")

params = {
    "apikey": API_KEY,
    "query": "python"
}

response = requests.get("https://httpbin.org/get", params=params)
response.raise_for_status()

data = response.json()

print("URL appelée :", data["url"])
print("Paramètres vus par le serveur (data['args']) :", data["args"])
print()

# 2) API Key dans les headers


print("=== 2) API Key dans les headers ===")

headers = {
    "X-API-Key": API_KEY
}


response = requests.get("https://httpbin.org/get", headers=headers)
response.raise_for_status()

data = response.json()

print("Headers vus par le serveur (data['headers']) :")
for name, value in data["headers"].items():
    if name.lower() == "x-api-key".lower():
        print(f"{name}: {value}")


# 3) API Key directement dans l’URL (DÉCONSEILLÉ)
# → visible dans l’historique, les logs, etc.

print("=== 3) API Key directement dans l'URL (déconseillé) ===")

url = f"https://httpbin.org/get?apikey={API_KEY}&query=python"

response = requests.get(url)
response.raise_for_status()

data = response.json()

print("URL appelée :", data["url"])
print("Paramètres vus par le serveur (data['args']) :", data["args"])
print()

# Remarque :
# Pour une "vraie" API (OpenWeatherMap, etc.), la logique est identique,
# seule l'URL change, et la clé doit être réelle.