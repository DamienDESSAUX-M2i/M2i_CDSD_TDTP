from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, coalesce, lit, trim, abs as spark_abs

# Initialisation
spark = SparkSession.builder \
    .appName("TP_Broadcast_Accumulator_Correction") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext


# Chargement
df = spark.read.csv("/data/commandes_ecommerce.csv", header=True, inferSchema=True)

df.show(10)
print(f"Lignes initiales : {df.count()}")

for column in df.columns:
    null_count = df.filter(col(column).isNull()).count()
    print(f"{column} : {null_count} nulls")


# 1. Supprimer les lignes sans produit
df_cleaned = df.filter(col("produit").isNotNull())

# 2. Corriger les quantités négatives (valeur absolue)
df_cleaned = df_cleaned.withColumn(
    "quantite",
    when(col("quantite") < 0, spark_abs(col("quantite")))
    .otherwise(col("quantite"))
)

# 3. Supprimer les quantités nulles ou zéro
df_cleaned = df_cleaned.filter(
    (col("quantite") > 0) & (col("quantite").isNotNull())
)

# 4. Remplacer les clients invalides par "Client Anonyme"
df_cleaned = df_cleaned.withColumn(
    "client",
    when(
        col("client").isNull() | 
        (col("client") == "NULL") | 
        (trim(col("client")) == ""),
        "Client Anonyme"
    ).otherwise(col("client"))
)


# 5. Imputer les prix manquants avec la moyenne par produit

# 5.1 Calculer le prix moyen par produit
prix_moyens = df_cleaned.groupBy("produit") \
    .agg({"prix_unitaire": "avg"}) \
    .withColumnRenamed("avg(prix_unitaire)", "prix_moyen")

# 5.2 Joindre avec le DataFrame principal
df_cleaned = df_cleaned.join(prix_moyens, on="produit", how="left")

# 5.3 Remplacer les prix nulls par la moyenne
df_cleaned = df_cleaned.withColumn(
    "prix_unitaire",
    coalesce(col("prix_unitaire"), col("prix_moyen"))
).drop("prix_moyen")

# 6. Supprimer les lignes sans date
df_cleaned = df_cleaned.filter(col("date").isNotNull())

# 7. Remplacer les régions nulles par "Non spécifiée"
df_cleaned = df_cleaned.withColumn(
    "region",
    when(col("region").isNull(), "Non spécifiée")
    .otherwise(col("region"))
)

# 8. Ajouter une colonne montant_total (quantite * prix_unitaire)
df_cleaned = df_cleaned.withColumn(
    "montant_total",
    col("quantite") * col("prix_unitaire")
)

df_cleaned.show()

# Sauvegarde
df_cleaned.write.mode("overwrite").option("header", "true").csv("/data/output/commandes_clean")

spark.stop()