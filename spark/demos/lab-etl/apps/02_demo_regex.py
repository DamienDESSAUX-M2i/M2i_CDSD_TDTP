import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType

builder: SparkSession.Builder = SparkSession.builder

spark = builder.appName("demo_regex").master("spark://spark-master:7077").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

data = [
    ("C001", "  jean dupont  ", "PARIS-75001", "Prix: 150€"),
    ("C002", "marie  martin", "LYON-69001", "Prix: 200€"),
    ("C003", "pierre durant  ", "MARSEILLE-13001", "Prix: 99€"),
    ("C004", "  sophie bernard", "TOULOUSE-31000", "Prix: 1250€"),
]

schema = StructType(
    [
        StructField("code", StringType(), True),
        StructField("client", StringType(), True),
        StructField("ville", StringType(), True),
        StructField("montant", StringType(), True),
    ]
)

df = spark.createDataFrame(data, schema)

print("\nDataFrame:")
df.show()

# 1. Nettoyer les espaces en trop
df = df.withColumn(
    "client",
    spark_func.regexp_replace(spark_func.trim(spark_func.col("client")), " +", " "),
)

# 2. Extraire le code postal
df = df.withColumn(
    "code_postal", spark_func.regexp_extract(spark_func.col("ville"), "(\\d{5})", 0)
)

# 3. Extraire le nom de la ville
df = df.withColumn(
    "nom_ville", spark_func.regexp_extract(spark_func.col("ville"), "^([A-Z]+)", 1)
).drop("ville")

# 4. extraire le montant
df = df.withColumn(
    "prix", spark_func.regexp_extract(spark_func.col("montant"), "(\\d+)", 0)
).drop("montant")

# 5. Mettre en forme les noms
df = df.withColumn("client", spark_func.upper(spark_func.col("client")))

df.write.mode("overwrite").parquet("/data/output/data_clean")
