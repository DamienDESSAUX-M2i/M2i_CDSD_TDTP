import pandas as pd

print("=== Démo 1 : Exploration de données ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame complet ---")
print(df)

# Dimensions
print("\n--- Dimensions (lignes, colonnes) ---")
print(df.shape)

# Premières et dernières lignes
print("\n--- 3 premières lignes ---")
print(df.head(3))

print("\n--- 2 dernières lignes ---")
print(df.tail(2))

# Informations sur les colonnes
print("\n--- Infos du DataFrame ---")
print(df.info())

# Statistiques descriptives
print("\n--- Statistiques descriptives ---")
print(df.describe())

# Noms des colonnes
print("\n--- Noms des colonnes ---")
print(df.columns)

# Types de données
print("\n--- Types de données ---")
print(df.dtypes)

# Valeurs manquantes
print("\n--- Nombre de valeurs manquantes par colonne ---")
print(df.isnull().sum())

# Valeurs uniques
print("\n--- Valeurs uniques de 'ville' ---")
print(df["ville"].unique())
print("\n--- Nombre de villes différentes ---")
print(df["ville"].nunique())
