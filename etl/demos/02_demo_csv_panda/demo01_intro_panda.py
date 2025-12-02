import pandas as pd

# Depuis un dictionnaire
data = {
    'nom': ['Dupont', 'Martin', 'Durant'],
    'prenom': ['Jean', 'Marie', 'Pierre'],
    'age': [35, 28, 42],
    'ville': ['Paris', 'Lyon', 'Marseille']
}
df = pd.DataFrame(data)
print(df)
print(type(df))

datas = [12,14,15]

df2 = pd.DataFrame(datas)
print(type(df2))
print(df2)