import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder

spark = (
    builder.appName("demo_read_csv")
    .master("spark://spark-master:7077")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

transactions = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv("/data/transactions.csv")
)

transactions.printSchema()

transactions.show(10)

transactions.groupBy("ville").agg(
    spark_func.count("*").alias("nb_transactions"),
    spark_func.sum("montant").alias("ca_total"),
    spark_func.avg("montant").alias("panier_moyen"),
).orderBy(spark_func.col("ca_total").desc()).show()
