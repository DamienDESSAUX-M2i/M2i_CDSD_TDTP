from pyspark.sql import SparkSession

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("exo2").getOrCreate()

# Récupérer le SparkContext
sc = spark.sparkContext

# Lecture du fichier achats_clients.csv
rdd_achats_clients = sc.textFile(
    "C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/achats_clients.csv"
)

# Afficharge 10 premières lignes
# print(rdd_achats_clients.take(10))

# Suppression du header
header = rdd_achats_clients.first()
rdd_achats_clients = rdd_achats_clients.filter(lambda line: line != header)

# Extraction de id_client et montant (1er et 3e colonnes)
rdd_extraction = rdd_achats_clients.map(
    lambda line: (line.split(",")[0], float(line.split(",")[2]))
)

# Aggregation par id_client
rdd_agg = rdd_extraction.reduceByKey(lambda x, y: x + y)

# Collecter les résultats
result = rdd_agg.collect()

for t in result:
    print(f"{t[0]}\t{t[1]}")
