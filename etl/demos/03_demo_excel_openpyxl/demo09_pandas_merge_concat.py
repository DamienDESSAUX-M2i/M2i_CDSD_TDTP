import pandas as pd

print("=== Démo Pandas - Jointures et fusion ===")

# Deux DataFrames pour la jointure
clients = pd.DataFrame({
    'client_id': [1, 2, 3],
    'nom': ['Alice', 'Bob', 'Charlie']
})

commandes = pd.DataFrame({
    'commande_id': [101, 102, 103],
    'client_id': [1, 1, 2],
    'montant': [100, 150, 200]
})

print("\n--- Table clients ---")
print(clients)

print("\n--- Table commandes ---")
print(commandes)

# Jointure (merge)
print("\n--- Jointure commandes + clients sur 'client_id' (LEFT JOIN) ---")
result = pd.merge(commandes, clients, on='client_id', how='left')
print(result)

# Types de jointure :
# - inner : intersection (par défaut)
# - left : toutes les lignes de gauche
# - right : toutes les lignes de droite
# - outer : union complète

# Pour la concaténation, on crée deux petits DataFrames
df1 = pd.DataFrame({'id': [1, 2], 'val': ['A', 'B']})
df2 = pd.DataFrame({'id': [3, 4], 'val': ['C', 'D']})

print("\n--- df1 ---")
print(df1)
print("\n--- df2 ---")
print(df2)

# Concaténation verticale (lignes empilées)
print("\n--- Concaténation verticale (ignore_index=True) ---")
df_concat_vertical = pd.concat([df1, df2], ignore_index=True)
print(df_concat_vertical)

# Concaténation horizontale (colonnes côte à côte)
print("\n--- Concaténation horizontale (axis=1) ---")
df_concat_horizontal = pd.concat([df1, df2], axis=1)
print(df_concat_horizontal)
