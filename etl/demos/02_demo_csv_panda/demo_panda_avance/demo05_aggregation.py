import pandas as pd

print("=== Démo 5 : Tri et agrégation ===")

df = pd.read_csv("data.csv")

print("\n--- DataFrame de départ ---")
print(df)

# Tri
print("\n--- Tri croissant sur 'age' ---")
df_sorted = df.sort_values("age")
print(df_sorted)

print("\n--- Tri décroissant sur 'age' ---")
df_sorted = df.sort_values("age", ascending=False)
print(df_sorted)

print("\n--- Tri par 'ville' puis par 'age' ---")
df_sorted = df.sort_values(["ville", "age"])
print(df_sorted)

# Agrégation simple
print("\n--- Moyenne des âges ---")
moyenne_age = df["age"].mean()
print(moyenne_age)

print("\n--- Somme des âges ---")
total = df["age"].sum()
print(total)

print("\n--- Min / Max / Mean des âges ---")
min_max = df["age"].agg(["min", "max", "mean"])
print(min_max)

# Groupby
print("\n--- Âge moyen par ville (groupby) ---")
par_ville = df.groupby("ville")["age"].mean()
print(par_ville)

# Agrégations multiples
print("\n--- Stats groupées par ville ---")
stats = df.groupby("ville").agg({
    "age": ["mean", "min", "max"],
    "nom": "count"
})
print(stats)
