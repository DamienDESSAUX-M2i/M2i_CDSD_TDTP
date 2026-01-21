# TP - Nettoyage de Données E-commerce avec PySpark

## Données

**Fichier** : `commandes_ecommerce.csv` (200 lignes)

**Colonnes** :

- `id_commande` : identifiant unique
- `date` : date de commande (YYYY-MM-DD)
- `client` : nom du client
- `produit` : produit commandé (Laptop, Smartphone, Tablette, Écouteurs, Clavier, Souris, Moniteur, Webcam)
- `quantite` : nombre d'unités
- `prix_unitaire` : prix en euros
- `region` : région de livraison
- `statut` : état de la commande

**Problèmes identifiés** :

- ~7% de produits manquants (null)
- ~8% de quantités négatives
- ~4% de quantités à zéro
- ~5% de quantités nulles
- ~16% de clients invalides (null, "NULL", espaces)
- ~12% de prix unitaires manquants
- ~10% de dates manquantes
- ~6% de régions manquantes

## Exercice

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, coalesce, lit, trim

# Initialisation
spark = SparkSession.builder.master("local").appName("Nettoyage").getOrCreate()

# Chargement


# 1. Supprimer les lignes sans produit


# 2. Corriger les quantités négatives (valeur absolue)


# 3. Supprimer les quantités nulles ou zéro


# 4. Remplacer les clients invalides par "Client Anonyme"
#    (gérer : null, "NULL", et espaces)


# 5. Imputer les prix manquants avec la moyenne par produit


# 6. Supprimer les lignes sans date


# 7. Remplacer les régions nulles par "Non spécifiée"


# 8. Ajouter une colonne montant_total (quantite * prix_unitaire)


# Sauvegarde

```
