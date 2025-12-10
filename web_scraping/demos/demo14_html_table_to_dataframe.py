"""
Démo 14 : Traitement de tableaux HTML

Objectifs :
- Extraire un tableau HTML avec BeautifulSoup
- Construire manuellement une liste de lignes
- Convertir ces données en DataFrame Pandas
- Utiliser pd.read_html comme alternative plus simple
"""

from bs4 import BeautifulSoup
import pandas as pd

print("=== DÉMO 14 : Traitement de tableaux HTML ===")
print("-" * 60)

html = """
<table class="data">
    <thead>
        <tr>
            <th>Nom</th>
            <th>Age</th>
            <th>Ville</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Alice</td>
            <td>25</td>
            <td>Paris</td>
        </tr>
        <tr>
            <td>Bob</td>
            <td>30</td>
            <td>Lyon</td>
        </tr>
    </tbody>
</table>
"""

soup = BeautifulSoup(html, "lxml")

# 1) Récupérer le tableau par sa classe
print("[1] Récupération du tableau <table class='data'> :")
table = soup.find("table", class_="data")
print(table)
print("-" * 60)

# 2) Méthode 1 : extraction manuelle
print("[2] Extraction manuelle des données :")

# Headers (noms de colonnes)
headers = [th.text for th in table.find("thead").find_all("th")]
print("En-têtes de colonnes :", headers)

# Lignes de données
rows = []
for tr in table.find("tbody").find_all("tr"):
    row = [td.text for td in tr.find_all("td")]
    rows.append(row)

print("Lignes extraites :")
for r in rows:
    print(" ", r)
print("-" * 60)

# Création d'un DataFrame à partir des données extraites
df_manual = pd.DataFrame(rows, columns=headers)
print("[3] DataFrame construit manuellement :")
print(df_manual)
print("-" * 60)

# 3) Méthode 2 : utilisation de pd.read_html
print("[4] DataFrame obtenu avec pd.read_html :")
df_auto = pd.read_html(str(table))[0]
print(df_auto)
print("-" * 60)
