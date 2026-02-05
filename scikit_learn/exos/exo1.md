## Dataset : Prédiction de qualité du vin

**Contexte** : Vous êtes data scientist pour un domaine vinicole. Votre mission est de prédire la qualité d'un vin (bon/mauvais) basée sur ses caractéristiques chimiques.

## Mission :

1. Exploration : Analyser les valeurs manquantes et les distributions
2. Ajouter une nouvelle variable binaire : bon vin (quality >= 6) vs mauvais vin (quality < 6). Cette variable sera la target
3. Préprocessing : Créer un pipeline de prétraitement
4. Split : Séparer en train/test (80/20)
5. Pipeline : Construire un pipeline complet avec LogisticRegression
6. Évaluation : Calculer l'accuracy

```python
wine_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
wine = pd.read_csv(wine_url, sep=';')
```
