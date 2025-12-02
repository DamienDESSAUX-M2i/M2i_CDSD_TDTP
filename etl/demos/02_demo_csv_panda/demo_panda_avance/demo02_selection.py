import pandas as pd

print("=== Démo 2 : Sélection de données ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame de départ ---")
print(df)

# Sélectionner une colonne
print("\n--- Colonne 'age' ---")
ages = df["age"]
print(ages)

print("\n--- Colonne 'ville' (notation pointée) ---")
villes = df.ville
print(villes)

# Sélectionner plusieurs colonnes
print("\n--- Sous-ensemble (nom, age) ---")
subset = df[["nom", "age"]]
print(subset)

# Sélectionner des lignes par index
print("\n--- Première ligne (iloc[0]) ---")
premiere_ligne = df.iloc[0]
print(premiere_ligne)

print("\n--- Lignes 0 à 4 (iloc[0:5]) ---")
lignes_0_a_4 = df.iloc[0:5]
print(lignes_0_a_4)

# Sélectionner par label
print("\n--- DataFrame avec index = 'nom' ---")
df_with_index = df.set_index("nom")
print(df_with_index)

print("\n--- Ligne pour 'Dupont' avec loc['Dupont'] ---")
jean = df_with_index.loc["Dupont"]
print(jean)

# Filtrage avec conditions
print("\n--- Adultes (age >= 18) ---")
adultes = df[df["age"] >= 18]
print(adultes)

print("\n--- Parisiens (ville == 'Paris') ---")
parisiens = df[df["ville"] == "Paris"]
print(parisiens)

print("\n--- Jeunes parisiens (age < 30 et ville == 'Paris') ---")
jeunes_parisiens = df[(df["age"] < 30) & (df["ville"] == "Paris")]
print(jeunes_parisiens)

# Plusieurs conditions
print("\n--- 25 < age < 40 et ville dans [Paris, Lyon] ---")
condition = (df["age"] > 25) & (df["age"] < 40) & (df["ville"].isin(["Paris", "Lyon"]))
resultat = df[condition]
print(resultat)
