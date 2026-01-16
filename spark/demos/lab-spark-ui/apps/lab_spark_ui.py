import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, desc
from pyspark.sql.functions import sum as spark_sum

spark = (
    SparkSession.builder.appName("LAB_Spark_UI_Visualisation")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "512m")
    .config("spark.executor.cores", "1")
    .config("spark.sql.shuffle.partitions", "6")
    .getOrCreate()
)


spark.sparkContext.setLogLevel("WARN")
sc = spark.sparkContext


def pause(message, duree=10):
    """Pause pour observer Spark UI"""
    print("\n" + "=" * 70)
    print(f"⏸️  {message}")
    print("=" * 70)
    print(f"⏳ Pause de {duree} secondes pour observer Spark UI...")
    time.sleep(duree)
    print("✅ On continue !\n")


def titre(texte):
    """Affiche un titre"""
    print("\n" + "=" * 70)
    print(f"🔷 {texte}")
    print("=" * 70)


titre("BIENVENUE DANS LE LAB SPARK UI")
print("""
Ce lab va te montrer comment Spark exécute les opérations :

📊 ARCHITECTURE SPARK :

    ┌───────────────────────────────────────────────────┐
    │                       DRIVER                      │
    │  (Ton programme Python - coordonne l'exécution)   │
    │  → Crée le DAG (plan d'exécution)                 │
    │  → Découpe en Jobs → Stages → Tasks               │
    │  → Distribue les tasks aux Executors              │
    └───────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │   EXECUTOR 1  │ │   EXECUTOR 2  │ │   EXECUTOR 3  │
    │   (Worker 1)  │ │   (Worker 2)  │ │   (Worker 3)  │
    │               │ │               │ │               │
    │  ┌─────────┐  │ │  ┌─────────┐  │ │  ┌─────────┐  │
    │  │ Task 1  │  │ │  │ Task 2  │  │ │  │ Task 3  │  │
    │  │ Task 4  │  │ │  │ Task 5  │  │ │  │ Task 6  │  │
    │  └─────────┘  │ │  └─────────┘  │ │  └─────────┘  │
    └───────────────┘ └───────────────┘ └───────────────┘

📌 VOCABULAIRE :
   • JOB    : Déclenché par une ACTION (count, collect, show, write...)
   • STAGE  : Groupe de transformations sans shuffle
   • TASK   : Unité de travail sur 1 partition, exécutée par 1 executor
   • SHUFFLE: Redistribution des données entre stages (coûteux !)
""")

pause(
    "Ouvre http://localhost:8080 pour voir le cluster, puis http://localhost:4040", 15
)


titre("ÉTAPE 1 : PREMIER JOB - count()")
print("""
On va créer un RDD et appeler count().

📌 CE QUI VA SE PASSER :
   1. Le Driver crée le DAG (plan d'exécution)
   2. count() est une ACTION → déclenche un JOB
   3. Le JOB est découpé en TASKS (1 par partition)
   4. Les TASKS sont envoyées aux EXECUTORS
   5. Les résultats remontent au DRIVER
""")


print("\n📊 Création d'un RDD avec 6 partitions...")
rdd = sc.parallelize(range(1, 1000001), numSlices=6)
print(f"   Nombre de partitions : {rdd.getNumPartitions()}")

pause("Observe dans Spark UI : rien ne s'est passé ! (lazy evaluation)", 8)

print("📊 Exécution de count() - ACTION qui déclenche un JOB...")
start = time.time()
resultat = rdd.count()
duree = time.time() - start

print(f"   Résultat : {resultat:,} éléments")
print(f"   Durée : {duree:.2f}s")

pause(
    """OBSERVE DANS SPARK UI (http://localhost:4040) :
   → Onglet 'Jobs' : 1 job créé (Job 0)
   → Clique sur le job pour voir les STAGES
   → Clique sur le stage pour voir les TASKS (6 tasks = 6 partitions)
   → Onglet 'Executors' : voir quel executor a traité quelles tasks""",
    15,
)


titre("ÉTAPE 2 : TRANSFORMATIONS ET DAG")
print("""
Les TRANSFORMATIONS sont lazy (pas exécutées immédiatement).
Spark construit un DAG (Directed Acyclic Graph) qui sera
exécuté lors de la prochaine ACTION.

📌 TRANSFORMATIONS À APPLIQUER :
   1. map()    → multiplier par 2
   2. filter() → garder les > 500000
   3. map()    → convertir en tuple (valeur, 1)
""")

print("\n📊 Application des transformations (lazy)...")
rdd_transforme = (
    rdd.map(lambda x: x * 2).filter(lambda x: x > 500000).map(lambda x: (x % 10, x))
)

print("   ✅ Transformations définies (mais pas exécutées !)")

pause("Observe Spark UI : toujours 1 seul job ! Les transformations sont lazy", 8)

print("📊 Exécution de count() - Déclenche le calcul du DAG complet...")
start = time.time()
resultat = rdd_transforme.count()
duree = time.time() - start

print(f"   Résultat : {resultat:,} éléments")
print(f"   Durée : {duree:.2f}s")

pause(
    """OBSERVE DANS SPARK UI :
   → Job 1 créé
   → Clique sur le job → 'DAG Visualization'
   → Tu vois le graphe : parallelize → map → filter → map → count
   → Tout est dans 1 SEUL STAGE (pas de shuffle)""",
    15,
)


titre("ÉTAPE 3 : SHUFFLE - CRÉATION DE PLUSIEURS STAGES")
print("""
Certaines opérations nécessitent un SHUFFLE (redistribution des données) :
   • reduceByKey, groupByKey
   • join, cogroup
   • sortBy, orderBy
   • repartition

📌 LE SHUFFLE :
   1. Les données sont écrites sur disque (shuffle write)
   2. Redistribuées entre executors par clé
   3. Lues par le stage suivant (shuffle read)
   → Très COÛTEUX en I/O réseau et disque !

📌 CE QUI VA SE PASSER :
   • Stage 1 : map + filter + map (narrow transformations)
   • SHUFFLE (redistribution par clé)
   • Stage 2 : reduceByKey (agrégation)
""")

print("\n📊 Opération avec SHUFFLE : reduceByKey...")
rdd_grouped = rdd.map(lambda x: (x % 5, x)).reduceByKey(lambda a, b: a + b)

start = time.time()
resultats = rdd_grouped.collect()
duree = time.time() - start

print(f"   Résultats : {resultats[:5]}...")
print(f"   Durée : {duree:.2f}s")

pause(
    """OBSERVE DANS SPARK UI :
   → Job 2 créé
   → Clique dessus : tu vois 2 STAGES !
   → Stage 0 : parallelize → map (avant shuffle)
   → Stage 1 : reduceByKey (après shuffle)
   → Dans chaque stage, clique pour voir les TASKS
   → Onglet 'Stages' : voir 'Shuffle Read' et 'Shuffle Write'""",
    20,
)


titre("ÉTAPE 4 : SHUFFLE COMPLEXE AVEC JOIN")
print("""
Un JOIN entre deux RDD crée un SHUFFLE important :
   • Les données des deux RDD sont redistribuées par clé
   • Les partitions avec la même clé se retrouvent sur le même executor

📌 CE QUI VA SE PASSER :
   • RDD 1 : utilisateurs (id, nom)
   • RDD 2 : commandes (id_user, montant)
   • JOIN sur id_user
   → 3 stages : préparation RDD1, préparation RDD2, join
""")


print("\n📊 Création des RDD...")
rdd_users = sc.parallelize(
    [(1, "Alice"), (2, "Bob"), (3, "Charlie"), (4, "David"), (5, "Eve"), (6, "Frank")],
    numSlices=3,
)

rdd_commandes = sc.parallelize(
    [
        (1, 100),
        (1, 200),
        (2, 150),
        (2, 300),
        (3, 250),
        (4, 175),
        (5, 400),
        (5, 125),
        (6, 350),
        (1, 275),
    ],
    numSlices=3,
)

print("   RDD users : 6 utilisateurs")
print("   RDD commandes : 10 commandes")

print("\n📊 JOIN des deux RDD...")
start = time.time()
rdd_join = rdd_users.join(rdd_commandes)
resultats = rdd_join.collect()
duree = time.time() - start

print(f"   Résultats du join : {len(resultats)} lignes")
for r in resultats[:5]:
    print(f"      User {r[0]}: {r[1][0]} → {r[1][1]}€")
print(f"   Durée : {duree:.2f}s")

pause(
    """OBSERVE DANS SPARK UI :
   → Nouveau job avec PLUSIEURS STAGES
   → Le DAG montre les 2 RDD qui convergent vers le join
   → Observe le 'Shuffle Read Size' dans les stages
   → Compare la taille des données avant/après shuffle""",
    15,
)


titre("ÉTAPE 5 : VISUALISER L'EFFET DU CACHE")
print("""
Sans CACHE, chaque action recalcule tout le DAG.
Avec CACHE, le résultat est stocké en mémoire.

📌 CE QU'ON VA FAIRE :
   1. Créer un RDD avec transformations coûteuses
   2. Exécuter 3 actions SANS cache → 3 recalculs
   3. Mettre en cache
   4. Exécuter 3 actions AVEC cache → 1 calcul + 2 lectures
""")


print("\n📊 Création du RDD avec transformations...")
rdd_complexe = (
    sc.parallelize(range(1, 500001), numSlices=6)
    .map(lambda x: (x % 100, x * 2))
    .filter(lambda x: x[1] > 100000)
)


print("\n🔴 SANS CACHE - 3 actions successives...")
start = time.time()
count1 = rdd_complexe.count()
sum1 = rdd_complexe.map(lambda x: x[1]).sum()
max1 = rdd_complexe.map(lambda x: x[1]).max()
duree_sans = time.time() - start
print(f"   Count: {count1}, Sum: {sum1}, Max: {max1}")
print(f"   Durée totale : {duree_sans:.2f}s")

pause(
    """OBSERVE DANS SPARK UI :
   → 3 nouveaux JOBS créés (un par action)
   → Chaque job recalcule TOUT le DAG
   → Pas de données en cache (onglet 'Storage' vide)""",
    15,
)


print("\n🟢 AVEC CACHE - 3 actions successives...")
rdd_cache = (
    sc.parallelize(range(1, 500001), numSlices=6)
    .map(lambda x: (x % 100, x * 2))
    .filter(lambda x: x[1] > 100000)
)

rdd_cache.cache()
print("   ✅ RDD marqué pour cache")

start = time.time()
count2 = rdd_cache.count()
sum2 = rdd_cache.map(lambda x: x[1]).sum()
max2 = rdd_cache.map(lambda x: x[1]).max()
duree_avec = time.time() - start
print(f"   Count: {count2}, Sum: {sum2}, Max: {max2}")
print(f"   Durée totale : {duree_avec:.2f}s")

if duree_sans > duree_avec:
    print(f"\n   🚀 Gain avec cache : {(1 - duree_avec / duree_sans) * 100:.1f}%")

pause(
    """OBSERVE DANS SPARK UI :
   → Onglet 'Storage' : le RDD est maintenant en cache !
   → Tu vois la taille en mémoire et le % mis en cache
   → Les jobs suivants sont plus rapides (lisent le cache)
   → Dans le DAG, une icône verte indique le cache""",
    15,
)


rdd_cache.unpersist()


titre("ÉTAPE 6 : DATAFRAME - PLAN D'EXÉCUTION CATALYST")
print("""
Avec les DataFrames, Spark utilise l'optimiseur CATALYST
qui crée un plan d'exécution optimisé.

📌 TU PEUX VOIR :
   • Le plan LOGIQUE (ce que tu as demandé)
   • Le plan PHYSIQUE (comment Spark va l'exécuter)
   • Les optimisations appliquées (predicate pushdown, etc.)
""")


print("\n📊 Création d'un DataFrame de ventes...")
data = [
    (
        f"client_{i}",
        f"produit_{i % 10}",
        i * 10.5,
        "2024-01-" + str((i % 28) + 1).zfill(2),
    )
    for i in range(1, 10001)
]

df = spark.createDataFrame(data, ["client", "produit", "montant", "date"])
print(f"   {df.count()} lignes créées")


print("\n📊 Requête complexe : top 5 clients par montant total...")
df_result = (
    df.filter(col("montant") > 50)
    .groupBy("client")
    .agg(
        spark_sum("montant").alias("total"),
        count("*").alias("nb_achats"),
        avg("montant").alias("moyenne"),
    )
    .orderBy(desc("total"))
    .limit(5)
)


print("\n📋 PLAN D'EXÉCUTION :")
df_result.explain(mode="extended")


print("\n📊 Résultat :")
df_result.show()

pause(
    """OBSERVE DANS SPARK UI :
   → Onglet 'SQL' : tu vois la requête et son plan
   → Clique sur la requête pour voir le DAG détaillé
   → Les opérations sont optimisées par Catalyst
   → Tu vois les métriques : lignes lues, shuffles, etc.""",
    15,
)


titre("ÉTAPE 7 : BROADCAST JOIN VS SHUFFLE JOIN")
print("""
Quand tu fais un JOIN, Spark peut utiliser :
   • SHUFFLE JOIN : redistribue les deux tables (coûteux)
   • BROADCAST JOIN : envoie la petite table à tous les executors

📌 BROADCAST JOIN :
   • Pas de shuffle de la grande table
   • La petite table est copiée sur chaque executor
   • Beaucoup plus rapide !
""")


print("\n📊 Création des tables...")
df_ventes = spark.createDataFrame(
    [(i, f"P{i % 20}", i * 1.5) for i in range(1, 100001)],
    ["vente_id", "produit_id", "montant"],
)
print(f"   Table ventes : {df_ventes.count()} lignes")


df_produits = spark.createDataFrame(
    [(f"P{i}", f"Produit {i}", f"Cat{i % 5}") for i in range(20)],
    ["produit_id", "nom_produit", "categorie"],
)
print(f"   Table produits : {df_produits.count()} lignes")


from pyspark.sql.functions import broadcast

print("\n📊 BROADCAST JOIN...")
start = time.time()
df_join = df_ventes.join(broadcast(df_produits), "produit_id")
count_join = df_join.count()
duree = time.time() - start
print(f"   Résultat : {count_join} lignes en {duree:.2f}s")

pause(
    """OBSERVE DANS SPARK UI :
   → Onglet 'SQL' : clique sur la dernière requête
   → Dans le plan, tu vois 'BroadcastHashJoin'
   → Pas de shuffle de la grande table !
   → Compare avec un shuffle join (désactive broadcast)""",
    15,
)


titre("ÉTAPE 8 : OBSERVER LES EXECUTORS EN ACTION")
print("""
On va lancer un job LONG pour observer les executors travailler.

📌 OBSERVE :
   • Onglet 'Executors' : CPU, mémoire, tasks en cours
   • Onglet 'Stages' → clique sur un stage actif
   • Tu vois les tasks s'exécuter en temps réel !
   • La barre de progression des tasks
""")

print("\n📊 Lancement d'un job long (20 partitions)...")
import time as t


def travail_lent(x):
    """Simule un traitement lent"""
    t.sleep(0.01)
    return x * 2


rdd_long = sc.parallelize(range(1, 5001), numSlices=20)

print("   Job en cours... observe les executors !")
start = time.time()
resultat = rdd_long.map(travail_lent).count()
duree = time.time() - start

print(f"   Terminé : {resultat} éléments en {duree:.2f}s")

pause(
    """AS-TU OBSERVÉ ?
   → Les tasks se distribuent sur les 3 workers
   → Certains executors terminent avant d'autres (data skew)
   → Le temps total = temps du plus lent executor""",
    10,
)


titre("RÉSUMÉ - CE QUE TU AS APPRIS")
print("""
📊 ARCHITECTURE :
   • DRIVER : coordonne, crée le DAG, distribue les tasks
   • EXECUTOR : exécute les tasks, stocke les données en cache
   • TASK : unité de travail sur 1 partition

📊 EXÉCUTION :
   • ACTION → déclenche un JOB
   • JOB → découpé en STAGES (séparés par les shuffles)
   • STAGE → contient des TASKS (1 par partition)

📊 OPTIMISATIONS :
   • CACHE : évite de recalculer le DAG
   • BROADCAST : évite les shuffles pour les petites tables
   • PARTITIONING : contrôle le parallélisme

📊 SPARK UI (http://localhost:4040) :
   • Jobs : liste des actions exécutées
   • Stages : détail des shuffles
   • Tasks : exécution sur les executors
   • Storage : RDD/DataFrames en cache
   • SQL : plans d'exécution Catalyst
   • Executors : état des workers

📊 URLS DU CLUSTER :
   • http://localhost:8080 → Spark Master
   • http://localhost:4040 → Application UI (driver)
   • http://localhost:8081 → Worker 1
   • http://localhost:8082 → Worker 2
   • http://localhost:8083 → Worker 3
""")

pause("Lab terminé ! Tu peux explorer Spark UI encore un peu avant de fermer", 30)

spark.stop()
print("\n✅ Session Spark fermée. À bientôt !")
