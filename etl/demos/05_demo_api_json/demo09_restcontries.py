import requests

#Tous les pays

response = requests.get("https://restcountries.com/v3.1/all?fields=name")
pays = response.json()

print("Nombre de pays :", len(pays))


# Un pays spécifique (France)

response = requests.get("https://restcountries.com/v3.1/name/france")
france = response.json()[0]

print("Capitale :", france['capital'][0])
print("Population :", f"{france['population']:,}")
print("Région :", france['region'])


# Par code (ex : FR)
response = requests.get("https://restcountries.com/v3.1/alpha/fr")

print(response.json())

# Filtrer la réponse pour obtenir uniquement certains champs

response = requests.get(
    "https://restcountries.com/v3.1/all?fields=name,capital,population"
)


print(response.json())