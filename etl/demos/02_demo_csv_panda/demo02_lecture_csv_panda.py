import pandas as pd

print("=== Lecture basique ===")
# Lecture basique (sans options)
# Cela charge simplement tout le fichier CSV en laissant Pandas deviner :
# - les types (int, float, string…)
# - les valeurs manquantes
# - les dates non converties automatiquement
df = pd.read_csv('data.csv')

# Afficher les 3 premières lignes pour vérifier le chargement
print(df.head(3))

print("=== Lecture avec options ===")
# Lecture avancée avec options personnalisées
df = pd.read_csv(
    'data.csv',
    sep=',',              # Séparateur utilisé dans le fichier CSV
    encoding='utf-8',     # Encodage du fichier
    na_values=['NA', ''], # Interpréter 'NA' et '' comme valeurs manquantes
    parse_dates=['date'], # Convertir la colonne 'date' en datetime
    dtype={'age': int},   # Forcer la colonne 'age' à être un entier
    nrows=1000            # Lire au maximum les 1000 premières lignes
)


# Vérifier le DataFrame obtenu avec les options
print(df.head())

print("=== Informations sur le DataFrame ===")
# Affiche :
# - le nombre de lignes/colonnes
# - les types des colonnes
# - les valeurs non-nulles
# - l'usage mémoire
print(df.info())