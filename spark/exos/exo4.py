import pyspark.sql.functions as f
from pyspark.sql import SparkSession

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("demo_join").getOrCreate()

# 1. Charger les données
dfMovies = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/movie.csv")
)

dfRatings = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/rating.csv")
)

# 2. Jointure de base
# - Faire un **inner join** entre `ratings` et `movies` sur `movieId`
# - Afficher quelques exemples de notes enrichies avec le titre du film
dfInner = dfMovies.join(other=dfRatings, on="movieId", how="inner")
dfInner.show()

# 3. Statistiques globales
# - Calculer le nombre de notes et la moyenne des notes par film
# - Trier par nombre de notes décroissant
dfStats1 = (
    dfInner.groupBy(["movieId", "title"])
    .agg(f.count("rating").alias("nb_rating"), f.avg("rating").alias("avg_rating"))
    .orderBy(f.col("nb_rating").desc())
)
dfStats1.show()

# 4. Variantes de jointures
# - **LEFT SEMI** : films qui ont au moins une note
dfLeftSemi = dfMovies.join(other=dfRatings, on="movieId", how="left_semi")
dfLeftSemi.show()

# - **LEFT ANTI** : films sans aucune note
dfLeftAnti = dfMovies.join(other=dfRatings, on="movieId", how="left_anti")
dfLeftAnti.show()

# - **LEFT OUTER** : liste complète des films avec stats si disponibles
dfLeftOuter = dfMovies.join(other=dfRatings, on="movieId", how="left_outer")
dfLeftOuter.show()

# - **FULL OUTER** : diagnostic des clés présentes uniquement dans l’un des deux fichiers
dfFullOuter = dfMovies.join(other=dfRatings, on="movieId", how="full_outer")
dfFullOuter.show()

# 5. Exercices pratiques
# A. **Top 5 global** : films les mieux notés
dfStats2 = (
    dfInner.groupBy(["movieId", "title"])
    .agg(f.count("rating").alias("nb_rating"), f.avg("rating").alias("avg_rating"))
    .orderBy([f.col("avg_rating").desc(), f.col("nb_rating").desc()])
    .limit(5)
)
dfStats2.show()
