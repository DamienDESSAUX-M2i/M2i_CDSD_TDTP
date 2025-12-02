import pandas as pd

print("=== Démo 6 : Écriture CSV avec Pandas ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame de départ ---")
print(df)

# Écriture basique
print("\n--- Écriture basique dans 'output.csv' (sans index) ---")
df.to_csv("output.csv", index=False)

# Avec options
print("\n--- Réécriture de 'output.csv' avec options (colonnes nom, age) ---")
df.to_csv(
    "output.csv",
    sep=",",
    encoding="utf-8",
    index=False,           # Ne pas inclure l'index
    header=True,           # Inclure les en-têtes
    na_rep="NA",           # Représentation des NaN
    columns=["nom", "age"] # Sélectionner des colonnes
)

# Ajouter à un fichier existant
print("\n--- Ajout de lignes à 'output.csv' (mode append, sans header) ---")
df.to_csv("output.csv", mode="a", header=False, index=False)

print("\n=== Fin de la démo écriture CSV ===")
