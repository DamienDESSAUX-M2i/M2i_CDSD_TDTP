import matplotlib.pyplot as plt
import scipy.stats as stats

import numpy as np

# Charger le csv
data = np.genfromtxt(
    "./ventes_mensuelles.csv", delimiter=",", skip_header=1, usecols=(1, 2, 3)
)

articles_vendus = data[:, 0].astype(int)
prix_moyen = data[:, 1].astype(float)
chiffre_affaires = data[:, 2].astype(float)

mois = np.genfromtxt(
    "./ventes_mensuelles.csv", delimiter=",", skip_header=1, usecols=0, dtype=str
)

# Calculer à l'aide de numpy
# Les total des ventes de l'année
print("Total des ventes de l'année : ", articles_vendus.sum())

# Le chiffre d'affaire total
print("Chiffre d'affaire total : ", chiffre_affaires.sum())

# Le mois avec le plus chiffre d'affaire
print("Mois avec le plus grand chiffre d'affaire : ", mois[np.argmax(chiffre_affaires)])

# La moyenne des prix
print("Moyenne des prix moyens : ", prix_moyen.mean())
print(
    "Moyenne des prix : ",
    np.sum(prix_moyen * articles_vendus) / np.sum(articles_vendus),
)

# Bonus : La corrélation entre articles vendus et le chiffre d'affaire
print(
    "Corrélation entre articles vendus et chiffre d'affaire : ",
    np.corrcoef(articles_vendus, chiffre_affaires)[0, 1],
)

r, p = stats.pearsonr(articles_vendus, chiffre_affaires)
print(f"Pearson correlation:\{r = } - {p = }")

fig, ax = plt.subplots()
ax.scatter(articles_vendus, chiffre_affaires)
a, b = np.polyfit(articles_vendus, chiffre_affaires, deg=1)
xseq = np.linspace(articles_vendus.min(), articles_vendus.max(), num=100)
ax.plot(xseq, a * xseq + b, color="k", lw=1)
plt.show()
