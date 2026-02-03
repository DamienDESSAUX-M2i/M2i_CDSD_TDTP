import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from matplotlib.axes import Axes
from scipy import stats
from scipy.stats import pearsonr, shapiro, spearmanr, zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

import numpy as np

# Parametrage graphique
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

warnings.filterwarnings("ignore")

np.random.seed(42)

n = 500

facteur_cuisine = np.random.normal(6, 1.5, n)

print(
    f"Facteur CUISINE créé : moyenne={facteur_cuisine.mean():.2f}, écart-type={facteur_cuisine.std():.2f}"
)

facteur_service = np.random.normal(6.5, 1.2, n)

print(
    f"Facteur SERVICE créé : moyenne={facteur_service.mean():.2f}, écart-type={facteur_service.std():.2f}"
)

facteur_ambiance = np.random.normal(7, 1.3, n)

print(
    f"Facteur AMBIANCE créé : moyenne={facteur_ambiance.mean():.2f}, écart-type={facteur_ambiance.std():.2f}"
)

## Creation groupe de variables :

# Variables rattaché au facteur cuisine
qualite_nourriture = facteur_cuisine * 1.0 + np.random.normal(0, 0.8, n)
presentation_plats = facteur_cuisine * 0.9 + np.random.normal(0, 1.0, n)
fraicheur_ingredients = facteur_cuisine * 0.85 + np.random.normal(0, 0.9, n)

# vattaché au facteur service :
rapidite_service = facteur_service * 1.0 + np.random.normal(0, 0.7, n)
amabilite_personnel = facteur_service * 0.95 + np.random.normal(0, 0.8, n)
competence_serveur = facteur_service * 0.9 + np.random.normal(0, 0.9, n)

# Variables rattaché au facteur ambiance
proprete_restaurant = facteur_ambiance * 1.0 + np.random.normal(0, 0.6, n)
ambiance = facteur_ambiance * 0.9 + np.random.normal(0, 1.0, n)
confort_siege = facteur_ambiance * 0.8 + np.random.normal(0, 1.1, n)

# Variables rattaché à aucun facteur
rapport_qualite_prix = np.random.normal(6, 1.5, n)

# Satisfaction globale
satisfaction_globale = (
    0.4 * facteur_cuisine
    + 0.35 * facteur_service
    + 0.15 * facteur_ambiance
    + 0.10 * rapport_qualite_prix
    + np.random.normal(0, 0.5, n)
)

# Création du DataFrame
df = pd.DataFrame(
    {
        "qualite_nourriture": qualite_nourriture,
        "presentation_plats": presentation_plats,
        "fraicheur_ingredients": fraicheur_ingredients,
        "rapidite_service": rapidite_service,
        "amabilite_personnel": amabilite_personnel,
        "competence_serveur": competence_serveur,
        "proprete_restaurant": proprete_restaurant,
        "ambiance": ambiance,
        "confort_siege": confort_siege,
        "rapport_qualite_prix": rapport_qualite_prix,
        "satisfaction_globale": satisfaction_globale,
    }
)

print(f"DataFrame créé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

# Borner les valeurs
for col in df.columns:
    df[col] = df[col].clip(1, 10)

# Ajoute de valeurs manquantes et d'outliers
df.loc[10, "qualite_nourriture"] = np.nan
df.loc[25, "rapidite_service"] = np.nan
df.loc[42, "ambiance"] = np.nan
df.loc[100, "presentation_plats"] = 1.5
df.loc[200, "amabilite_personnel"] = 10

print(df.head(10))

print(f"\nListe des varialbes : {list(df.columns)}")

print(f"\nDonnées générées : {len(df)} clients, {len(df.columns)} variables")


# Step 1 : Nettoyage des données
## NaN
na_count = df.isnull().sum()
na_total = na_count.sum()
print(f"\nNombre total de valeurs manquantes : {na_total}")

for col in df.columns:
    nb_na = df[col].isnull().sum()

    if nb_na > 0:
        mediane = df[col].median()
        df[col].fillna(mediane, inplace=True)
        print(f"{col} : {nb_na} NaN remplacés par la médiane {mediane}")

print(f"\nAprès imputation : {df.isnull().sum().sum()} valeurs manquantes")


## Outliers
def detecter_outliers_iqr(serie: pd.Series, nom_variable: str):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    borne_inf = q1 - 1.5 * iqr
    borne_sup = q3 + 1.5 * iqr
    outliers = (serie < borne_inf) | (serie > borne_sup)
    n_outliers = outliers.sum()
    indices_outliers = serie[outliers].index.to_list()
    return n_outliers, indices_outliers, borne_inf, borne_sup


outliers_total = 0
for col in df.columns:
    n_out, indices, bi, bs = detecter_outliers_iqr(df[col], col)
    outliers_total += n_out

    if n_out:
        print(f"{col:<30} | {n_out:>8} | {bi:>12.2f} | {bs:>12.2f}")

## Doublons
n_doublons = df.duplicated().sum()
print(f"\nNombre de doublons : {n_doublons}")

if n_doublons:
    df = df.drop_duplicates()
    print(f"Doublons supprimés - Nouveau nombre de lignes {len(df)}")
else:
    print("Aucun doublon détecté")


# Step 2 :
## Séparation variables explicatives et cible(s)
variables_X = [col for col in df.columns if col != "satisfaction_globale"]
variables_Y = "satisfaction_globale"

print(f"\nVariables explicatives (X) : {len(variables_X)} variables")
print(f"{variables_X}")
print(f"\nVariable cible (Y) : {variables_Y}")

X = df[variables_X].copy()
Y = df[variables_Y].copy()

## Normalisation
scaler = StandardScaler()
X_scaled_array = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled_array, columns=X.columns, index=X.index)

print("\nParamètres calculés par le scaller :")
print(f"  Moyennes de chaque colonnes : {scaler.mean_}")
print(f"  Ecart-type de chaque colonnes : {scaler.var_}")

print("\nAVANT standardisation :")
print(f"  Moyennes : de {X.mean().min():.2f} à {X.mean().max():.2f}")
print(f"  Écarts-types : de {X.std().min():.2f} à {X.std().max():.2f}")

print("\nAPRÈS standardisation :")
print(f"  Moyennes : {X_scaled.mean().round(6).tolist()}")
print(f"  Écarts-types : {X_scaled.std().round(6).tolist()}")

# Step 3 : Annalyse des corrélations
## Corrélations variables X
corr_matrix = X.corr(method="pearson")


def trouver_correleations_fortes(matrice_corr: pd.DataFrame, seuil: float = 0.5):
    paires = []
    cols = matrice_corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            r = matrice_corr.iloc[i, j]
            if abs(r) >= seuil:
                paires.append(
                    {
                        "Variable_1": cols[i],
                        "Variable_2": cols[j],
                        "Corrélation": round(r, 3),
                    }
                )
    resultats = pd.DataFrame(paires)
    resultats_trie = resultats.sort_values(
        "Corrélation",
        ascending=False,
        key=abs,
    )
    return resultats_trie


correlations_fortes = trouver_correleations_fortes(corr_matrix, seuil=0.5)

print(correlations_fortes.to_string(index=False))

## Corrélations entre X et Y
colonnes_a_garder = variables_X + [variables_Y]

df_complet = df[colonnes_a_garder]

matrice_complete = df_complet.corr()

corr_avec_y = matrice_complete[variables_Y].drop(variables_Y)

corr_avec_y_sorted = corr_avec_y.abs().sort_values(ascending=False)

for var in corr_avec_y_sorted.index:
    r = corr_avec_y[var]
    print(f"{var:30} : r = {r:+.3f}")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

ax1: Axes = axes[0]
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmax=1,
    vmin=-1,
    ax=ax1,
    square=True,
    linewidths=0.5,
)
ax1.set_title("Matrice de corrélation", fontweight="bold")

ax2: Axes = axes[1]
valeurs_triees = corr_avec_y.loc[corr_avec_y_sorted.index]
colors = ["green" if x > 0 else "red" for x in valeurs_triees]
valeurs_triees.plot(kind="barh", ax=ax2, color=colors)
ax2.set_xlabel("Corrélation avec satisfaction")
ax2.set_title("Impact sur la satisfaction", fontweight="bold")

plt.tight_layout()
plt.savefig("etape3_correlations.png", dpi=150)
plt.close()

# Step 4 : ACP
pca = PCA()

try:
    pca.fit(X_scaled)
    print("ACP calculée avec succès")
except ValueError as exception:
    print(f"Erreur : {exception}")
    raise

variance_expliquee = pca.explained_variance_ratio_
variance_cumulee = pca.explained_variance_ratio_.cumsum()
valeurs_propres = pca.explained_variance_

for i, (ve, vc, vp) in enumerate(
    zip(variance_expliquee, variance_cumulee, valeurs_propres), start=1
):
    print(f"PC{i:<3} | {ve * 100:<8.2f} | {vc:<8.2f} | {vp:<8.2f} | {vp > 1}")

# Règle des 80%
n_80pct = (variance_cumulee >= 0.80).argmax() + 1

# Règle de Kaiser
n_kaiser = sum(valeurs_propres > 1)

print(f"\n  RÈGLE DES 80% : {n_80pct} composantes pour ≥80% de variance")
print(f"  RÈGLE DE KAISER : {n_kaiser} composantes avec λ > 1")

n_composantes = max(n_80pct, n_kaiser)
print(
    f"\n  >>> DÉCISION : {n_composantes} composantes ({variance_cumulee[n_composantes - 1] * 100:.1f}% de variance)"
)


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

x = range(1, len(valeurs_propres) + 1)
axes[0].bar(
    x, variance_expliquee * 100, alpha=0.6, color="steelblue", label="Individuelle"
)
axes[0].plot(x, variance_cumulee * 100, "ro-", label="Cumulée")
axes[0].axhline(80, color="green", linestyle="--", label="Seuil 80%")
axes[0].set_xlabel("Composante")
axes[0].set_ylabel("Variance (%)")
axes[0].set_title("Scree Plot", fontweight="bold")
axes[0].legend()

colors = ["green" if lam > 1 else "gray" for lam in valeurs_propres]
axes[1].bar(x, valeurs_propres, color=colors)
axes[1].axhline(1, color="red", linestyle="--", linewidth=2, label="Seuil Kaiser (λ=1)")
axes[1].set_xlabel("Composante")
axes[1].set_ylabel("Valeur propre (λ)")
axes[1].set_title("Critère de Kaiser", fontweight="bold")
axes[1].legend()

plt.tight_layout()
plt.savefig("etape4_acp", dpi=300)
plt.close()

# Step 5 : AF
## KMO
kmo_per_variable, kmo_total = calculate_kmo(X_scaled)
print(f"\n KMO global : {kmo_total:.3f}")
if kmo_total >= 0.9:
    print("Interprétation KMO : Excellent")
elif kmo_total >= 0.8:
    print("Interprétation KMO : Trés bon")
elif kmo_total >= 0.7:
    print("Interprétation KMO : Acceptable")
elif kmo_total >= 0.6:
    print("Interprétation KMO : Médiocre")
else:
    print("Interprétation KMO : Inacceptable")

## Barlett
chi2, p_bartlett = calculate_bartlett_sphericity(X_scaled)
print("\nRésultats Bartlett :")
print(f"  Chi2: {chi2}")
print(f"  p_value: {p_bartlett}")


## Création du modèle factoriel
n_facteur = 4
fa = FactorAnalyzer(n_factors=n_facteur, rotation="varimax", method="principal")
fa.fit_transform(X_scaled)
loadings_fa = pd.DataFrame(
    fa.loadings_,
    columns=[f"Facteur_{i + 1}" for i in range(n_facteur)],
    index=X.columns,
)

print("\n" + loadings_fa.round(3).to_string())

for i in range(n_facteur):
    facteur = f"Facteur_{i + 1}"
    fortes = loadings_fa[facteur][abs(loadings_fa[facteur]) >= 0.4].sort_values(
        key=abs, ascending=False
    )

    print(f"\n  {facteur} :")
    for var, val in fortes.items():
        signe = "+" if val > 0 else "-"
        barre = "█" * int(abs(val) * 10)
        print(f"    {signe} {var:30} {val:+.3f} {barre}")

print("\n--- 5.7 Visualisation ---")

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    loadings_fa,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    ax=ax,
    linewidths=0.5,
)
ax.set_title(
    "Loadings après rotation Varimax\n(|valeur| ≥ 0.5 = lien fort)", fontweight="bold"
)
plt.tight_layout()
plt.savefig("etape5_af.png", dpi=300)
plt.close()


# STEP 6 -> Regression multiple

## 6.1 Creation modele de regression :


X_reg = sm.add_constant(X)

model = sm.OLS(Y, X_reg).fit()

print(model.summary())
