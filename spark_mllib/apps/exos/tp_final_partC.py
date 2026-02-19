from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

EXOS_PATH = Path(__file__).parent.resolve()
SKLEARN_RESULTS_PATH = EXOS_PATH / "sklearn_results.json"
SPARK_RESULTS_PATH = EXOS_PATH / "spark_results.json"

# ## Partie C — Comparaison et Analyse

# > **Ce script est indépendant des parties A et B.** Il charge uniquement `sklearn_results.json` et `spark_results.json` pour produire les tableaux et graphiques de comparaison.

# ### C.0 Chargement des résultats JSON
df_sklearn = pd.read_json(SKLEARN_RESULTS_PATH)
df_sklearn.rename(
    columns={
        "regression": "sklearn_reg",
        "classification": "sklearn_clf",
    },
    inplace=True,
)
df_spark = pd.read_json(SPARK_RESULTS_PATH)
df_spark.rename(
    columns={
        "regression": "spark_reg",
        "classification": "spark_clf",
    },
    inplace=True,
)

# ### C.1 Tableau comparatif — Régression

# Construire un `DataFrame` Pandas à partir des deux dictionnaires chargés et l'afficher :

# | Aspect               | Scikit-learn | Spark MLlib |
# | -------------------- | ------------ | ----------- |
# | Temps d'entraînement | ? s          | ? s         |
# | MAE                  | ? hg/ha      | ? hg/ha     |
# | RMSE                 | ? hg/ha      | ? hg/ha     |
# | R²                   | ?            | ?           |

# ### C.2 Tableau comparatif — Classification

# Faire de même pour la classification (Accuracy, F1-score, temps).
df_results = pd.concat([df_sklearn, df_spark], axis=1)
df_reg = df_results.loc[["time", "mae", "rmse", "r2"], ["sklearn_reg", "spark_reg"]]
df_clf = df_results.loc[["time", "accuracy", "f1"], ["sklearn_clf", "spark_clf"]]

print(f"\n{'=' * 64}")
print("Sklearn / Spark Comparison:")
print(f"{'=' * 64}")
print("Regression:")
print(df_reg)
print("\nClassification:")
print(df_clf)

# ### C.3 Visualisation comparative

# Produire un graphique à barres groupées comparant les métriques clés des deux frameworks (MAE, RMSE, R², Accuracy, F1)
fig, axes = plt.subplots(1, 2, figsize=(7, 5))
ax1 = axes[0]
df_reg.div(df_reg.max(axis=1), axis=0).plot.bar(rot=0, ax=ax1)
ax1.set_title("Regression")
ax2 = axes[1]
df_clf.div(df_clf.max(axis=1), axis=0).plot.bar(rot=0, ax=ax2)
ax2.set_title("Classification")
plt.tight_layout()
save_path = EXOS_PATH / "comparison_sklearn_spark.png"
plt.savefig(save_path.as_posix(), dpi=300)
