from datetime import datetime
from pathlib import Path

import pandas as pd
from markdown_pdf import MarkdownPdf, Section

file_dir = Path(__file__).parent.resolve()

content: list[str] = []
content.append(f"# Rapport {datetime.today().__format__('%Y-%m-%d %H:%M:%S')}")
content.append("")

# Question 1
path_ventes_csv = file_dir.joinpath("ventes.csv")
df = pd.read_csv(path_ventes_csv)

# Question 2
df["montant_total"] = df["quantite"] * df["prix_unitaire"]
content.append("## Données")
content.append(str(df.to_markdown(index=False)))
content.append("")

# Question 3
total_vendeur = (
    df.groupby("vendeur")["montant_total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"montant_total": "total_ventes"})
)
content.append("## Total des ventes par vendeur")
content.append(str(total_vendeur.to_markdown(index=False)))
content.append("")

# Question 4
total_produit = (
    df.groupby("produit")["montant_total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"montant_total": "total_ventes"})
)
content.append("## Total des ventes par produit")
content.append(str(total_produit.to_markdown(index=False)))
content.append("")

# Question 5
top3_montant_total = df.sort_values("montant_total", ascending=False).head(3)
content.append("## Top 3 des ventes")
content.append(str(top3_montant_total.to_markdown(index=False)))
content.append("")

# Question 6
path_ventes_anelysees_csv = file_dir.joinpath("ventes_analysees.csv")
df.to_csv(path_ventes_anelysees_csv, index=False)

path_report_md = file_dir.joinpath("report.md")
path_report_pdf = file_dir.joinpath("report.pdf")
with open(path_report_md, "wt", encoding="utf-8") as report:
    report.writelines("\n".join(content))

    pdf = MarkdownPdf()
    pdf.meta["title"] = "Report"
    pdf.add_section(Section("\n".join(content), toc=False))
    pdf.save(path_report_pdf)
