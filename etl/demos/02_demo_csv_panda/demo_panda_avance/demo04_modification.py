import pandas as pd

print("=== Démo 4 : Modification de données ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame de départ ---")
print(df)

# Ajouter une colonne
print("\n--- Ajout de colonnes 'pays' et 'age_plus_10' ---")
df["pays"] = "France"
df["age_plus_10"] = df["age"] + 10
print(df)

# Modifier une colonne
print("\n--- Modification de 'age' (age + 1) ---")
df["age"] = df["age"] + 1
print(df)

# Renommer des colonnes
print("\n--- Renommage de 'nom' en 'nom_famille' ---")
df = df.rename(columns={"nom": "nom_famille", "prenom": "prenom"})
print(df)

# Supprimer des colonnes
print("\n--- Suppression de 'age_plus_10' ---")
df = df.drop(columns=["age_plus_10"])

# Pour illustrer la suppression de plusieurs colonnes
df["colonne1"] = "temp1"
df["colonne2"] = "temp2"

print("\n--- Avant suppression de colonne1 / colonne2 ---")
print(df)

df = df.drop(["colonne1", "colonne2"], axis=1)
print("\n--- Après suppression de colonne1 / colonne2 ---")
print(df)

# Supprimer des lignes
print("\n--- Suppression des lignes d'index 0 et 1 ---")
df = df.drop([0, 1])
print(df)

print("\n--- Filtrage des lignes avec age > 20 ---")
df = df[df["age"] > 20]
print(df)

# Remplacer des valeurs
print("\n--- Remplacement 'Paris' par 'Paris 75' dans 'ville' ---")
df["ville"] = df["ville"].replace("Paris", "Paris 75")
print(df)

print("\n--- Remplacement plus complet via df.replace ---")
df = df.replace({"ville": {"Paris": "Paris 75", "Lyon": "Lyon 69"}})
print(df)
