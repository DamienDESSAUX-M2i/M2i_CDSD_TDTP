# Exercice : Prédiction de notation de restaurants

## Objectif

Comparer les performances de 3 algorithmes de classification (KNN, Decision Tree, Random Forest) pour prédire la catégorie de notation d'un restaurant basée sur ses caractéristiques.

## Contexte

Vous travaillez pour une plateforme de réservation de restaurants en ligne. Votre mission est de créer un système capable de prédire la catégorie de notation d'un restaurant avant même qu'il reçoive des avis clients, en se basant uniquement sur ses caractéristiques objectives (prix, type de cuisine, services, etc.).

## Dataset

Vous allez générer un dataset synthétique réaliste de restaurants :

```python
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

# Génération du dataset
np.random.seed(42)
n_restaurants = 1000

# Génération des features
data = {
    'price_range': np.random.choice([1, 2, 3, 4], n_restaurants, p=[0.2, 0.35, 0.3, 0.15]),
    'cuisine_type': np.random.choice(['Italien', 'Français', 'Japonais', 'Mexicain',
                                       'Indien', 'Américain', 'Chinois', 'Méditerranéen'], n_restaurants),
    'city_zone': np.random.choice(['Centre', 'Banlieue', 'Périphérie'], n_restaurants, p=[0.4, 0.35, 0.25]),
    'seating_capacity': np.random.randint(20, 200, n_restaurants),
    'years_open': np.random.randint(1, 30, n_restaurants),
    'has_terrace': np.random.choice([0, 1], n_restaurants, p=[0.6, 0.4]),
    'has_parking': np.random.choice([0, 1], n_restaurants, p=[0.5, 0.5]),
    'delivery_service': np.random.choice([0, 1], n_restaurants, p=[0.4, 0.6]),
    'accepts_reservation': np.random.choice([0, 1], n_restaurants, p=[0.3, 0.7]),
    'vegetarian_options': np.random.choice([0, 1], n_restaurants, p=[0.2, 0.8]),
    'avg_wait_time': np.random.randint(5, 60, n_restaurants),
    'chef_experience': np.random.randint(0, 25, n_restaurants)
}

restaurants = pd.DataFrame(data)

# Génération de la variable cible (rating) basée sur une logique
# Plus de points pour : prix élevé, zone centrale, chef expérimenté, services, ancienneté
score = (
    restaurants['price_range'] * 15 +
    restaurants['chef_experience'] * 2 +
    restaurants['years_open'] * 1.5 +
    (restaurants['city_zone'] == 'Centre') * 20 +
    restaurants['has_terrace'] * 10 +
    restaurants['has_parking'] * 8 +
    restaurants['accepts_reservation'] * 12 +
    restaurants['vegetarian_options'] * 5 +
    (60 - restaurants['avg_wait_time']) * 0.5 +
    np.random.normal(0, 15, n_restaurants)  # Bruit aléatoire
)

# Catégorisation en 4 classes
restaurants['rating_category'] = pd.cut(
    score,
    bins=4,
    labels=['Moyen', 'Bon', 'Très bon', 'Excellent']
)

print(restaurants.head())
print(f"\nDistribution des catégories :\n{restaurants['rating_category'].value_counts().sort_index()}")
```

## Variables disponibles

### Variables indépendantes (features)

- **price_range** : Gamme de prix (1=€, 2=€€, 3=€€€, 4=€€€€)
- **cuisine_type** : Type de cuisine
- **city_zone** : Zone de la ville (Centre, Banlieue, Périphérie)
- **seating_capacity** : Nombre de places assises
- **years_open** : Nombre d'années d'existence
- **has_terrace** : Présence d'une terrasse (0/1)
- **has_parking** : Parking disponible (0/1)
- **delivery_service** : Service de livraison (0/1)
- **accepts_reservation** : Accepte les réservations (0/1)
- **vegetarian_options** : Options végétariennes (0/1)
- **avg_wait_time** : Temps d'attente moyen (minutes)
- **chef_experience** : Années d'expérience du chef

### Variable cible

- **rating_category** : Catégorie de notation (Moyen, Bon, Très bon, Excellent)

## Étapes à réaliser

### 1. Exploration des données

- Générez le dataset avec le code fourni
- Affichez les 10 premières lignes
- Vérifiez s'il y a des valeurs manquantes
- Analysez la distribution des catégories de notation
- Créez un graphique montrant la distribution des ratings par zone de ville
- Créez un graphique montrant la relation entre price_range et rating_category

### 2. Préparation des données

- Séparez X (features) et y (target)
- Identifiez les variables numériques et catégorielles
- Encodez les variables catégorielles
- Divisez les données en train/test (80/20)

### 3. Construction des modèles

#### a) K-Nearest Neighbors (KNN)

#### b) Decision Tree (Arbre de décision)

#### c) Random Forest

### 4. Évaluation et comparaison

Pour chaque modèle evaluez les metriques
Créez un tableau comparatif

### 5. Prédiction sur de nouveaux restaurants

Créez 3 restaurants fictifs et prédisez leur catégorie
