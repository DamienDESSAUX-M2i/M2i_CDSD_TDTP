import pandas as pd

print("=== Démo Pandas - Transformation de données ===")

# DataFrame de base pour la démo
df = pd.DataFrame({
    'prenom': ['Jean', 'Marie', 'Paul', 'Luc'],
    'nom': ['Dupont', 'Martin', 'Noir', 'Durant'],
    'age': [15, 30, 70, 45],
    'date': ['2024-01-10', '2023-12-05', '2020-07-20', '2019-03-15'],
    'adresse': [
        '10 rue de Paris,Paris',
        '5 avenue de Lyon,Lyon',
        '3 impasse du Port,Marseille',
        '8 boulevard Sud,Lille'
    ]
})

print("\n--- DataFrame initial ---")
print(df)

# Conversion de types
print("\n--- Conversion des types ---")
df['age'] = df['age'].astype(int)
df['date'] = pd.to_datetime(df['date'])
print(df.dtypes)

# Extraction depuis les dates
print("\n--- Extraction (année, mois, jour_semaine) depuis 'date' ---")
df['annee'] = df['date'].dt.year
df['mois'] = df['date'].dt.month
df['jour_semaine'] = df['date'].dt.dayofweek
print(df[['date', 'annee', 'mois', 'jour_semaine']])

# Manipulation de chaînes
print("\n--- Création de 'nom_complet' et 'initiales' ---")
df['nom_complet'] = df['prenom'] + ' ' + df['nom']
df['initiales'] = df['nom'].str[0] + df['prenom'].str[0]
print(df[['prenom', 'nom', 'nom_complet', 'initiales']])

# Découper une chaîne (adresse => rue + ville)
print("\n--- Découpage de la colonne 'adresse' en 'rue' et 'ville' ---")
df[['rue', 'ville']] = df['adresse'].str.split(',', expand=True)
print(df[['adresse', 'rue', 'ville']])

# Apply - fonction personnalisée
print("\n--- Catégorisation des âges ---")
def categoriser_age(age):
    if age < 18:
        return 'Mineur'
    elif age < 65:
        return 'Adulte'
    else:
        return 'Senior'

df['categorie'] = df['age'].apply(categoriser_age)
print(df[['age', 'categorie']])
