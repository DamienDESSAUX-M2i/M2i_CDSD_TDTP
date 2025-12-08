from pathlib import Path

import pandas as pd

file_dir = Path(__file__).parent.resolve()


# Questions 1 et 2
def load_dfs(path_dir: Path) -> list[pd.DataFrame]:
    dfs: list[pd.DataFrame] = []
    file_paths = [path for path in path_dir.glob("magasin_*.csv") if path.is_file()]
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df["magasin"] = file_path.stem.split("_")[1]
        dfs.append(df)
    return dfs


# Question 3
df = pd.concat(load_dfs(file_dir), axis=0)

# Question 4
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna()
df_clean["date"] = pd.to_datetime(df_clean["date"])

# Question 5
df_clean["montant_total"] = df_clean["quantite"] * df_clean["prix_unitaire"]

# Question 6
total_magasin = (
    df_clean.groupby("magasin")["montant_total"]
    .sum()
    .reset_index()
    .rename(columns={"montant_total": "CA"})
    .sort_values("CA")
)

total_vendeur = (
    df_clean.groupby(["magasin", "vendeur"])["montant_total"]
    .sum()
    .reset_index()
    .rename(columns={"montant_total": "total_vendeur"})
    .sort_values("total_vendeur", ascending=False)
)

top_produit = (
    df_clean.groupby("produit")["montant_total"]
    .sum()
    .reset_index()
    .rename(columns={"montant_total": "total_produit"})
    .nlargest(n=10, columns="total_produit")
)

path_output = file_dir.joinpath("tp1.xlsx")
with pd.ExcelWriter(path_output) as writer:
    df_clean.to_excel(writer, index=False, sheet_name="Consolidé")
    total_magasin.to_excel(writer, index=False, sheet_name="Par magasin")
    total_vendeur.to_excel(writer, index=False, sheet_name="Par vendeur")
    top_produit.to_excel(writer, index=False, sheet_name="Top produit")
