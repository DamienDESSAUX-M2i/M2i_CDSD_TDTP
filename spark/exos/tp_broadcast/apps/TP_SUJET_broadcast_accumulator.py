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
-> Lorsque la taille des données est trop importante.

B.2 Pourquoi les accumulators ne sont-ils pas fiables pour la logique métier ?
-> Spark peut rééxécuter une tâche or les accumulateurs ne sont pas réinitialisé.
Le résultat d'un accumulateur n'est donc pas certain et peut varier d'une exécution à l'autre.

B.3 Quelle est la différence entre cache() et broadcast() ?
-> les données en cache sont réparties sur le cluster tandis que les données en broadcast sont dupliquées sur chaque éxécutant.
Le broadcast est réservé aux petites données tandis que le cache peut être utilisé pour des volumes plus importants.
Le cache est destiné à une optimisation de performance calcul tandis que le broadcast est destiné à une optimisation de communication.

B.4 Comment gérer un accumulator pour des opérations non commutatives ?
-> On n'utilise pas d'accumulateur pour du non commutatif à cause du parallélisme des calculs.

================================================================================
"""

# =============================================================
# VOTRE CODE ICI
# =============================================================

import time
from typing import Tuple

import pyspark.sql.functions as spark_func
from pyspark.accumulators import AccumulatorParam
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

t1 = time.time()

achats_enriched1 = achats.withColumn(
    "client_info", enrichedWithClient(spark_func.col("id_client"))
)

t2 = time.time()

print(f"\nAggregation WITH broadcast: {t2 - t1}")

print("\nAchats enriched:")
achats_enriched1.show(5)

# 3.4 Comparer le temps d'exécution avec une jointure classique

t3 = time.time()

achats_clients = achats.join(
    other=clients_enriched2,
    on=(achats["id_client"] == clients_enriched2["client_id"]),
    how="left",
)

t4 = time.time()

print(f"\nAggregation WITHOUT broadcast: {t4 - t3}")

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
class ListCollector(AccumulatorParam):
    def zero(self, v):
        return []

    def addInPlace(self, variable: list, value: str):
        variable.append(value)
        return variable


# 5.2 Collecter :
#     - La liste des id_client inconnus
#     - La liste des montants invalides (valeur brute)
list_montants_invalides = sc.accumulator([], ListCollector())
list_clients_inconnus = sc.accumulator([], ListCollector())


def parsing_row2(row):
    # Montant invalide
    try:
        montant = float(row["montant"])
        if montant < 0:
            list_montants_invalides.add(row["montant"])
    except:
        list_montants_invalides.add(row["montant"])

    # Client inconnu
    if not row["client_id"]:
        list_clients_inconnus.add(row["client_id"])
    return row


achats_clients.foreach(parsing_row2)

# 5.3 Afficher le rapport d'erreurs
print("\nParsing stats:")
print("Montants invalides", list_montants_invalides.value)
print("Clients inconnus", list_clients_inconnus.value)

# -------------------------------------------------------------
# EXERCICE 6 : ANALYSE COMPLÈTE
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 6 : ANALYSE COMPLÈTE")
print("=" * 70)

# Réaliser une analyse complète des ventes en utilisant broadcast ET accumulator.

# 6.1 Calculer pour chaque segment de client :
#     - Nombre de transactions valides
#     - Montant total des achats
#     - Montant moyen par transaction
# 6.2 Pendant le traitement, collecter via accumulators :
#     - Nombre total de transactions traitées
#     - Nombre d'erreurs par type
#     - Montant total des ventes valides

senior_transaction_valide = sc.accumulator(0)
senior_montant_total = sc.accumulator(0)
b2c_transaction_valide = sc.accumulator(0)
b2c_montant_total = sc.accumulator(0)
etudiant_transaction_valide = sc.accumulator(0)
etudiant_montant_total = sc.accumulator(0)
b2b_transaction_valide = sc.accumulator(0)
b2b_montant_total = sc.accumulator(0)
vip_transaction_valide = sc.accumulator(0)
vip_montant_total = sc.accumulator(0)

err_transaction_invalide = sc.accumulator(0)
err_montants_invalides = sc.accumulator(0)
err_montants_negatifs = sc.accumulator(0)
err_montants_vides = sc.accumulator(0)
err_clients_inconnus = sc.accumulator(0)

MAP_ACC = {
    "Sénior": {
        "transactions_valides": senior_transaction_valide,
        "montant_total": senior_montant_total,
    },
    "B2C": {
        "transactions_valides": b2c_transaction_valide,
        "montant_total": b2c_montant_total,
    },
    "Etudiant": {
        "transactions_valides": etudiant_transaction_valide,
        "montant_total": etudiant_montant_total,
    },
    "B2B": {
        "transactions_valides": b2b_transaction_valide,
        "montant_total": b2b_montant_total,
    },
    "VIP": {
        "transactions_valides": vip_transaction_valide,
        "montant_total": vip_montant_total,
    },
}


def parsing_row3(row):
    acc_dict = MAP_ACC[row["segment"]]
    # Client inconnu
    if not row["client_id"]:
        err_transaction_invalide.add(1)
        err_clients_inconnus.add(1)
        return None
    # Montant invalide
    if not row["montant"]:
        err_transaction_invalide.add(1)
        err_montants_invalides.add(1)
        err_montants_vides.add(1)
        return None
    try:
        montant = float(row["montant"])
        if montant >= 0:
            acc_dict["montant_total"].add(montant)
            acc_dict["transactions_valides"].add(1)
        else:
            err_transaction_invalide.add(1)
            err_montants_invalides.add(1)
            err_montants_negatifs.add(1)
            return None
    except:
        err_transaction_invalide.add(1)
        err_montants_invalides.add(1)
        return None
    return row


t5 = time.time()

achats_clients.foreach(parsing_row3)

t6 = time.time()

# 6.3 Afficher :
#     - Les résultats par segment
#     - Le taux d'erreur global
#     - Le rapport qualité des données
print("\nRésultats par segment")
for segment in MAP_ACC.keys():
    print(" \nSegment:", segment)
    print(
        " Nombre transactions valides", MAP_ACC[segment]["transactions_valides"].value
    )
    print(" Montant total achat", MAP_ACC[segment]["montant_total"].value)
    print(
        " Montant moyen par transaction",
        MAP_ACC[segment]["montant_total"].value
        / MAP_ACC[segment]["transactions_valides"].value,
    )

nb_transactions_valides = sum(
    [MAP_ACC[segment]["transactions_valides"].value for segment in MAP_ACC.keys()]
)
montant_total = sum(
    [MAP_ACC[segment]["montant_total"].value for segment in MAP_ACC.keys()]
)

print("\nRapport Qualité")
print(" Montant total transaction valides: ", montant_total)
print(" Nombre de transactions valides: ", nb_transactions_valides)
print(" Nombre transactions invalides: ", err_transaction_invalide.value)
print(
    " Taux d'erreur (en %): ",
    round(
        err_transaction_invalide.value
        / (nb_transactions_valides + err_transaction_invalide.value)
        * 100,
        2,
    ),
)
print(" Nombre montants invalides: ", err_montants_invalides.value)
print("   Nombre montants négatifs: ", err_montants_negatifs.value)
print("   Nombre montants vides: ", err_montants_vides.value)
print(" Nombre clients inconnus: ", err_clients_inconnus.value)

# -------------------------------------------------------------
# EXERCICE 7 : COMPARAISON DE PERFORMANCE
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("EXERCICE 7 : COMPARAISON DE PERFORMANCE")
print("=" * 70)

# Comparer les approches avec et sans optimisation.


# 7.1 SANS optimisation :
#     - Jointure classique entre achats et clients
#     - Filtrage des erreurs avec plusieurs passes
def validation(row) -> bool:
    # Client inconnu
    if not row["client_id"]:
        return False
    # Montant invalide
    if not row["montant"]:
        return False
    try:
        montant = float(row["montant"])
        if montant < 0:
            return False
    except:
        return False
    return True


t7 = time.time()

achats_clients_cleaned = achats_clients.withColumn(
    "montant", spark_func.col("montant").cast(DoubleType())
).filter((spark_func.col("montant") > 0) & (spark_func.col("client_id").isNotNull()))
achats_clients_cleaned.groupBy("segment").agg(
    spark_func.sum("montant").alias("montant_total"),
    spark_func.avg("montant").alias("avg_montant"),
).show()

t8 = time.time()

# 7.2 AVEC optimisation :
#     - Broadcast pour la jointure
#     - Accumulators pour le comptage d'erreurs

# 7.3 Mesurer et comparer les temps d'exécution
time_with_optimisation = t1 - t2 + t6 - t5
time_without_optimisation = t4 - t3 + t8 - t7
print("\nComparison")
print(" AVEC optimisation: ", t1 - t2 + t6 - t5)
print(" SANS optimisation: ", t4 - t3 + t8 - t7)
print(
    " gain (en %): ",
    round(
        (time_without_optimisation - time_with_optimisation)
        / time_without_optimisation
        * 100,
        2,
    ),
)

# Fermeture
spark.stop()
print("\n✅ TP terminé !")
