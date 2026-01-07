from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, max, min

spark = SparkSession.builder.master("local").appName("exo3").getOrCreate()

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/housing.csv")
)

# 1. Calculer min, max, moyenne pour median_house_value
df.select(
    min("median_house_value").alias("min_median_house_value"),
    max("median_house_value").alias("max_median_house_value"),
    avg("median_house_value").alias("avg_median_house_value"),
).show()

# 2. Calculer min, max, moyenne pour median_income
df.select(
    min("median_income").alias("min_median_income"),
    max("median_income").alias("max_median_income"),
    avg("median_income").alias("avg_median_income"),
).show()

# 3. Calculer min, max, moyenne pour housing_median_age
df.select(
    min("housing_median_age").alias("min_housing_median_age"),
    max("housing_median_age").alias("max_housing_median_age"),
    avg("housing_median_age").alias("avg_housing_median_age"),
).show()

# 4. Compter combien de districts ont une population > 5000
result = df.filter(col("population") > 5000).count()
print(f"Le nombre de districts ayant une population supérieure à 5000 est {result}.")

# 5. Prix moyen des maisons par type de proximité océan
df.groupby("ocean_proximity").agg(
    avg("median_house_value").alias("avg_median_house_value")
).sort("avg_median_house_value").show()

# 6. Revenu moyen par type de proximité océan
df.groupby("ocean_proximity").agg(avg("median_income").alias("avg_median_income")).sort(
    "avg_median_income"
).show()

# 7. Âge moyen des maisons par type de proximité océan
df.groupby("ocean_proximity").agg(
    avg("housing_median_age").alias("avg_housing_median_age")
).sort("avg_housing_median_age").show()

# 8. Population moyenne par type de proximité océan
df.groupby("ocean_proximity").agg(avg("population").alias("avg_population")).sort(
    col("avg_population").desc()
).show()
