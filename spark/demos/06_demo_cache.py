import time

from pyspark import StorageLevel
from pyspark.sql import SparkSession

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("demo_cache").getOrCreate()

storageLevelDict = {
    # Mémoire RAM uniquement
    # Avantage : accés rapide
    # Inconvénients : Risque de perte si pas assez de mémoire, consomme beaucoup de mémoire
    # Usage : Dataset petit/moyen <1Go seulement si RAM suffisante
    "MEMORY_ONLY": StorageLevel.MEMORY_ONLY,
    # Mémoire RAM et DISK
    # Avantage : Plus sécurisé, bon compromis perf/sécurité
    # Inconvénient : Plus lent
    # Usage : Recommandé la plupart du temps
    "MEMORY_AND_DISK": StorageLevel.MEMORY_AND_DISK,
    # Mémoire RAM uniquement sous forme compréssée
    # Avantage : Economise de la RAM (10x moins)
    # Inconvénient : Risque de perte lors de la compression/décompression
    # Usage : Dataset volumineux
    # "MEMORY_ONLY_SER" : StorageLevel.MEMORY_ONLY_SER # /!\ Non disponible en Python
    # Mémoire RAM uniquement avec un réplicat
    # Avantage : Tolérance aux pannes
    # Inconvénient : Double la concommation de la RAM
    # Usage : Dataset semsible
    "MEMORY_ONLY_2": StorageLevel.MEMORY_ONLY_2,
}

numberRDD = spark.sparkContext.parallelize(range(1, 1000))

expensiveRDD = (
    numberRDD.filter(lambda x: x % 2 == 0)
    .map(lambda x: x * x)
    .filter(lambda x: x > 1_000)
)

print("Sans Cache :")
t1 = time.time()
count = expensiveRDD.count()
sum1 = expensiveRDD.sum()
t2 = time.time()

print(f"Temps sans cache : {int((t2 - t1) * 1000)}ms")

print("Avec Cache :")
expensiveRDD.cache()  # defaut MEMORY_ONLY
# expensiveRDD.persist(StorageLevel.MEMORY_AND_DISK)

t1 = time.time()
count = expensiveRDD.count()
sum1 = expensiveRDD.sum()
t2 = time.time()

print(f"Temps avec cache : {int((t2 - t1) * 1000)}ms")

# Gestion du cache
spark.catalog.clearCache()
expensiveRDD.unpersist()
