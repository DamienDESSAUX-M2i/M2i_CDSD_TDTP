## Déployer un model en production

```bash
# Servir le modèle en production sur le port 5001
mlflow models serve -m "models:/iris-api-model/Production" -p 5001 --no-conda
```

## Utiliser le modèle :

```bash
curl -X POST http://127.0.0.1:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "dataframe_split": {
      "columns": ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"],
      "data": [[5.1, 3.5, 1.4, 0.2], [5.0, 4.5, 2.0, 0.2]]
    }
  }'
```