import random
import time

from pyspark.accumulators import AccumulatorParam
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder

spark = (
    builder.appName("BroadcastComparison")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

sc = spark.sparkContext

donnees = sc.parallelize(range(1, 1_000_001), numSlices=8)

donnees.cache()

donnees.count()


print("\n SCÉNARIO 1 : Calculer nb_pairs et nb_impairs")

print("\n SANS ACCUMULATOR (2 jobs séparés) :")


start = time.time()

nb_pairs_v1 = donnees.filter(lambda x: x % 2 == 0).count()

nb_impairs_v1 = donnees.filter(lambda x: x % 2 != 0).count()

temps_sans = time.time() - start

print(f"   Pairs: {nb_pairs_v1:,}")
print(f"   Impairs: {nb_impairs_v1:,}")
print(f"   ⏱ Temps: {temps_sans:.2f}s")


print("\n AVEC ACCUMULATOR (1 seul job) :")

compteur_pairs = sc.accumulator(0)

compteur_impairs = sc.accumulator(0)

start = time.time()


def compter(x):
    if x % 2 == 0:
        compteur_pairs.add(1)
    else:
        compteur_impairs.add(1)
    return x


donnees.map(compter).count()

temps_avec = time.time() - start

print(f"   Pairs: {compteur_pairs.value:,}")
print(f"   Impairs: {compteur_impairs.value:,}")
print(f"   ⏱ Temps: {temps_avec:.2f}s")

if temps_sans > temps_avec:
    print(f"\n Gain: {(1 - temps_avec / temps_sans) * 100:.1f}%")


print("\n SCÉNARIO 2 : Calculer somme, moyenne, min, max, count")

print("\n SANS ACCUMULATOR (4 jobs séparés) :")

start = time.time()

total_v1 = donnees.sum()
count_v1 = donnees.count()
min_v1 = donnees.min()
max_v1 = donnees.max()
moyenne_v1 = total_v1 / count_v1  # pas de job

temps_sans = time.time() - start

print(f"   Count: {count_v1:,}")
print(f"   Somme: {total_v1:,}")
print(f"   Moyenne: {moyenne_v1:,.2f}")
print(f"   Min: {min_v1}")
print(f"   Max: {max_v1}")
print(f"   ⏱ Temps: {temps_sans:.2f}s")


print("\n AVEC ACCUMULATOR (1 job séparé) :")


class MinAccumulator(AccumulatorParam):
    def zero(self, v):
        return float("inf")

    def addInPlace(self, v1, v2):
        return min(v1, v2)


class MaxAccumulator(AccumulatorParam):
    def zero(self, v):
        return float("-inf")

    def addInPlace(self, v1, v2):
        return max(v1, v2)


acc_min = sc.accumulator(float("inf"), MinAccumulator())
acc_max = sc.accumulator(float("-inf"), MaxAccumulator())
acc_count = sc.accumulator(0)
acc_somme = sc.accumulator(0)

start = time.time()


def collecter_stats(x):
    acc_min.add(x)
    acc_max.add(x)
    acc_count.add(1)
    acc_somme.add(x)
    return x


donnees.map(collecter_stats).count()

moyenne_v2 = acc_somme.value / acc_count.value

temps_avec = time.time() - start

print(f"   Count: {acc_count.value:,}")
print(f"   Somme: {acc_somme.value:,}")
print(f"   Moyenne: {moyenne_v2:,.2f}")
print(f"   Min: {acc_min.value}")
print(f"   Max: {acc_max.value}")
print(f"   ⏱ Temps: {temps_avec:.2f}s")


if temps_sans > temps_avec:
    print(f"\n Gain: {(1 - temps_avec / temps_sans) * 100:.1f}%")
