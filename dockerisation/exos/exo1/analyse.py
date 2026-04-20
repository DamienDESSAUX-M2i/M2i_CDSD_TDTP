import sys

import pandas as pd

# Récupérer le fichier depuis les arguments ou utiliser data.csv par défaut
fichier = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
df = pd.read_csv(fichier)

# Calculer le montant total
df["montant_total"] = df["quantite"] * df["prix_unitaire"]

# Afficher les statistiques
print(f"Nombre total de transactions: {len(df)}")
print(f"Chiffre d'affaires total: {df['montant_total'].sum()}€")
print("Produit le plus vendu:")
print(df.groupby("produit")["quantite"].sum().sort_values(ascending=False).head(1))
print("Produit le plus rentable:")
print(df.groupby("produit")["montant_total"].sum().sort_values(ascending=False).head(1))
