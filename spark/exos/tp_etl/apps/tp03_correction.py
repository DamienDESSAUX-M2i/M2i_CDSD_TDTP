from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructField, StructType, StringType
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("tp03") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("/data/resultats_natation.csv", header=True, inferSchema=True)

# Partie 1: Nettoyage des données
df_clean = df.filter(
    (col("temps_secondes").isNotNull()) & 
    (col("temps_secondes") > 0) & 
    (col("temps_secondes") <= 300) &
    (col("nom").isNotNull()) & 
    (col("nom") != "") &
    (col("age") >= 10) & 
    (col("age") <= 80) &
    (col("categorie_age").isNotNull())
)

df_clean = df_clean.withColumn("nom", trim(initcap(col("nom"))))

df_clean = df_clean.withColumn(
    "pays",
    when(regexp_extract(col("pays"), "^(FR|FRA)$", 0) != "", "France")
    .when(regexp_extract(col("pays"), "^(US|USA)$", 0) != "", "United States")
    .when(regexp_extract(col("pays"), "^(GB|GBR|UK)$", 0) != "", "United Kingdom")
    .when(regexp_extract(col("pays"), "^(DE|DEU|GER)$", 0) != "", "Germany")
    .when(regexp_extract(col("pays"), "^(ES|ESP)$", 0) != "", "Spain")
    .when(regexp_extract(col("pays"), "^(IT|ITA)$", 0) != "", "Italy")
    .when(regexp_extract(col("pays"), "^(JP|JPN)$", 0) != "", "Japan")
    .when(regexp_extract(col("pays"), "^(CN|CHN)$", 0) != "", "China")
    .when(regexp_extract(col("pays"), "^(AU|AUS)$", 0) != "", "Australia")
    .when(regexp_extract(col("pays"), "^(CA|CAN)$", 0) != "", "Canada")
    .when(regexp_extract(col("pays"), "^(BR|BRA)$", 0) != "", "Brazil")
    .when(regexp_extract(col("pays"), "^(RU|RUS)$", 0) != "", "Russia")
    .otherwise(col("pays"))
)

df_clean = df_clean.withColumn(
    "date_competition",
    when(col("date_competition").contains("/"), 
         to_date(col("date_competition"), "dd/MM/yyyy"))
    .otherwise(to_date(col("date_competition"), "yyyy-MM-dd"))
)

df_clean = df_clean.dropDuplicates(["athlete_id", "epreuve", "nage", "date_competition"])

# Exercice 2.1: Classement par épreuve et compétition
w_classement = Window.partitionBy("competition_id", "epreuve", "nage").orderBy("temps_secondes")

df_classement = df_clean.withColumn("position", row_number().over(w_classement))
df_classement = df_classement.withColumn(
    "ecart_avec_premier",
    col("temps_secondes") - first("temps_secondes").over(w_classement)
)
df_classement = df_classement.withColumn("est_podium", col("position") <= 3)

podium = df_classement.filter(col("est_podium")).select(
    "athlete_id", "nom", "epreuve", "date_competition", "temps_secondes", 
    "position", "ecart_avec_premier", "est_podium"
)

# Exercice 2.2: Progression personnelle
w_progression = Window.partitionBy("athlete_id", "epreuve", "nage").orderBy("date_competition")

df_progression = df_clean.withColumn("temps_precedent", lag("temps_secondes").over(w_progression))
df_progression = df_progression.withColumn(
    "amelioration_secondes",
    col("temps_precedent") - col("temps_secondes")
)
df_progression = df_progression.withColumn(
    "amelioration_pct",
    (col("amelioration_secondes") / col("temps_precedent")) * 100
)
df_progression = df_progression.withColumn(
    "meilleur_temps_perso",
    min("temps_secondes").over(
        Window.partitionBy("athlete_id", "epreuve", "nage")
        .orderBy("date_competition")
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )
)
df_progression = df_progression.withColumn(
    "est_record_perso",
    col("temps_secondes") == col("meilleur_temps_perso")
)

# Exercice 2.3: Analyse par catégorie
w_categorie = Window.partitionBy("categorie_age", "epreuve", "nage")

df_categorie = df_clean.withColumn(
    "temps_moyen_categorie",
    avg("temps_secondes").over(w_categorie)
)
df_categorie = df_categorie.withColumn(
    "ecart_vs_moyenne",
    col("temps_secondes") - col("temps_moyen_categorie")
)
df_categorie = df_categorie.withColumn(
    "rang_categorie",
    row_number().over(w_categorie.orderBy("temps_secondes"))
)
df_categorie = df_categorie.withColumn(
    "percentile_categorie",
    ntile(4).over(w_categorie.orderBy("temps_secondes"))
)

total_par_categorie = df_clean.groupBy("categorie_age", "epreuve", "nage").count().withColumnRenamed("count", "total_categorie")
df_categorie = df_categorie.join(total_par_categorie, ["categorie_age", "epreuve", "nage"])
df_categorie = df_categorie.withColumn(
    "top_10_pct",
    col("rang_categorie") <= (col("total_categorie") * 0.1)
)

# Exercice 2.4: Polyvalence des nageurs
w_athlete = Window.partitionBy("athlete_id")

df_polyvalence = df_clean.groupBy("athlete_id", "nom").agg(
    countDistinct(concat(col("epreuve"), col("nage"))).alias("nb_epreuves_differentes"),
    countDistinct("nage").alias("nb_styles_differents"),
    count("*").alias("nb_competitions_total")
)

df_rangs = df_clean.withColumn(
    "rang",
    row_number().over(Window.partitionBy("competition_id", "epreuve", "nage").orderBy("temps_secondes"))
)
df_rangs_style = df_rangs.groupBy("athlete_id", "nage").agg(
    avg("rang").alias("rang_moyen_style")
)

w_meilleur_style = Window.partitionBy("athlete_id").orderBy("rang_moyen_style")
df_rangs_style = df_rangs_style.withColumn(
    "rang_style",
    row_number().over(w_meilleur_style)
)
meilleur_style = df_rangs_style.filter(col("rang_style") == 1).select(
    "athlete_id",
    col("nage").alias("meilleur_style")
)

df_rangs_global = df_rangs.groupBy("athlete_id").agg(
    avg("rang").alias("rang_moyen_toutes_epreuves")
)

df_polyvalence = df_polyvalence.join(meilleur_style, "athlete_id", "left")
df_polyvalence = df_polyvalence.join(df_rangs_global, "athlete_id", "left")
df_polyvalence = df_polyvalence.withColumn(
    "est_polyvalent",
    col("nb_styles_differents") >= 3
)
df_polyvalence = df_polyvalence.filter(col("nb_competitions_total") >= 5)

# Exercice 2.5: Tendance de performance
epreuve_favorite = df_clean.groupBy("athlete_id", "epreuve", "nage").count().withColumnRenamed("count", "nb_competitions")

w_favorite = Window.partitionBy("athlete_id").orderBy(desc("nb_competitions"))
epreuve_favorite = epreuve_favorite.withColumn("rang", row_number().over(w_favorite))
epreuve_favorite = epreuve_favorite.filter(col("rang") == 1).select("athlete_id", "epreuve", "nage", "nb_competitions")

df_tendance = df_clean.join(
    epreuve_favorite.select("athlete_id", col("epreuve").alias("epreuve_fav"), col("nage").alias("nage_fav")),
    "athlete_id"
)
df_tendance = df_tendance.filter(
    (col("epreuve") == col("epreuve_fav")) & (col("nage") == col("nage_fav"))
)

w_mobile = Window.partitionBy("athlete_id").orderBy("date_competition").rowsBetween(-3, -1)
df_tendance = df_tendance.withColumn(
    "moyenne_mobile_3comp",
    avg("temps_secondes").over(w_mobile)
)
df_tendance = df_tendance.withColumn(
    "tendance",
    when(col("temps_secondes") < col("moyenne_mobile_3comp"), "Amélioration")
    .when(col("temps_secondes") > col("moyenne_mobile_3comp") + 1, "Dégradation")
    .otherwise("Stable")
)
df_tendance = df_tendance.join(epreuve_favorite.select("athlete_id", "nb_competitions"), "athlete_id")

# Exercice 2.6: Performance relative par pays
w_pays = Window.partitionBy("pays", "epreuve", "nage")

df_pays = df_clean.withColumn(
    "meilleur_temps_pays",
    min("temps_secondes").over(w_pays)
)
df_pays = df_pays.withColumn(
    "temps_moyen_pays",
    avg("temps_secondes").over(w_pays)
)
df_pays = df_pays.withColumn(
    "rang_dans_pays",
    row_number().over(w_pays.orderBy("temps_secondes"))
)
df_pays = df_pays.withColumn(
    "ecart_vs_meilleur_pays",
    col("temps_secondes") - col("meilleur_temps_pays")
)
df_pays = df_pays.withColumn(
    "est_meilleur_pays",
    col("temps_secondes") == col("meilleur_temps_pays")
)

podium.show()
df_progression.show()
df_categorie.show()
df_polyvalence.show()
df_tendance.show()
df_pays.show()