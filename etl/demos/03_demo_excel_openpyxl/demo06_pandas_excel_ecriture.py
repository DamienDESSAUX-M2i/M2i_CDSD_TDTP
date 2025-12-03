import pandas as pd

print("=== Démo Pandas - Écriture Excel ===")

# DataFrame exemple
df = pd.DataFrame({
    'Produit': ['Laptop', 'Souris', 'Clavier'],
    'Quantité': [5, 10, 3],
    'Prix': [899.99, 29.99, 79.99]
})

print("\nDataFrame de départ :")
print(df)

# Écriture basique dans un fichier Excel
print("\n--- Écriture basique dans 'output_pandas.xlsx' ---")
df.to_excel('output_pandas.xlsx', index=False)

# Exemple de deuxième DataFrame pour la feuille 'Stocks'
df2 = pd.DataFrame({
    'Produit': ['Laptop', 'Souris', 'Clavier', 'Écran'],
    'Stock': [10, 50, 20, 5]
})

# Plusieurs feuilles dans le même fichier
print("\n--- Écriture dans plusieurs feuilles (multi_sheets.xlsx) ---")
with pd.ExcelWriter('multi_sheets.xlsx') as writer:
    df.to_excel(writer, sheet_name='Ventes', index=False)
    df2.to_excel(writer, sheet_name='Stocks', index=False)

# Avec formatage de colonnes via openpyxl
print("\n--- Écriture avec formatage dans 'formatted_pandas.xlsx' ---")
with pd.ExcelWriter('formatted_pandas.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    
    # Accéder au classeur et à la feuille créée
    workbook = writer.book
    worksheet = writer.sheets['Data']
    
    # Modifier la largeur de la colonne A (Produit)
    worksheet.column_dimensions['A'].width = 20
    

print("Fichiers Excel écrits avec Pandas : output_pandas.xlsx, multi_sheets.xlsx, formatted_pandas.xlsx")
