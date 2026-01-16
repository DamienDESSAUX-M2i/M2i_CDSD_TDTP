import random
import time

import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder

spark = (
    builder.appName("demo_broadcast_comparison")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

transactions_data = [
    (
        i,
        f"P{random.randint(1, 100):03d}",
        f"C{random.randint(1, 1000):04d}",
        random.choice(["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]),
        round(random.uniform(10, 500), 2),
        random.randint(1, 10),
    )
    for i in range(2_000_000)
]

transactions = spark.createDataFrame(
    transactions_data,
    ["transaction_id", "produit_id", "client_id", "ville", "montant", "quantite"],
).repartition(12)

transactions.cache()
nb_transactions = transactions.count()

products_data = [
    (
        f"P{i:03d}",
        f"Produit {i}",
        f"Cat_{i % 10}",
        round(random.uniform(5, 100), 2),
        round(random.uniform(0, 1), 2),
    )
    for i in range(1, 101)
]

products = spark.createDataFrame(
    products_data,
    ["produit_id", "nom_produit", "categorie", "prix_achat", "taux_marge"],
)

products.cache()
nb_products = products.count()

print(f"\n Transactions: {nb_transactions:,} lignes")
print(f" Produits: {nb_products} lignes")


print("\n" + "=" * 60)
print("TEST 1 : JOIN SANS BROADCAST (Shuffle Join)")
print("=" * 60)

start = time.time()

result_shuffle = (
    transactions.join(
        products,
        on="produit_id",
        how="inner",
    )
    .groupBy("categorie")
    .agg(
        spark_func.sum(spark_func.col("montant") * spark_func.col("quantite")).alias(
            "ca_total"
        ),
        spark_func.count("*").alias("nb_ventes"),
    )
)

result_shuffle.collect()
temps_shuffle = time.time() - start

print(f"\n Temps SANS broadcast: {temps_shuffle:.2f} secondes")


print("\n" + "=" * 60)
print("TEST 1 : JOIN AVEC BROADCAST (Shuffle Join)")
print("=" * 60)

start = time.time()

result_broadcast = (
    transactions.join(
        spark_func.broadcast(products),
        on="produit_id",
        how="inner",
    )
    .groupBy("categorie")
    .agg(
        spark_func.sum(spark_func.col("montant") * spark_func.col("quantite")).alias(
            "ca_total"
        ),
        spark_func.count("*").alias("nb_ventes"),
    )
)

result_broadcast.collect()
temps_broadcast = time.time() - start

print(f"\n Temps AVEC broadcast: {temps_broadcast:.2f} secondes")
