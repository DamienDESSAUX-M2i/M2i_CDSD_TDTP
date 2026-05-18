# Démo KPIs de Performance Modèle

Cette démo simule plusieurs types de problèmes de machine learning et calcule les KPIs adaptés.

## Conteneurs

1. `model-simulator` : génère des datasets artificiels et entraîne des modèles simples
2. `model-kpi-dashboard` : affiche les résultats dans Streamlit

## Types de problèmes simulés

| Type de problème | KPIs pertinents | Quand les choisir |
|---|---|---|
| Classification équilibrée | Accuracy | Classes équilibrées et erreurs symétriques |
| Classification déséquilibrée | F1-score, Precision, Recall, AUC-ROC | Fraude, churn, panne rare |
| Régression | RMSE, MAE, MAPE, R² | Prédiction de valeurs continues |
| Clustering | Silhouette, Davies-Bouldin | Évaluation non supervisée |

## Lancement

```bash
docker compose up --build
```

## Dashboard

```txt
http://localhost:8502
```

## Relance propre

```bash
docker compose down -v
docker compose up --build
```
