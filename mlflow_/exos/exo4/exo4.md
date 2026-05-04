# Exercice — MlflowClient

## Contexte

Tu travailles sur un projet de détection de spam e-mail. Tu dois comparer plusieurs configurations de `RandomForestClassifier` et de `LogisticRegression`, puis identifier et taguer le meilleur modèle.

**Données :**

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=1500,
    n_features=18,
    n_informative=10,
    random_state=0
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)
```

---

## Tâche 1 — Setup et création de l'experiment

Instancie un `MlflowClient` connecté à `http://localhost:5000`.

Si un experiment nommé `"spam_detection"` existe déjà, supprime-le d'abord avec `client.delete_experiment()`.

Crée ensuite un nouvel experiment avec les tags suivants :

| tag       | valeur          |
|-----------|-----------------|
| `team`    | `data-science`  |
| `project` | `spam-v1`       |
| `owner`   | ton prénom      |

Récupère l'experiment par son nom et affiche son `experiment_id` et son `lifecycle_stage`.

## Tâche 2 — Logger des runs manuellement

Entraîne et logue les 4 configurations suivantes. Pour chaque configuration, crée un run avec `client.create_run()`, log les paramètres, entraîne le modèle, log les métriques, puis **termine le run**.

**Configurations à tester :**

| run_name         | modèle             | hyperparamètres                  |
|------------------|--------------------|----------------------------------|
| `rf_trial_1`     | RandomForest       | `n_estimators=50`, `max_depth=3` |
| `rf_trial_2`     | RandomForest       | `n_estimators=100`, `max_depth=5`|
| `logreg_trial_1` | LogisticRegression | `C=0.1`, `max_iter=200`          |
| `logreg_trial_2` | LogisticRegression | `C=1.0`, `max_iter=200`          |

**Pour chaque run, logger :**

- Paramètres : tous les hyperparamètres du tableau + `model_type`
- Métriques CV (5 folds)
- Métriques test set 
- Tag sur le run : `model_type`

## Tâche 3 — Recherche et filtrage

### 3a. Lister tous les runs

Récupère tous les runs avec `search_runs()`, triés par `test_roc_auc` décroissant. Affiche le `run_name`, `test_accuracy` et `test_roc_auc` de chaque run.

### 3b. Filtrer par seuil de métrique

Récupère uniquement les runs avec `test_roc_auc > 0.85`. Affiche le nombre de runs qui passent ce seuil.

### 3c. Filtrer par type de modèle

Récupère uniquement les runs de type `random_forest` en filtrant sur le tag `model_type`.

### 3d. Combiner les critères

Récupère les runs Random Forest dont `test_accuracy > 0.88`.


## Tâche 4 — Comparer avec un DataFrame

Convertis les résultats de `search_runs()` en `pd.DataFrame` avec les colonnes `run_name`, `model_type`, `test_accuracy`, `test_roc_auc`, `test_f1`, `run_id`. Trie par `test_roc_auc` décroissant et affiche le tableau complet.


## Tâche 5 — Sélectionner et taguer le champion

À partir du DataFrame trié :

1. Récupère le `run_id` du meilleur run
2. Ajoute le tag `status = "champion"` 
3. Ajoute le tag `promoted_at` avec la date du jour
4. Vérifie les tags via `client.get_run(best_run_id).data.tags`
