from datetime import datetime

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, TimestampType

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.master("spark://spark-master:7077")
    .appName("02_nettoyage_spark")
    .getOrCreate()
)

air_quality = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/air_quality_raw.csv")
)


# Parser les timestamps multi-formats avec une UDF Spark.
def parse_timestamp(timestamp_str: str) -> datetime:
    formats = [
        "%Y-%m-%d %H:%M:%S",  # ISO
        "%d/%m/%Y %H:%M",  # FR
        "%m/%d/%Y %H:%M:%S",  # US
        "%Y-%m-%dT%H:%M:%S",  # ISO avec T
    ]

    for format in formats:
        try:
            timestamp = datetime.strptime(timestamp_str, format)
            return timestamp
        except:
            pass

    return None


parseTimestamp = F.udf(parse_timestamp, TimestampType())

air_quality_cleaned = air_quality.withColumn(
    "timestamp",
    parseTimestamp(F.col("timestamp")),
)

# Convertir les valeurs avec virgule décimale en float.
air_quality_cleaned = air_quality_cleaned.withColumn(
    "value", F.col("value").cast(DoubleType())
)

# Supprimer les valeurs négatives et les outliers (>1000 ug/m3).
air_quality_cleaned = air_quality_cleaned.filter(
    (F.col("value") >= 0) & (F.col("value") <= 1000)
)

# Dédupliquer sur `(station_id, timestamp, pollutant)`.
air_quality_cleaned = air_quality_cleaned.drop_duplicates(
    ["station_id", "timestamp", "pollutant"]
)

# Calculer les moyennes horaires par station et polluant.
mean_hour = (
    air_quality_cleaned.withColumn(
        "trunc_hour",
        F.date_trunc("hour", "timestamp"),
    )
    .groupBy(["station_id", "pollutant", "trunc_hour"])
    .agg(F.avg("value").alias("mean_value"))
    .orderBy(
        "station_id",
        "pollutant",
        "trunc_hour",
    )
)
mean_hour.show()

# Sauvegarder en Parquet partitionné par `date`.
air_quality_cleaned = air_quality_cleaned.withColumn(
    "trunc_date",
    F.date_trunc("day", "timestamp"),
)

air_quality_cleaned.write.mode("overwrite").option("header", "true").partitionBy(
    "trunc_date"
).parquet("/output/air_quality_clean/")

# Rapport : lignes en entrée, lignes supprimées, lignes en sortie.
count_air_quality = air_quality.count()
count_air_quality_cleaned = air_quality_cleaned.count()
print("\nRAPPORT")
print(" Nombre de lignes dans le dataset air_quality_raw : ", count_air_quality)
print(" Nombre de lignes supprimées : ", count_air_quality - count_air_quality_cleaned)
print(
    " Nombre de lignes dans le dataset air_quality_clean : ", count_air_quality_cleaned
)

# >>> RAPPORT
# >>>  Nombre de lignes dans le dataset air_quality_raw :  1230951
# >>>  Nombre de lignes supprimées :  231439
# >>>  Nombre de lignes dans le dataset air_quality_clean :  999512

spark.stop()
