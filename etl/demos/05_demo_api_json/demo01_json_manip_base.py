import json  # Bibliothèque standard Python pour manipuler le JSON (pas besoin d'installation)

# -----------------------------------------------------------------------------
# - Convertir une chaîne JSON (format texte) en dictionnaire Python
# - Convertir un dictionnaire Python en JSON
# - Indenter un JSON pour le rendre lisible
# - Lire un fichier JSON → dict
# - Écrire un dict → fichier JSON
# -----------------------------------------------------------------------------


# 1) JSON STRING → PYTHON DICT

# Chaîne JSON valide (format texte, comme envoyé par une API)
json_string = '{"nom": "Dupont", "age": 30}'
print(type(json_string))
# json.loads(...) analyse la chaîne JSON et renvoie un objet Python
# Généralement un dict (pour un objet JSON) ou une list (pour un tableau JSON)
data = json.loads(json_string)
print(type(data))

print("Nom issu du JSON :", data['nom'])  # Accès comme un dictionnaire Python

# 2) PYTHON DICT → JSON STRING

# Dictionnaire Python classique
data = {'nom': 'Martin', 'age': 25}

# json.dumps(...) transforme un dict en chaîne JSON
json_string = json.dumps(data)
print(type(json_string))

print("JSON généré :", json_string)  # Chaîne JSON compacte

# 3) JSON avec indentation (plus lisible pour l'humain)

# indent=2 ajoute 2 espaces d'indentation → JSON formaté
json_string_pretty = json.dumps(data, indent=2)
print("JSON indenté :\n", json_string_pretty)

# 4) Lire un fichier JSON → dict Python

# json.load(...) lit directement le JSON depuis un fichier ouvert.
# Le fichier doit contenir un JSON valide.
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)

# data est maintenant un dict Python utilisable

# 5) Écrire un dict Python → fichier JSON

# json.dump(...) écrit du JSON dans un fichier.
# indent=2 rend le fichier plus lisible.
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)