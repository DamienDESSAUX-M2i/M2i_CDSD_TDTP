from pathlib import Path

import pandas as pd
import requests
import scipy
import seaborn as sns
from matplotlib import pyplot as plt

DIR_PATH = Path(__file__).parent.resolve()
BASE_URL = "https://restcountries.com/v3.1"

# Question 1
endpoint = "region/europe"
response = requests.get(url="/".join([BASE_URL, endpoint]))
entries = response.json()

# Question 2
data = {"nom": [], "capital": [], "population": [], "superficie": [], "langue": []}
for entry in entries:
    data["nom"].append(entry.get("name").get("official"))
    data["capital"].append(entry.get("capital")[0])
    data["population"].append(entry.get("population", 0))
    data["superficie"].append(entry.get("area", 0))
    data["langue"].append(list(entry.get("languages").values())[0])
df = pd.DataFrame(data=data)

# Question 3
df["densite_population"] = df["population"] / df["superficie"]

# Question 4
top5_most_populated_country = df.nlargest(n=5, columns="population")

# Question 5
total_population = pd.DataFrame(data={"population_total": [df["population"].sum()]})

# Question 6
highest_population_density_country = df.nlargest(n=1, columns="densite_population")

# Bonus 1
top3_language = (
    df.groupby("langue")
    .agg({"population": "sum", "nom": "count"})
    .reset_index()
    .rename(columns={"population": "total_population", "nom": "nombre_pays"})
    .nlargest(n=3, columns="total_population")
)

# Question 7
excel_path = DIR_PATH.joinpath("exo4.xlsx")
with pd.ExcelWriter(excel_path) as writer:
    top5_most_populated_country.to_excel(
        writer, index=False, sheet_name="Top5 Population"
    )

    total_population.to_excel(writer, index=False, sheet_name="Total population")
    highest_population_density_country.to_excel(
        writer, index=False, sheet_name="Plus haute densité"
    )
    top3_language.to_excel(writer, index=False, sheet_name="Top3 langue")

# Bonus 2
plt.figure()
sns.scatterplot(data=df, x="superficie", y="population")
plt.title("Population en fonction de la superficie")
plot_01_path = DIR_PATH.joinpath("exo4_01.png")
plt.savefig(plot_01_path)

df_analyse = df[df["nom"] != "Russian Federation"]
plt.figure()
sns.scatterplot(data=df_analyse, x="superficie", y="population")
plt.title("Population en fonction de la superficie (sans les valeurs aberrantes)")
plot_02_path = DIR_PATH.joinpath("exo4_02.png")
plt.savefig(plot_02_path)

pearson_result, pvalue = scipy.stats.pearsonr(df["superficie"], df["population"])

content = []
content.append("# Analyse bivariée")
content.append("## superficie / population")
content.append(f"![]({plot_01_path.name})")
content.append(
    "On observe une valeur aberrante. Il s'agit de la russie. Dans la suite de l'analyse, on ne considère pas cette valeur."
)
content.append(f"![]({plot_02_path.name})")
content.append(
    f"""
Une corrélation linéaire entre la superficie et la population ne semble pas évidente.

Le dataset comporte {df.shape[0]} lignes. Le nombre de lignes est raisonnable pour calculer un coefficient de corrélation de *Pearson*.

Coefficient de corrélation de *Pearson* : {pearson_result}.

pvalue test de non-correlation de *Pearson* : {pvalue}.

Le coefficient de corrélation de Pearson est supérieur à 0.5 donc il y a corrélation linéaire entre superficie et population. La pvalue est inférieure à 0.05, ce qui est sinificatif.
"""
)

report_path = DIR_PATH.joinpath("exo4.md")
with open(report_path, "wt", encoding="utf-8") as report:
    report.writelines("\n".join(content))
