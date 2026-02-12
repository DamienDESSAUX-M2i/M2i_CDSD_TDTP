# TP : Prediction du Churn Client

Vous etes data scientist dans une entreprise de telecommunications. Le departement marketing vous demande de predire quels clients risquent de quitter l'entreprise (churn) dans les prochains mois.

**Enjeux business :**

- Cout d'acquisition d'un nouveau client : ~500€
- Cout de retention d'un client existant : ~100€
- Taux de churn actuel : ~15%
- Objectif : identifier les clients a risque pour lancer des actions de retention ciblees

**Contraintes :**

- Le modele doit etre interpretable pour l'equipe marketing
- Il faut minimiser les faux negatifs (clients qui partent sans etre detectes)

## Dataset

Utilisez le dataset Telco Customer Churn disponible sur Kaggle :

```python
# URL : https://www.kaggle.com/blastchar/telco-customer-churn
```

## Cahier des Charges

### Phase 1 : Exploration et Preparation des Donnees

#### 1.1 Chargement et exploration

- Charger le dataset
- Afficher les dimensions et types de donnees
- Identifier les valeurs manquantes
- Analyser la distribution de la variable cible (Churn)

#### 1.2 Analyse exploratoire

- Statistiques descriptives des variables numeriques
- Distribution des variables categoriques
- Correlation entre variables numeriques
- Taux de churn par segment (contrat, anciennete, etc.)

#### 1.3 Visualisations

- Histogrammes des variables numeriques
- Bar plots du taux de churn par categorie
- Heatmap de correlation

#### 1.4 Preparation des donnees

- Traitement des valeurs manquantes
- Encodage des variables categoriques
- Separation train/test (stratifiee)
- Normalisation si necessaire

### Phase 2 : Modelisation

#### 2.1 Baseline

- Entrainer un modele simple (Logistic Regression)
- Etablir les metriques de reference

#### 2.2 Comparaison d'algorithmes

Tester au minimum :

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- KNN

Pour chaque modele :

- Metriques : Accuracy, Precision, Recall, F1

#### 2.3 Selection du meilleur modele

- Tableau comparatif des performances
- Choix du modele base sur les criteres metier (recall important)

### 3 Feature importance

- Analyser l'importance des features
- Identifier les 5 features les plus predictives
- Tester un modele avec seulement ces features

### Phase 4 : Mise en Production

#### 4.1 Pipeline final

- Creer un pipeline sklearn complet
- Inclure preprocessing + modele

#### 5.2 Sauvegarde du modele

- Sauvegarder avec joblib

#### 5.3 Fonction de prediction

```python
def predict_churn(customer_data):
    """
    Predit le risque de churn pour un client.

    Args:
        customer_data: dict avec les caracteristiques du client

    Returns:
        dict avec probabilite de churn et recommandation
    """
    # A implementer
    pass
```
