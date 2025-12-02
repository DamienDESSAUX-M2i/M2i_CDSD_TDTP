import pandas as pd

print("=== Démo 3 : Gestion des valeurs manquantes ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame initial ---")
print(df)

# Détecter les valeurs manquantes
print("\n--- Tableau booléen des valeurs manquantes ---")
print(df.isnull())

print("\n--- Nombre de valeurs manquantes par colonne ---")
print(df.isnull().sum())

# Supprimer les lignes avec valeurs manquantes
print("\n--- dropna() : lignes sans aucun NaN ---")
df_clean_all = df.dropna()
print(df_clean_all)

print("\n--- dropna(subset=['age']) : supprimer si 'age' est NaN ---")
df_clean_age = df.dropna(subset=["age"])
print(df_clean_age)

# Supprimer les colonnes avec trop de valeurs manquantes
print("\n--- dropna(axis=1, thresh=len(df)*0.8) : garder les colonnes avec ≥ 80% de données ---")
df_clean_cols = df.dropna(axis=1, thresh=len(df) * 0.8)
print(df_clean_cols)

# Remplir les valeurs manquantes
print("\n--- Remplissage des NaN dans 'age' par 0 ---")
df_fill = df.copy()
df_fill["age"].fillna(0, inplace=True)
print(df_fill)

print("\n--- Remplissage des NaN dans 'age' par la moyenne ---")
df_fill_mean = df.copy()
df_fill_mean["age"].fillna(df_fill_mean["age"].mean(), inplace=True)
print(df_fill_mean)

print("\n--- Remplissage des NaN dans 'ville' par 'Inconnue' ---")
df_fill_ville = df.copy()
df_fill_ville["ville"].fillna("Inconnue", inplace=True)
print(df_fill_ville)

# Forward fill / Backward fill
print("\n--- ffill sur 'age' (valeur précédente) ---")
df_ffill = df.copy()
df_ffill["age"].fillna(method="ffill", inplace=True)
print(df_ffill)

print("\n--- bfill sur 'age' (valeur suivante) ---")
df_bfill = df.copy()
df_bfill["age"].fillna(method="bfill", inplace=True)
print(df_bfill)
