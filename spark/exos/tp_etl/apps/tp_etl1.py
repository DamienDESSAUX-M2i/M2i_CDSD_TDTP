import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession

# Initialisation
builder: SparkSession.Builder = SparkSession.builder
spark = builder.appName("tp_etl1").master("spark://spark-master:7077").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Chargement
df = spark.read.csv("/data/commandes_ecommerce.csv", header=True, inferSchema=True)

print("\nSchema:")
df.printSchema()

print("\nStatistics NULL:")
df.select(
    [
        spark_func.count(spark_func.when(spark_func.col(c).isNull(), c)).alias(
            c + "_null"
        )
        for c in df.columns
    ]
).show()

print("\nDataFrame:")
df.show()

# 1. Supprimer les lignes sans produit
print("\nProduct NULL:")
df.filter(spark_func.col("produit").isNull()).show()

df_cleaned = df.filter(spark_func.col("produit").isNotNull())

# 2. Corriger les quantités négatives (valeur absolue)
print("\nQuantity negative:")
df_cleaned.filter(spark_func.col("quantite") < 0).show()

df_cleaned = df_cleaned.withColumn(
    "quantite",
    spark_func.when(
        spark_func.col("quantite").cast("double") < 0,
        spark_func.abs(spark_func.col("quantite").cast("double")),
    ).otherwise(spark_func.col("quantite").cast("double")),
)

# 3. Supprimer les quantités nulles ou zéro
print("\nQuantity 0:")
df_cleaned.filter(
    (spark_func.col("quantite").isNull()) | (spark_func.col("quantite") == 0)
).show()

df_cleaned = df_cleaned.filter(
    (spark_func.col("quantite").isNotNull()) & (spark_func.col("quantite") > 0)
)

# 4. Remplacer les clients invalides par "Client Anonyme"
#    (gérer : null, "NULL", et espaces)
print("\nClient NULL:")
df_cleaned.filter(
    (spark_func.col("client").isNull())
    | (spark_func.col("client") == "NULL")
    | (spark_func.trim(spark_func.col("client")) == "")
).show()

df_cleaned = df_cleaned.withColumn(
    "client",
    spark_func.when(
        (spark_func.col("client").isNull())
        | (spark_func.col("client") == "NULL")
        | (spark_func.trim(spark_func.col("client")) == ""),
        "client_anonyme",
    ).otherwise(spark_func.col("client")),
)

# 5. Imputer les prix manquants avec la moyenne par produit
print("\nDate NULL:")
df_cleaned.filter(spark_func.col("prix_unitaire").isNull()).show()

prix_moyen = (
    df_cleaned.groupBy("produit")
    .agg({"prix_unitaire": "avg"})
    .withColumnRenamed("avg(prix_unitaire)", "prix_moyen")
)
df_cleaned = df_cleaned.join(prix_moyen, "produit", "left")
df_cleaned = df_cleaned.withColumn(
    "prix_unitaire",
    spark_func.coalesce(spark_func.col("prix_unitaire"), spark_func.col("prix_moyen")),
).drop(spark_func.col("prix_moyen"))

# 6. Supprimer les lignes sans date
print("\nDate NULL:")
df_cleaned.filter(spark_func.col("date").isNull()).show()

df_cleaned = df_cleaned.filter(spark_func.col("date").isNotNull())

# 7. Remplacer les régions nulles par "Non spécifiée"
print("\nRegion NULL:")
df_cleaned.filter(spark_func.col("region").isNull()).show()

df_cleaned = df_cleaned.withColumn(
    "region",
    spark_func.when(
        spark_func.col("region").isNull(),
        "Non spécifiée",
    ).otherwise(spark_func.col("region")),
)

# 8. Ajouter une colonne montant_total (quantite * prix_unitaire)
df_cleaned = df_cleaned.withColumn(
    "montant_total", spark_func.col("quantite") * spark_func.col("prix_unitaire")
)

# Sauvegarde
print("\nDataFrame clean:")
df_cleaned.show()

df_cleaned.write.mode("overwrite").option("header", "true").csv(
    "/data/commandes_ecommerce_clean"
)

spark.stop()
