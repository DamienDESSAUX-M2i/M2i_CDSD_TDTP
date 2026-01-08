from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder

# Créer une session
spark = (
    builder.master("local").appName("demo-rdd").getOrCreate()
)  # local ou spark://localhost:7000 ou hadoop://...

# Récupérer le SparkContext
sc = spark.sparkContext

# Création d'un RDD
firstRDD = sc.parallelize([1, 2, 3])

# Transformer le premier RDD
secondRDD = firstRDD.map(lambda e: e * 5)

# Collecter les résultats
result = secondRDD.collect()

print(result)
