import pandas as pd

print("=== Démo Pandas - Lecture Excel ===")

# Lire la première feuille (par défaut, généralement 'Feuil1')
print("\n--- Lecture de la première feuille (par défaut) ---")
df = pd.read_excel('data.xlsx')
print(df)

# Lire une feuille spécifique : 'Ventes'
print("\n--- Lecture de la feuille 'Ventes' ---")
df_ventes = pd.read_excel('data.xlsx', sheet_name='Ventes')
print(df_ventes)

# Lire plusieurs feuilles à la fois
print("\n--- Lecture de toutes les feuilles dans un dictionnaire ---")
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)  # Dictionnaire {nom_feuille: DataFrame}
print("Feuilles lues :", list(all_sheets.keys()))

df1 = all_sheets['Feuil1']
df2 = all_sheets['Feuil2']

print("\nContenu de 'Feuil1' :")
print(df1)

print("\nContenu de 'Feuil2' :")
print(df2)

# Avec options plus avancées sur une feuille
print("\n--- Lecture de la feuille 'Ventes' avec options ---")
df_options = pd.read_excel(
    'data.xlsx',
    sheet_name='Ventes',
    header=0,              # Ligne d'en-tête (0 = première ligne)
    skiprows=0,            # Exemple : ici on n'ignore aucune ligne
    usecols='A:D',         # Colonnes à lire (A à D)
    nrows=100              # Limiter le nombre de lignes lues
)
print(df_options)
