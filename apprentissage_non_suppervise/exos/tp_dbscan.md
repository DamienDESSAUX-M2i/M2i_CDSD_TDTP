# TP — Détection de zones géographiques d’activité avec DBSCAN

## Contexte

Vous travaillez pour une plateforme de mobilité urbaine (type Uber / Bolt / Deliveroo).

L’entreprise souhaite :

* Identifier automatiquement les zones à forte activité.
* Détecter les “hotspots” naturels de la ville.
* Identifier les zones isolées.
* Détecter les points aberrants (erreurs GPS, trajets suspects).

Vous disposez d’un jeu de données réel contenant des coordonnées GPS.

---

# Jeu de données réel

Nom : NYC Taxi Trip Data (échantillon)

Source officielle :
[https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

Un échantillon simplifié peut être utilisé via Kaggle :

[https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data)

Variables importantes :

* pickup_longitude
* pickup_latitude

Chaque ligne = une prise en charge taxi.

---

# Objectif du TP

Utiliser DBSCAN pour :

1. Identifier les zones de forte concentration de pickups.
2. Détecter les points aberrants.
3. Interpréter les clusters comme des zones d’activité urbaines.

---

# Partie 1 — Préparation des données

1. Charger un échantillon de 5 000 à 20 000 points.
2. Conserver uniquement :

   * latitude
   * longitude
3. Supprimer :

   * coordonnées nulles
   * coordonnées hors de NYC
4. Convertir les coordonnées en radians si nécessaire.

Question :

Pourquoi la distance euclidienne classique n’est pas idéale pour des coordonnées GPS ?

Indice : distance sphérique (Haversine).

---

# Partie 2 — Compréhension des paramètres DBSCAN

1. Quelle unité doit avoir epsilon pour des coordonnées GPS ?
2. Pourquoi min_samples doit être ajusté selon la densité urbaine ?
3. Pourquoi la dimension (ici 2D) simplifie le choix des paramètres ?

---

# Partie 3 — Choix d’epsilon

Méthode k-distance :

1. Calculer la distance au 4e ou 5e voisin.
2. Tracer la courbe triée.
3. Identifier le “coude”.
4. Justifier le choix d’epsilon.

Expliquer ce que représente physiquement epsilon (ex : 200 mètres).

---

# Partie 4 — Application DBSCAN

1. Appliquer DBSCAN avec la métrique appropriée (euclidienne ou haversine).
2. Identifier :

   * nombre de clusters
   * nombre de points bruit
3. Visualiser les clusters sur une carte.

---

# Partie 5 — Interprétation métier

Pour chaque cluster :

1. Calculer le centre géographique.
2. Identifier la zone correspondante (ex : Manhattan Midtown, JFK Airport, etc.).
3. Interpréter :

   * zone résidentielle
   * zone touristique
   * zone aéroportuaire
   * zone d’affaires

---

# Partie 6 — Analyse avancée

1. Que se passe-t-il si epsilon est trop petit ?
2. Que se passe-t-il si epsilon est trop grand ?
3. Que se passe-t-il si min_samples augmente fortement ?
4. DBSCAN peut-il détecter des zones de densité très différentes ?
5. Proposer une alternative si les densités sont hétérogènes.

