from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, lit, max, min

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("demo-df").getOrCreate()

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv(
        "C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/friends-with-header.csv"
    )
)

df.show()

# Sélection colonne
df.select("name", "age").show()

# Filtre
df.filter(col("age") > 35).show()
df.filter((col("age") > 35) & (col("friendsNumber") > 35)).show()
listPrenoms = ["Ben", "Will"]
df.filter(col("name").isin(listPrenoms)).sort("name").show()

# Ajout colonne
dfWithBirthYear = df.withColumn("BirthYear", lit(datetime.now().year) - col("age"))
dfWithBirthYear.show()

# Aggregation
df.select(
    min("age").alias("age_min"),
    max("age").alias("age_max"),
    avg("age").alias("age_avg"),
).show()
