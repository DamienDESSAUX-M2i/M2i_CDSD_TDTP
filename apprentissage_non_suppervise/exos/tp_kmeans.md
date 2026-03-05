## TP – Segmentation clients avec K-Means 

### Contexte métier

Vous êtes data analyst dans une enseigne de centre commercial.
La direction marketing souhaite mieux comprendre les profils clients afin de :

* Adapter les campagnes promotionnelles
* Identifier les clients à fort potentiel
* Optimiser les offres personnalisées
* Mettre en place des stratégies de fidélisation ciblées

Vous disposez d’un jeu de données réel contenant des informations sur les clients.

---

## Jeu de données

Nom : Mall Customers Dataset

Source officielle (Kaggle) :
[https://www.kaggle.com/datasets/shwetabh123/mall-customers](https://www.kaggle.com/datasets/shwetabh123/mall-customers)

Le dataset contient 200 clients avec les variables suivantes :

* CustomerID : identifiant unique
* Gender : genre du client
* Age : âge du client
* Annual Income (k$) : revenu annuel en milliers de dollars
* Spending Score (1-100) : score de dépense attribué par le centre commercial

Le Spending Score est un indicateur interne basé sur le comportement d’achat.

---

## Objectif général

Mettre en œuvre une segmentation non supervisée des clients à l’aide de l’algorithme K-Means afin de proposer une analyse stratégique exploitable par le service marketing.

---

## Travail demandé

### Partie 1 – Analyse exploratoire

1. Décrire la structure du jeu de données.
2. Identifier les variables pertinentes pour la segmentation.
3. Analyser la distribution des variables numériques.
4. Détecter d’éventuelles valeurs aberrantes.
5. Justifier les variables retenues pour le clustering.

---

### Partie 2 – Préparation des données

1. Sélectionner les variables utilisées pour K-Means.
2. Justifier la nécessité (ou non) de la normalisation.
3. Appliquer une standardisation adaptée.
4. Expliquer mathématiquement pourquoi le scaling est important dans K-Means.

---

### Partie 3 – Choix du nombre de clusters

1. Appliquer la méthode du coude (Elbow Method).
2. Interpréter la courbe d’inertie.
3. Calculer le score de silhouette pour différents k.
4. Justifier le choix final du nombre de clusters.
5. Discuter les limites de ces méthodes.

---

### Partie 4 – Clustering avec K-Means

1. Entraîner un modèle K-Means avec le nombre de clusters choisi.
2. Associer chaque client à un cluster.
3. Extraire les centres des clusters.
4. Interpréter la signification des centres dans l’espace des variables.

---

### Partie 5 – Analyse métier des segments

Pour chaque cluster :

1. Calculer les moyennes des variables numériques.
2. Identifier le profil type du segment.
3. Donner un nom stratégique au segment (ex : VIP, impulsifs, prudents, etc.).

---

### Partie 6 – Analyse critique

1. Quelles sont les limites de K-Means dans ce contexte ?
2. Que se passe-t-il si on ajoute la variable Age ?
3. Que se passe-t-il si on ajoute Gender ?
4. Quels seraient les avantages d’un modèle probabiliste comme GMM ?
5. Dans quels cas DBSCAN serait-il plus adapté ?

