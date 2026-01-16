"""
================================================================================
TP SPARK - BROADCAST & ACCUMULATOR
================================================================================

CONTEXTE :
----------
Vous travaillez pour une entreprise e-commerce. Vous disposez de deux fichiers :
- clients.csv : référentiel des clients (34 clients)
- achats.csv : historique des achats (34 transactions)

Le fichier achats.csv contient des données de qualité variable :
- Certains montants sont invalides (texte, vide, négatif)
- Certains clients n'existent pas dans le référentiel

OBJECTIFS :
-----------
1. Utiliser les BROADCAST VARIABLES pour optimiser les jointures
2. Utiliser les ACCUMULATORS pour collecter des métriques pendant le traitement
3. Comparer les performances avec/sans ces optimisations

================================================================================
EXERCICE 1 : CHARGEMENT ET EXPLORATION DES DONNÉES
================================================================================

1.1 Charger les deux fichiers CSV dans des DataFrames
1.2 Afficher le schéma et les premières lignes de chaque DataFrame
1.3 Compter le nombre de lignes dans chaque fichier

================================================================================
EXERCICE 2 : BROADCAST VARIABLE - TABLE DE RÉFÉRENCE PAYS
================================================================================

On souhaite enrichir les données clients avec le taux de TVA par pays.

Table de référence des taux de TVA :
- France : 20%
- Belgique : 21%
- Suisse : 7.7%
- Luxembourg : 17%
- Canada : 5%
- Maroc : 20%

2.1 Créer un dictionnaire Python avec les taux de TVA par pays
2.2 Broadcaster ce dictionnaire vers tous les workers
2.3 Créer une UDF qui utilise la broadcast variable pour récupérer le taux
2.4 Ajouter une colonne "taux_tva" au DataFrame clients
2.5 Afficher les clients avec leur taux de TVA

================================================================================
EXERCICE 3 : BROADCAST VARIABLE - OPTIMISATION DE JOINTURE
================================================================================

On veut joindre les achats avec les informations clients.

3.1 Créer un dictionnaire {id_client: (nom, prenom, segment)} depuis le DataFrame clients
    ATTENTION : Les id_client dans achats.csv sont au format "C001", "C002", etc.
                Les client_id dans clients.csv sont des entiers (1, 2, 3, etc.)
                Il faut faire la correspondance !

3.2 Broadcaster ce dictionnaire
3.3 Enrichir le DataFrame achats avec les informations clients via la broadcast variable
3.4 Comparer le temps d'exécution avec une jointure classique

================================================================================
EXERCICE 4 : ACCUMULATOR - COMPTAGE D'ERREURS
================================================================================

Le fichier achats.csv contient des données invalides. On veut les compter
PENDANT le traitement, sans job supplémentaire.

4.1 Créer les accumulators suivants :
    - montants_valides : nombre de montants valides
    - montants_invalides : nombre de montants non numériques
    - montants_negatifs : nombre de montants négatifs
    - montants_vides : nombre de montants vides
    - clients_inconnus : nombre de clients non trouvés dans le référentiel

4.2 Créer une fonction de parsing qui :
    - Parse le montant (gère les erreurs)
    - Vérifie si le client existe
    - Incrémente les bons accumulators
    - Retourne None si invalide, sinon retourne la ligne enrichie

4.3 Appliquer cette fonction et afficher les statistiques

================================================================================
EXERCICE 5 : ACCUMULATOR PERSONNALISÉ - COLLECTE DE DONNÉES
================================================================================

On veut collecter la liste des clients inconnus et les montants invalides
pour un rapport d'erreurs.

5.1 Créer un AccumulatorParam personnalisé pour collecter des listes
5.2 Collecter :
    - La liste des id_client inconnus
    - La liste des montants invalides (valeur brute)
5.3 Afficher le rapport d'erreurs

================================================================================
EXERCICE 6 : ANALYSE COMPLÈTE AVEC MÉTRIQUES
================================================================================

Réaliser une analyse complète des ventes en utilisant broadcast ET accumulator.

6.1 Calculer pour chaque segment de client :
    - Nombre de transactions valides
    - Montant total des achats
    - Montant moyen par transaction

6.2 Pendant le traitement, collecter via accumulators :
    - Nombre total de transactions traitées
    - Nombre d'erreurs par type
    - Montant total des ventes valides

6.3 Afficher :
    - Les résultats par segment
    - Le taux d'erreur global
    - Le rapport qualité des données

================================================================================
EXERCICE 7 : COMPARAISON DE PERFORMANCE
================================================================================

Comparer les approches avec et sans optimisation.

7.1 SANS optimisation :
    - Jointure classique entre achats et clients
    - Filtrage des erreurs avec plusieurs passes

7.2 AVEC optimisation :
    - Broadcast pour la jointure
    - Accumulators pour le comptage d'erreurs

7.3 Mesurer et comparer les temps d'exécution

================================================================================
BONUS : QUESTIONS DE RÉFLEXION
================================================================================

B.1 Dans quel cas la broadcast variable n'est-elle PAS recommandée ?

B.2 Pourquoi les accumulators ne sont-ils pas fiables pour la logique métier ?

B.3 Quelle est la différence entre cache() et broadcast() ?

B.4 Comment gérer un accumulator pour des opérations non commutatives ?

================================================================================
"""

# =============================================================
# VOTRE CODE ICI
# =============================================================

import time
from typing import Tuple

import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

builder: SparkSession.Builder = SparkSession.builder

# Initialisation Spark
spark = (
    builder.appName("TP_Broadcast_Accumulator")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext

print("=" * 70)
print("TP SPARK - BROADCAST & ACCUMULATOR")
print("=" * 70)

# -------------------------------------------------------------
# EXERCICE 1 : CHARGEMENT DES DONNÉES
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 1 : CHARGEMENT DES DONNÉES")
print("=" * 70)

# 1.1 Charger les deux fichiers CSV dans des DataFrames
clients = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv("/data/clients.csv")
)

achats = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv("/data/achats.csv")
)

# 1.2 Afficher le schéma et les premières lignes de chaque DataFrame
print("\nClient Schema:")
print(clients.schema)
print("\nAchats Schema:")
print(achats.schema)

# 1.3 Compter le nombre de lignes dans chaque fichier
print("\nNumber of lines in clients:")
print(clients.count())
print("\nNumber of lignes in achats:")
print(achats.count())

# -------------------------------------------------------------
# EXERCICE 2 : BROADCAST - TABLE TVA
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 2 : BROADCAST - TABLE TVA")
print("=" * 70)

# On souhaite enrichir les données clients avec le taux de TVA par pays.
# Table de référence des taux de TVA :
# - France : 20%
# - Belgique : 21%
# - Suisse : 7.7%
# - Luxembourg : 17%
# - Canada : 5%
# - Maroc : 20%

# 2.1 Créer un dictionnaire Python avec les taux de TVA par pays
MAP_TVA = {
    "France": 0.2,
    "Belgique": 0.21,
    "Suisse": 0.077,
    "Luxembourg": 0.17,
    "Canada": 0.05,
    "Maroc": 0.2,
}

# 2.2 Broadcaster ce dictionnaire vers tous les workers
map_tva_broadcast = sc.broadcast(MAP_TVA)


# 2.3 Créer une UDF qui utilise la broadcast variable pour récupérer le taux
def get_rate(country: str) -> float:
    return (
        map_tva_broadcast.value[country]
        if country in map_tva_broadcast.value.keys()
        else 0.0
    )


getRate = spark_func.udf(get_rate, DoubleType())

# 2.4 Ajouter une colonne "taux_tva" au DataFrame clients
clients_enriched1 = clients.withColumn("taux_tva", getRate(spark_func.col("country")))

# 2.5 Afficher les clients avec leur taux de TVA
clients_enriched1.show(5)

# -------------------------------------------------------------
# EXERCICE 3 : BROADCAST - JOINTURE OPTIMISÉE
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 3 : BROADCAST - JOINTURE OPTIMISÉE")
print("=" * 70)


# 3.1 Créer un dictionnaire {id_client: (nom, prenom, segment)} depuis le DataFrame clients
#     ATTENTION : Les id_client dans achats.csv sont au format "C001", "C002", etc.
#                 Les client_id dans clients.csv sont des entiers (1, 2, 3, etc.)
#                 Il faut faire la correspondance !
def transform_client_id(client_id: int) -> str:
    return "C" + str(client_id).zfill(3)


transformClientId = spark_func.udf(transform_client_id, StringType())

clients_enriched2 = clients_enriched1.withColumn(
    "client_id", transformClientId(spark_func.col("client_id"))
)

t0 = time.time()

clients_dict = {}
for row in clients_enriched2.select(
    ["client_id", "nom", "prenom", "segment"]
).collect():
    clients_dict[row[0]] = (row[1], row[2], row[3])

print("\nClient C001:")
print(clients_dict["C001"])

# 3.2 Broadcaster ce dictionnaire
clients_dict_broadcast = sc.broadcast(clients_dict)


# 3.3 Enrichir le DataFrame achats avec les informations clients via la broadcast variable
def enriched_with_client(client_id: str) -> Tuple[str, str, str]:
    return (
        clients_dict_broadcast.value[client_id]
        if client_id in clients_dict_broadcast.value.keys()
        else ("Unknown", "Unknown", "Unknown")
    )


schema = StructType(
    [
        StructField("nom", StringType(), False),
        StructField("prenom", StringType(), False),
        StructField("segment", StringType(), False),
    ]
)

enrichedWithClient = spark_func.udf(enriched_with_client, schema)

achats_enriched1 = achats.withColumn(
    "client_info", enrichedWithClient(spark_func.col("id_client"))
)

t1 = time.time()

print(f"\nAggregation WITH broadcast: {t1 - t0}")

print("\nAchats enriched:")
achats_enriched1.show(5)

# 3.4 Comparer le temps d'exécution avec une jointure classique

t2 = time.time()

achats_clients = achats.join(
    other=clients_enriched2,
    on=(achats["id_client"] == clients_enriched2["client_id"]),
    how="left",
)

t3 = time.time()

print(f"\nAggregation WITHOUT broadcast: {t3 - t2}")

print("\nAchats clients:")
achats_clients.show(5)

# -------------------------------------------------------------
# EXERCICE 4 : ACCUMULATOR - COMPTAGE D'ERREURS
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 4 : ACCUMULATOR - COMPTAGE D'ERREURS")
print("=" * 70)

# Le fichier achats.csv contient des données invalides. On veut les compter
# PENDANT le traitement, sans job supplémentaire.

# 4.1 Créer les accumulators suivants :
#     - montants_valides : nombre de montants valides
#     - montants_invalides : nombre de montants non numériques
#     - montants_negatifs : nombre de montants négatifs
#     - montants_vides : nombre de montants vides
#     - clients_inconnus : nombre de clients non trouvés dans le référentiel
montant_valide = sc.accumulator(0)
montants_invalides = sc.accumulator(0)
montants_negatifs = sc.accumulator(0)
montants_vides = sc.accumulator(0)
clients_inconnus = sc.accumulator(0)


# 4.2 Créer une fonction de parsing qui :
#     - Parse le montant (gère les erreurs)
#     - Vérifie si le client existe
#     - Incrémente les bons accumulators
#     - Retourne None si invalide, sinon retourne la ligne enrichie
def parsing_row(row):
    # Montant
    montant: str = row["montant"]
    if not montant:
        montants_invalides.add(1)
        montants_vides.add(1)
        return None
    try:
        montant = float(montant)
    except:
        montants_invalides.add(1)
        return None
    if montant < 0:
        montants_invalides.add(1)
        montants_negatifs.add(1)
        return None
    montant_valide.add(1)
    # Client inconnu
    if not row["client_id"]:
        clients_inconnus.add(1)
        return None
    return row


# 4.3 Appliquer cette fonction et afficher les statistiques
achats_clients.foreach(parsing_row)

print("\nParsing stats:")
print("Montants valides", montant_valide.value)
print("Montants invalides", montants_invalides.value)
print("Montants négatifs", montants_negatifs.value)
print("Montants vides", montants_vides.value)
print("Clients inconnus", clients_inconnus.value)

# -------------------------------------------------------------
# EXERCICE 5 : ACCUMULATOR PERSONNALISÉ
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 5 : ACCUMULATOR PERSONNALISÉ")
print("=" * 70)

# On veut collecter la liste des clients inconnus et les montants invalides
# pour un rapport d'erreurs.

# 5.1 Créer un AccumulatorParam personnalisé pour collecter des listes
# 5.2 Collecter :
#     - La liste des id_client inconnus
#     - La liste des montants invalides (valeur brute)
# 5.3 Afficher le rapport d'erreurs

# -------------------------------------------------------------
# EXERCICE 6 : ANALYSE COMPLÈTE
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 6 : ANALYSE COMPLÈTE")
print("=" * 70)

# TODO: Votre code ici


# -------------------------------------------------------------
# EXERCICE 7 : COMPARAISON DE PERFORMANCE
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 7 : COMPARAISON DE PERFORMANCE")
print("=" * 70)

# TODO: Votre code ici


# Fermeture
spark.stop()
print("\n✅ TP terminé !")
