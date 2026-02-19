import json
import time
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import numpy as np

EXOS_PATH = Path(__file__).parent.resolve()
APP_PATH = EXOS_PATH.parent
SPARKML_PATH = APP_PATH.parent
DATA_PATH = SPARKML_PATH / "data"
CROP_YIELD_PATH = DATA_PATH / "crop_yield.csv"

# ### A.1 Chargement et exploration

# Charger le fichier `crop_yield.csv` avec Pandas.
crop_yield = pd.read_csv(CROP_YIELD_PATH.as_posix()).drop("Unnamed: 0", axis=1)

# - Afficher les dimensions et les types de colonnes
print(f"\n{'=' * 64}")
print("Info:")
print(f"{'=' * 64}")
crop_yield.info()

# - Identifier les valeurs manquantes (nombre et pourcentage par colonne)
print(f"\n{'=' * 64}")
print("Null:")
print(f"{'=' * 64}")
print(crop_yield.isna().sum())

# - Afficher les statistiques descriptives (`describe()`)
print(f"\n{'=' * 64}")
print("Info:")
print(f"{'=' * 64}")
print(crop_yield.describe())

# - Afficher la distribution du rendement (`hg/ha_yield`) avec un histogramme
print(f"\n{'=' * 64}")
print("Histogram 'hg/ha_yield':")
print(f"{'=' * 64}")

plt.figure(figsize=(7, 5))
plt.title("Histogram 'hg/ha_yield'")
crop_yield["hg/ha_yield"].hist(bins=int(1 + np.log2(len(crop_yield))))
plt.tight_layout()
save_path = EXOS_PATH / "hg_ha_yield_hist.png"
plt.savefig(save_path.as_posix(), dpi=300)

print("Histogram path: ", save_path)

# - Afficher le rendement moyen par type de culture (`Item`) — top 10
print(f"\n{'=' * 64}")
print("Top 10 average 'hg/ha_yield' per 'Item':")
print(f"{'=' * 64}")
print(crop_yield.groupby("Item")["hg/ha_yield"].mean().nlargest(10))

# - Afficher le rendement moyen par pays (`Area`) — top 10
print(f"\n{'=' * 64}")
print("Top 10 average 'hg/ha_yield' per 'Area':")
print(f"{'=' * 64}")
print(crop_yield.groupby("Area")["hg/ha_yield"].mean().nlargest(10))

# ### A.2 Préparation des données

# - **Créer la cible de classification :**
print(f"\n{'=' * 64}")
print("Compute 'high_yield':")
print(f"{'=' * 64}")
median_yield = crop_yield["hg/ha_yield"].median()
crop_yield["high_yield"] = (crop_yield["hg/ha_yield"] > median_yield).astype(int)
print(f"Average 'high_yield': {median_yield:.0f} hg/ha")
print("Distribution 'high_yield':")
print(crop_yield["high_yield"].value_counts())

# - **Définir les features :**
print(f"\n{'=' * 64}")
print("Features and target:")
print(f"{'=' * 64}")
features = [
    "Area",
    "Item",
    "Year",
    "average_rain_fall_mm_per_year",
    "pesticides_tonnes",
    "avg_temp",
]
print("Features: ", features)
target_reg = "hg/ha_yield"
print("Target regressor: ", target_reg)
target_clf = "high_yield"
print("Target classification: ", target_clf)

# - **Split train/test **
print(f"\n{'=' * 64}")
print("Split train/test:")
print(f"{'=' * 64}")
X = crop_yield[features]
y_reg = crop_yield[target_reg]
y_clf = crop_yield[target_clf]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X, y_reg, test_size=0.2, random_state=42, stratify=y_clf
)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

num_features = X.select_dtypes(include=np.number).columns.to_list()
cat_features = X.select_dtypes(include="object").columns.to_list()
print("Numerical features: ", num_features)
print("Categorical features: ", cat_features)

# ### A.3 Pipeline Scikit-learn — Régression

# Construire un `Pipeline` avec `ColumnTransformer` :

# **Transformer numérique :**

# 1. `SimpleImputer(strategy='median')`
# 2. `StandardScaler`
num_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

# **Transformer catégoriel :**

# 1. `SimpleImputer(strategy='most_frequent')`
# 2. `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`
cat_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", cat_pipeline, cat_features),
        ("num", num_pipeline, num_features),
    ]
)

# **Régresseur :** `RandomForestRegressor(n_estimators=100, random_state=42)`
rf_reg_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]
)

# ### A.4 Pipeline Scikit-learn — Classification

# Réutiliser le même `preprocessor` avec un `RandomForestClassifier` :
rf_clf_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]
)

# ### A.5 Entraînement et mesure du temps
print(f"\n{'=' * 64}")
print("Regressor Pipeline:")
print(f"{'=' * 64}")
t0_rf_reg = time.time()
rf_reg_pipeline.fit(X_train_reg, y_train_reg)
t1_rf_reg = time.time()

# ### A.6 Évaluation

# **Régression :**

# - MAE
# - RMSE
# - R²

y_pred_rf_reg = rf_reg_pipeline.predict(X_test_reg)

results_reg = {}
results_reg["regression"] = {
    "mae": mean_absolute_error(y_test_reg, y_pred_rf_reg),
    "rmse": root_mean_squared_error(y_test_reg, y_pred_rf_reg),
    "r2": r2_score(y_test_reg, y_pred_rf_reg),
    "time": t1_rf_reg - t0_rf_reg,
}

print(f"{'Model':<30} | {'mae':<10} | {'rmse':<10} | {'r2':<10} | {'time':<10}")
for model, metrics in results_reg.items():
    print(
        f"{'RandomForestRegressor':<30} | {metrics['mae']:<10.6f} | {metrics['rmse']:<10.6f} | {metrics['r2']:<10.6f} | {metrics['time']:<10.6f}"
    )

print(f"\n{'=' * 64}")
print("Regressor Pipeline:")
print(f"{'=' * 64}")
t0_rf_clf = time.time()
rf_clf_pipeline.fit(X_train_clf, y_train_clf)
t1_rf_clf = time.time()

# **Classification :**

# - Accuracy
# - F1-score
# - Matrice de confusion

y_pred_rf_clf = rf_clf_pipeline.predict(X_test_clf)

results_clf = {}
results_clf["classification"] = {
    "accuracy": accuracy_score(y_test_clf, y_pred_rf_clf),
    "f1": f1_score(y_test_clf, y_pred_rf_clf),
    "time": t1_rf_reg - t0_rf_reg,
}

print(f"{'Model':<30} | {'accuracy':<10} | {'f1':<10} | {'time':<10}")
for model, metrics in results_clf.items():
    print(
        f"{'RandomForestClassifier':<30} | {metrics['accuracy']:<10.4f} | {metrics['f1']:<10.4f} | {metrics['time']:<10.6f}"
    )

conf_mat = confusion_matrix(y_test_clf, y_pred_rf_clf)
print("\nConfusion Matrix:")
print(f"TP: {conf_mat[0, 0]:<10} | FN: {conf_mat[0, 1]:<10}")
print(f"FP: {conf_mat[1, 0]:<10} | TN: {conf_mat[1, 1]:<10}")

# ### A.7 Feature Importances

# Extraire et afficher les 10 features les plus importantes pour **chacun des deux modèles**
print(f"\n{'=' * 64}")
print("Feature importance RandomForestRegressor:")
print(f"{'=' * 64}")
rf_reg = rf_reg_pipeline.named_steps["regressor"]
preprocessor_fit = rf_reg_pipeline.named_steps["preprocessor"]

encoder = preprocessor_fit.named_transformers_["cat"].named_steps["encoder"]
cat_features = encoder.get_feature_names_out(cat_features).tolist()
all_features = cat_features + num_features

rf_reg_importances = rf_reg.feature_importances_
indices = np.argsort(rf_reg_importances)[::-1]

sorted_names = [all_features[i] for i in indices]
sorted_imp = rf_reg_importances[indices]

fig, axes = plt.subplots()
axes.barh(range(len(sorted_imp[:10])), sorted_imp[::-1][:10])
axes.set_yticks(range(len(sorted_imp[:10])))
axes.set_yticklabels(sorted_names[::-1][:10], fontsize=10)
axes.set_xlabel("Importance", fontsize=10)
axes.set_title("Feature importance RandomForestClassifier")
plt.tight_layout()
save_path = EXOS_PATH / "rf_reg_feature_importance.png"
plt.savefig(save_path.as_posix(), dpi=300)

print("Feature importance RandomForestRegressor path: ", save_path)

print(f"\n{'=' * 64}")
print("Feature importance RandomForestClassifier:")
print(f"{'=' * 64}")
rf_clf = rf_clf_pipeline.named_steps["classifier"]

rf_clf_importances = rf_clf.feature_importances_
indices = np.argsort(rf_clf_importances)[::-1]

sorted_names = [all_features[i] for i in indices]
sorted_imp = rf_clf_importances[indices]

fig, axes = plt.subplots()
axes.barh(range(len(sorted_imp[:10])), sorted_imp[::-1][:10])
axes.set_yticks(range(len(sorted_imp[:10])))
axes.set_yticklabels(sorted_names[::-1][:10], fontsize=10)
axes.set_xlabel("Importance", fontsize=10)
axes.set_title("Feature importance RandomForestClassifier")
plt.tight_layout()
save_path = EXOS_PATH / "rf_clf_feature_importance.png"
plt.savefig(save_path.as_posix(), dpi=300)

print("Feature importance RandomForestClassifier path: ", save_path)

# ### A.8 Sauvegarde et export JSON

# - Sauvegarder les deux pipelines avec `joblib.dump`
print(f"\n{'=' * 64}")
print("Save pipelines:")
print(f"{'=' * 64}")
rf_reg_pipeline_path = EXOS_PATH / "rf_reg_pipeline.pkl"
joblib.dump(rf_reg_pipeline, rf_reg_pipeline_path.as_posix())
print("RandomForestRegressor Pipeline path: ", rf_reg_pipeline_path)

rf_clf_pipeline_path = EXOS_PATH / "rf_clf_pipeline.pkl"
joblib.dump(rf_clf_pipeline, rf_clf_pipeline_path.as_posix())
print("RandomForestClassifier Pipeline path: ", rf_clf_pipeline_path)

# - Exporter les métriques dans un fichier `sklearn_results.json` au format suivant :

# ```json
# {
#   "regression": {
#     "time": 0.0,
#     "mae": 0.0,
#     "rmse": 0.0,
#     "r2": 0.0
#   },
#   "classification": {
#     "time": 0.0,
#     "accuracy": 0.0,
#     "f1": 0.0
#   }
# }
# ```
print(f"\n{'=' * 64}")
print("Save Sklearn results:")
print(f"{'=' * 64}")
data = {}
data.update(results_reg)
data.update(results_clf)
json_path = EXOS_PATH / "sklearn_results.json"
json_path.write_text(data=json.dumps(data), encoding="utf-8")
print("Sklearn results path: ", json_path)
