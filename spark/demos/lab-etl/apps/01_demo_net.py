import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder

spark = builder.appName("demo_net").master("spark://spark-master:7077").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("/data/ventes.csv", header=True, inferSchema=True)

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

# Problème 1 : Valeur nulles dans la colonne 'produit'
print("\nProduct NULL:")
df.filter(spark_func.col("produit").isNull()).show()

# Solution : supprimer les lignes
df = df.filter(spark_func.col("produit").isNotNull())

# Problème 2 : valeurs négatives dans 'quantite'
print("\nQuantity negative:")
df.filter(spark_func.col("quantite") < 0).show()

# Solution: Remplacer la valeur absolue
df = df.withColumn(
    "quantite",
    spark_func.when(
        spark_func.col("quantite") < 0,
        spark_func.abs(spark_func.col("quantite")),
    ).otherwise(spark_func.col("quantite")),
)

# Problème 3: Quantité à 0
print("\nQuantity 0:")
df.filter(spark_func.col("quantite") == 0).show()

# Solution : Supprimer les lignes
df = df.filter(spark_func.col("quantite") > 0)

# Problème 4 : Valeur nulle dans client
print("\nClient NULL:")
df.filter(spark_func.col("client").isNull()).show()

# Solution: Remplacer par 'client_anonyme'
df = df.withColumn(
    "client",
    spark_func.when(
        (spark_func.col("client").isNull())
        | (spark_func.col("client") == "NULL")
        | (spark_func.trim(spark_func.col("client")) == ""),
        "client_anonyme",
    ).otherwise(spark_func.col("client")),
)

# Problème 5 : Date manquante
print("\nDate NULL:")
df.filter(spark_func.col("date").isNull()).show()

# Solution : Supprimer les lignes
df = df.filter(spark_func.col("date").isNotNull())

# Problème 6 : Prix unitaire null
print("\nDate NULL:")
df.filter(spark_func.col("prix_unitaire").isNull()).show()

# Solution: Calculer le prix moyen
prix_moyen = (
    df.groupBy("produit")
    .agg({"prix_unitaire": "avg"})
    .withColumnRenamed("avg(prix_unitaire)", "prix_moyen")
)
df = df.join(prix_moyen, "produit", "left")
df = df.withColumn(
    "prix_unitaire",
    spark_func.coalesce(spark_func.col("prix_unitaire"), spark_func.col("prix_moyen")),
).drop(spark_func.col("prix_moyen"))

# DataFrame cleaned
print("\nDataFrame Cleaned:")
df.show()

# Sauvegarde du DataFrame cleaned
df.write.mode("overwrite").option("header", "true").csv("/data/ventes_cleaned")

spark.stop()
