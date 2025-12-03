import pandas as pd

print("=== Démo Pandas - Nettoyage de données ===")

# DataFrame avec quelques problèmes :
# - valeurs manquantes
# - doublons
# - espaces parasites
df = pd.DataFrame({
    'nom': [' Dupont ', 'Martin', 'Dupont ', 'Durant'],
    'email': ['dupont@example.com', 'martin@example.com', 'dupont@example.com', None],
    'ville': ['Paris', None, 'Lyon', ' Lille '],
    'age': [35, None, 35, 42]
})

print("\n--- DataFrame initial ---")
print(df)

# 1. Valeurs manquantes
print("\n--- Remplacer les valeurs manquantes par 0 (fillna(0)) ---")
print(df.fillna(0))  # Remplacer par 0

print("\n--- Supprimer les lignes avec au moins une valeur manquante (dropna()) ---")
print(df.dropna())   # Supprimer les lignes

# 2. Doublons
print("\n--- Suppression des doublons sur toutes les colonnes (drop_duplicates()) ---")
print(df.drop_duplicates())

print("\n--- Suppression des doublons basés uniquement sur la colonne 'email' ---")
print(df.drop_duplicates(subset=['email']))

# 3. Espaces inutiles
print("\n--- Suppression des espaces en début/fin de 'nom' ---")
df_nom_clean = df.copy()
df_nom_clean['nom'] = df_nom_clean['nom'].str.strip()
print(df_nom_clean)

# 4. Casse (majuscule/minuscule)
print("\n--- 'ville' en MAJUSCULES ---")
print(df['ville'].str.upper())

print("\n--- 'email' en minuscules ---")
print(df['email'].str.lower())
