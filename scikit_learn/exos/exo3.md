# Exercice 2 : Regression Logistique - Prediction de Defaut de Paiement

## Contexte

Vous etes data scientist dans une banque qui souhaite predire le risque de defaut de paiement de ses clients sur leurs cartes de credit. Un modele performant permettra d'identifier les clients a risque et d'adapter les strategies commerciales en consequence.

## Dataset

Vous utiliserez le dataset **Default of Credit Card Clients** disponible sur UCI ML Repository.

```python
import pandas as pd
from sklearn.datasets import fetch_openml


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
df = pd.read_excel(url, header=1)
```

### Description des variables principales

| Variable                   | Description                                                                   |
| -------------------------- | ----------------------------------------------------------------------------- |
| LIMIT_BAL                  | Montant du credit accorde (en dollars taiwanais)                              |
| SEX                        | Genre (1=homme, 2=femme)                                                      |
| EDUCATION                  | Niveau d'education (1=graduate school, 2=university, 3=high school, 4=others) |
| MARRIAGE                   | Statut marital (1=marie, 2=celibataire, 3=autres)                             |
| AGE                        | Age (annees)                                                                  |
| PAY_0 a PAY_6              | Statut de paiement mensuel (-1=paye, 0=revolving, 1-9=mois de retard)         |
| BILL_AMT1 a BILL_AMT6      | Montant de la facture (6 derniers mois)                                       |
| PAY_AMT1 a PAY_AMT6        | Montant du paiement (6 derniers mois)                                         |
| default.payment.next.month | **Variable cible** (1=defaut, 0=pas de defaut)                                |

## Partie 1 : Exploration et Preprocessing

### Question 1.1 : Chargement et exploration initiale

- Chargez le dataset et examinez sa structure
- Combien d'observations et de variables ?
- Renommez la colonne cible en 'default' pour simplifier
- Verifiez les valeurs manquantes

### Question 1.2 : Analyse de la variable cible

- Quelle est la proportion de defauts de paiement ?
- Le dataset est-il desequilibre ?
- Visualisez la distribution avec un diagramme en barres

### Question 1.3 : Analyse des variables categorielles

Pour les variables SEX, EDUCATION et MARRIAGE :

- Affichez la distribution de chaque categorie
- Calculez le taux de defaut par categorie
- Y a-t-il des categories avec des valeurs inattendues ?

### Question 1.4 : Analyse des variables numeriques

- Creez des boxplots pour LIMIT_BAL et AGE par classe de defaut
- Y a-t-il des differences notables entre les deux groupes ?
- Identifiez les outliers potentiels

### Question 1.5 : Feature engineering

Creez les nouvelles features suivantes :

- `utilization_rate` : ratio moyen utilisation credit (BILL_AMT / LIMIT_BAL)
- `payment_ratio` : ratio moyen paiement/facture (PAY_AMT / BILL_AMT)
- `total_delay` : somme des retards de paiement (PAY_0 a PAY_6)

## Partie 2 : Preparation des Donnees

### Question 2.1 : Encodage des variables categorielles

- Appliquez One-Hot Encoding sur EDUCATION et MARRIAGE
- Gardez SEX en binaire (0/1)
- Supprimez les colonnes originales apres encodage

### Question 2.2 : Separation et standardisation

- Separez features (X) et cible (y)
- Divisez en train/test (80/20, stratify=y)
- Standardisez les features numeriques

## Partie 3 : Entrainement du Modele

### Question 3.1 : Modele de base

Entrainez une regression logistique avec les parametres par defaut
