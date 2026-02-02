import os
import sys
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, TimestampType

# Configuration des chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output", "air_quality_clean")

AIR_QUALITY_PATH = os.path.join(DATA_DIR, "air_quality_raw.csv")
STATIONS_PATH = os.path.join(DATA_DIR, "stations.csv")


def create_spark_session():
    """Cree et configure la session Spark."""
    spark = (
        SparkSession.builder.appName("TP Qualite Air - Nettoyage")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark


def parse_multi_format_timestamp(timestamp_str):
    """
    UDF pour parser les timestamps multi-formats.
    Formats supportes:
    - %Y-%m-%d %H:%M:%S (ISO)
    - %d/%m/%Y %H:%M (FR)
    - %m/%d/%Y %H:%M:%S (US)
    - %Y-%m-%dT%H:%M:%S (ISO avec T)
    """
    if timestamp_str is None:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    return None


def clean_value(value_str):
    """
    UDF pour nettoyer les valeurs numeriques.
    - Remplace la virgule par un point
    - Retourne None pour les valeurs non numeriques
    """
    if value_str is None:
        return None

    try:
        # Remplacer virgule par point
        clean_str = value_str.replace(",", ".")
        return float(clean_str)
    except (ValueError, AttributeError):
        return None


def main():
    # Creer la session Spark
    spark = create_spark_session()
    print(f"Spark version: {spark.version}")

    # Enregistrer les UDFs
    parse_timestamp_udf = F.udf(parse_multi_format_timestamp, TimestampType())
    clean_value_udf = F.udf(clean_value, DoubleType())

    # Charger les donnees brutes
    print("\n[1/6] Chargement des donnees brutes...")
    df_raw = spark.read.option("header", "true").csv(AIR_QUALITY_PATH)

    initial_count = df_raw.count()
    print(f"  Lignes en entree: {initial_count:,}")

    # Charger les stations pour avoir la capacite
    df_stations = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(STATIONS_PATH)
    )

    # Parser les timestamps multi-formats
    print("\n[2/6] Parsing des timestamps multi-formats...")
    df_with_timestamp = df_raw.withColumn(
        "timestamp_parsed", parse_timestamp_udf(F.col("timestamp"))
    )

    # Filtrer les timestamps invalides
    invalid_timestamps = df_with_timestamp.filter(
        F.col("timestamp_parsed").isNull()
    ).count()
    df_with_timestamp = df_with_timestamp.filter(F.col("timestamp_parsed").isNotNull())
    print(f"  Timestamps invalides supprimes: {invalid_timestamps:,}")

    # Convertir les valeurs avec virgule decimale en float
    print("\n[3/6] Conversion des valeurs numeriques...")
    df_with_values = df_with_timestamp.withColumn(
        "value_clean", clean_value_udf(F.col("value"))
    )

    # Filtrer les valeurs non numeriques
    invalid_values = df_with_values.filter(F.col("value_clean").isNull()).count()
    df_with_values = df_with_values.filter(F.col("value_clean").isNotNull())
    print(f"  Valeurs non numeriques supprimees: {invalid_values:,}")

    # Supprimer les valeurs negatives et les outliers (>1000 ug/m3)
    print("\n[4/6] Suppression des valeurs aberrantes...")
    negative_count = df_with_values.filter(F.col("value_clean") < 0).count()
    outlier_count = df_with_values.filter(F.col("value_clean") > 1000).count()

    df_clean = df_with_values.filter(
        (F.col("value_clean") >= 0) & (F.col("value_clean") <= 1000)
    )
    print(f"  Valeurs negatives supprimees: {negative_count:,}")
    print(f"  Outliers (>1000) supprimes: {outlier_count:,}")

    # Dedupliquer sur (station_id, timestamp, pollutant)
    print("\n[5/6] Deduplication...")
    before_dedup = df_clean.count()
    df_dedup = df_clean.dropDuplicates(["station_id", "timestamp_parsed", "pollutant"])
    after_dedup = df_dedup.count()
    duplicates_removed = before_dedup - after_dedup
    print(f"  Doublons supprimes: {duplicates_removed:,}")

    # Calculer les moyennes horaires par station et polluant
    print("\n[6/6] Agregation horaire et sauvegarde...")

    # Ajouter les colonnes de temps
    df_with_time = (
        df_dedup.withColumn("date", F.to_date(F.col("timestamp_parsed")))
        .withColumn("hour", F.hour(F.col("timestamp_parsed")))
        .withColumn("year", F.year(F.col("timestamp_parsed")))
        .withColumn("month", F.month(F.col("timestamp_parsed")))
    )

    # Agreger par heure
    df_hourly = df_with_time.groupBy(
        "station_id", "pollutant", "unit", "date", "hour", "year", "month"
    ).agg(
        F.round(F.mean("value_clean"), 2).alias("value_mean"),
        F.round(F.min("value_clean"), 2).alias("value_min"),
        F.round(F.max("value_clean"), 2).alias("value_max"),
        F.count("*").alias("measurement_count"),
    )

    # Joindre avec les informations des stations
    df_final = df_hourly.join(
        df_stations.select("station_id", "station_name", "city", "station_type"),
        on="station_id",
        how="left",
    )

    # Sauvegarder en Parquet partitionne par date
    # os.makedirs(OUTPUT_DIR, exist_ok=True)

    df_final.write.mode("overwrite").partitionBy("date").parquet(
        "/output/air_quality_clean"
    )

    final_count = df_final.count()

    # Rapport final
    print("RAPPORT DE NETTOYAGE")
    print(f"Lignes en entree:              {initial_count:>12,}")
    print(f"Timestamps invalides:          {invalid_timestamps:>12,}")
    print(f"Valeurs non numeriques:        {invalid_values:>12,}")
    print(f"Valeurs negatives:             {negative_count:>12,}")
    print(f"Outliers (>1000):              {outlier_count:>12,}")
    print(f"Doublons:                      {duplicates_removed:>12,}")
    total_removed = (
        invalid_timestamps
        + invalid_values
        + negative_count
        + outlier_count
        + duplicates_removed
    )
    print(f"Total lignes supprimees:       {total_removed:>12,}")
    print(f"Lignes apres agregation:       {final_count:>12,}")
    print(f"\nFichiers Parquet sauvegardes dans: {OUTPUT_DIR}")

    # Afficher un apercu
    print("\nApercu des donnees nettoyees:")
    df_final.show(10)

    # Statistiques par polluant
    print("\nStatistiques par polluant:")
    df_final.groupBy("pollutant").agg(
        F.count("*").alias("records"),
        F.round(F.mean("value_mean"), 2).alias("avg_value"),
        F.round(F.min("value_min"), 2).alias("min_value"),
        F.round(F.max("value_max"), 2).alias("max_value"),
    ).orderBy("pollutant").show()

    # Fermer Spark
    spark.stop()


if __name__ == "__main__":
    main()
