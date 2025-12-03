from pathlib import Path

import pandas as pd

file_dir = Path(__file__).parent.resolve()

# Question 1
path_file_xlsx = file_dir.joinpath("ventes_janvier.xlsx")
df = pd.read_excel(path_file_xlsx)

# Question 2
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean["region"] = df_clean["region"].fillna("Non spécifié")
df_clean["date"] = pd.to_datetime(df_clean["date"])
df_clean["date_YYYYMMdd"] = df_clean["date"].dt.date

# Question 3
df_clean["montant_total"] = df_clean["quantite"] * df_clean["prix_unitaire"]
df_clean["annee"] = df_clean["date"].dt.year
df_clean["mois"] = df_clean["date"].dt.month
df_clean["jour"] = df_clean["date"].dt.day
df_clean["jour_semaine"] = df_clean["date"].dt.day_name(locale="fr_FR")

# Question 4
total_region = (
    df_clean.groupby("region")["montant_total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"montant_total": "total_ventes"})
)
print(total_region)

best_selling_product = df_clean.nlargest(n=1, columns="quantite")
print(best_selling_product)

nb_sell_per_day = (
    df_clean.groupby("jour_semaine")["quantite"]
    .sum()
    .reset_index()
    .rename(columns={"quantite": "total_quantite"})
    .nlargest(n=1, columns="total_quantite")
)
print(nb_sell_per_day)

path_output = file_dir.joinpath("exo2.xlsx")
with pd.ExcelWriter(path_output) as writer:
    df.to_excel(writer, index=False, sheet_name="Données")
    df_clean.to_excel(writer, index=False, sheet_name="Données nettoyées")
    total_region.to_excel(writer, index=False, sheet_name="Par région")
    best_selling_product.to_excel(writer, index=False, sheet_name="Par produit")
