import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

builder: SparkSession.Builder = SparkSession.builder
spark = builder.appName("tp_etl3").master("spark://spark-master:7077").getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("ERROR")

df = spark.read.csv("/data/resultats_natation.csv", header=True, inferSchema=True)

print("\nSchema:")
df.printSchema()

print("\nDataFrame:")
df.show()

# ===
# Partie 1 : Nettoyage des données
# ===

# Avant d'analyser les performances, vous devez nettoyer le dataset :
# Problèmes à corriger :
# 1. **Valeurs manquantes** :
#    - Certains temps sont manquants (NULL ou 0)
#    - Certains noms d'athlètes sont vides
#    - Certaines catégories d'âge sont NULL

# Suppression des lignes avec un temps NULL ou 0
df_cleaned = df.filter(
    (F.col("temps_secondes").isNotNull()) & (F.col("temps_secondes") > 0)
)

# Modification des noms NULL par les noms le plus représentés par classes athlete_id
window_nom = Window.partitionBy("athlete_id")

df_cleaned = df_cleaned.withColumn(
    "nom",
    F.when(
        F.col("nom").isNull(),
        F.coalesce(F.mode("nom").over(window_nom), F.lit("UNKNOWN")),
    ).otherwise(F.col("nom")),
)


# Modification des categorie_age NULL par Junior si age < 18, Senior si < 35 et Master sinon
def get_category_age(age) -> str:
    if not age:
        return "UNKNOWN"
    if age < 18:
        return "Junior"
    if age < 35:
        return "Senior"
    return "Master"


getCategroyAge = F.udf(get_category_age, StringType())

df_cleaned = df_cleaned.withColumn(
    "categorie_age",
    F.when(
        F.col("categorie_age").isNull(),
        getCategroyAge(F.col("age")),
    ).otherwise(F.col("categorie_age")),
)

# 2. **Doublons** :
#    - Certaines performances sont dupliquées (même athlète, même épreuve, même date)

# Suppression des doublons
df_cleaned = df_cleaned.dropDuplicates(
    ["athlete_id", "date_competition", "epreuve", "nage"]
)

# 3. **Valeurs aberrantes** :
#    - Temps négatifs (erreur de saisie)
#    - Temps > 300 secondes (disqualifications non marquées)
#    - Âges < 10 ou > 80 (erreurs)

# Conversion des temps négatif en leur valeur absolue
df_cleaned = df_cleaned.withColumn(
    "temps_secondes",
    F.when(F.col("temps_secondes") < 0, F.abs(F.col("temps_secondes"))).otherwise(
        F.col("temps_secondes")
    ),
)

# Suppression des temps > 300
df_cleaned = df_cleaned.filter(F.col("temps_secondes") <= 300)

# 4. **Formatage** :
#    - Dates au format "YYYY-MM-DD" ou "DD/MM/YYYY" (inconsistant)
#    - Noms avec espaces en trop ou casse incohérente
#    - Pays avec abréviations différentes (FR/FRA/France)

# Conversion des dates aux format YYYY-MM-DD
df_cleaned = df_cleaned.withColumn(
    "date_competition",
    F.coalesce(
        F.to_date(F.col("date_competition"), "yyyy-MM-dd"),
        F.to_date(F.col("date_competition"), "dd/MM/yyyy"),
    ),
)

# Norlamisation des noms
df_cleaned = df_cleaned.withColumn(
    "nom",
    F.lower(F.trim(F.regexp_replace(F.col("nom"), r" +", " "))),
)

# Normalisation des pays
MAP_PAYS = {
    "RU": "Russia",
    "RUS": "Russia",
    "Russie": "Russia",
    "Russia": "Russia",
    "FRA": "France",
    "FR": "France",
    "France": "France",
    "DEU": "Germany",
    "DE": "Germany",
    "Allemagne": "Germany",
    "Germany": "Germany",
    "USA": "United States",
    "US": "United States",
    "Etats Unis": "United States",
    "United States": "United States",
    "ITA": "Italy",
    "IT": "Italy",
    "Italie": "Italy",
    "Italy": "Italy",
    "ESP": "Spain",
    "ES": "Spain",
    "Espagne": "Spain",
    "Spain": "Spain",
    "KR": "South Korea",
    "KOR": "South Korea",
    "Corée du Sud": "South Korea",
    "South Korea": "South Korea",
    "BRA": "Brazil",
    "BR": "Brazil",
    "Brésil": "Brazil",
    "Brazil": "Brazil",
    "JP": "Japan",
    "Japon": "Japan",
    "Japan": "Japan",
    "GBR": "United Kingdom",
    "GB": "United Kingdom",
    "UK": "United Kingdom",
    "United Kingdom": "United Kingdom",
}

map_pays_broadcast = sc.broadcast(MAP_PAYS)


def normalize_pays(pays: str) -> str:
    return map_pays_broadcast.value.get(pays, pays.title())


normalizePays = F.udf(normalize_pays, StringType())

df_cleaned = df_cleaned.withColumn("pays", normalizePays(F.col("pays")))

print("\nRapport de traitement")
print("\tSuppression des lignes avec un temps NULL ou 0")
print(
    "\tModification des noms NULL par les noms le plus représentés par classes athlete_id"
)
print(
    "\tModification des categorie_age NULL par Junior si age < 18 et Senior si < 35 et Master sinon"
)
print("\tSuppression des doublons")
print("\tConversion des temps négatif en leur valeur absolue")
print("\tSuppression des temps > 300")
print("\tConversion des dates aux format YYYY-MM-DD")
print("\tNormalisation des noms")
print("\tNormalisation des pays")
df_nb_rows = df.count()
df_clean_nb_rows = df_cleaned.count()
print(f"\tNombre de ligne initiale : {df_nb_rows}")
print(f"\tNombre de lignes après traitement : {df_clean_nb_rows}")
print(f"\tNombre de lignes supprimées : {df_nb_rows - df_clean_nb_rows}")

print("\nDataFrame Cleaned:")
df_cleaned.show()

# ===
# Partie 2 : Analyse avec Window Functions
# ===

# Exercice 2.1 : Classement par épreuve et compétition

# **Objectif** : Pour chaque compétition et chaque épreuve, classer les athlètes

# **Attendu** :

# - Colonnes : athlete_id, nom, epreuve, date_competition, temps_secondes
# - `position` : classement dans l'épreuve (1er, 2ème, 3ème...)
# - `ecart_avec_premier` : différence de temps avec le 1er (en secondes)
# - `est_podium` : booléen indiquant si l'athlète est sur le podium (top 3)

window_position = Window.partitionBy(["competition_id", "epreuve", "nage"]).orderBy(
    "temps_secondes"
)

df_position = (
    df_cleaned.withColumn("position", F.dense_rank().over(window_position))
    .withColumn(
        "ecart_avec_premier",
        F.col("temps_secondes") - F.min(F.col("temps_secondes")).over(window_position),
    )
    .withColumn("est_podium", F.when(F.col("position") <= 3, True).otherwise(False))
)

# **Filtrer** : Afficher uniquement le podium de chaque épreuve

print("\nRank by date_eprueve, epreuve and nage:")
df_position.select(
    [
        "athlete_id",
        "nom",
        "epreuve",
        "date_competition",
        "temps_secondes",
        "position",
        "ecart_avec_premier",
        "est_podium",
    ]
).filter(F.col("est_podium")).orderBy(
    ["date_competition", "epreuve", "position"]
).show()

# ### Exercice 2.2 : Progression personnelle

# **Objectif** : Analyser l'évolution des performances de chaque athlète sur la saison

# **Attendu** :

# - Pour chaque athlète et chaque type d'épreuve (ex: "100m Libre")
# - `temps_precedent` : temps de la compétition précédente
# - `amelioration_secondes` : temps_precedent - temps_actuel (positif = amélioration)
# - `amelioration_pct` : amélioration en pourcentage
# - `meilleur_temps_perso` : record personnel sur cette épreuve jusqu'à cette date
# - `est_record_perso` : booléen indiquant si c'est un nouveau record

window_perf = Window.partitionBy(["athlete_id", "epreuve", "nage"]).orderBy(
    "date_competition"
)

df_perf = (
    df_position.withColumn(
        "temps_precedent", F.lag(F.col("temps_secondes")).over(window_perf)
    )
    .withColumn(
        "amelioration_secondes",
        F.col("temps_precedent") - F.col("temps_secondes"),
    )
    .withColumn(
        "amelioration_pct",
        F.col("amelioration_secondes") / F.col("temps_precedent") * 100,
    )
    .withColumn(
        "meilleur_temps_perso",
        F.min(F.col("temps_secondes")).over(
            Window.partitionBy(["athlete_id", "epreuve", "nage"])
            .orderBy("date_competition")
            .rowsBetween(Window.unboundedPreceding, Window.currentRow)
        ),
    )
    .withColumn(
        "est_record_perso",
        F.when(
            F.col("temps_secondes") == F.col("meilleur_temps_perso"),
            True,
        ).otherwise(False),
    )
)

# **Trier** : Par athlète et date chronologique

df_perf.select(
    [
        "athlete_id",
        "nom",
        "epreuve",
        "date_competition",
        "temps_secondes",
        "temps_precedent",
        "amelioration_secondes",
        "amelioration_pct",
        "meilleur_temps_perso",
        "est_record_perso",
    ]
).orderBy(["athlete_id", "epreuve", "date_competition"]).show()

# ### Exercice 2.3 : Analyse par catégorie

# **Objectif** : Comparer chaque performance à la moyenne de sa catégorie

# **Attendu** :

# - `temps_moyen_categorie` : temps moyen de la catégorie sur cette épreuve (sur toute la saison)
# - `ecart_vs_moyenne` : différence avec la moyenne (négatif = meilleur que la moyenne)
# - `percentile_categorie` : dans quel quartile se situe l'athlète (1-4)
# - `rang_categorie` : classement dans sa catégorie d'âge sur cette épreuve
# - `top_10_pct` : booléen indiquant si dans les 10% meilleurs de sa catégorie

window_catagory = Window.partitionBy(["categorie_age", "epreuve", "nage"]).orderBy(
    "temps_secondes"
)

df_comparison = (
    df_perf.withColumn(
        "temps_moyen_categorie",
        F.avg(F.col("temps_secondes")).over(window_catagory),
    )
    .withColumn(
        "ecart_vs_moyenne",
        F.col("temps_secondes") - F.col("temps_moyen_categorie"),
    )
    .withColumn(
        "percentile_categorie",
        F.ntile(4).over(window_catagory),
    )
    .withColumn(
        "rang_categorie",
        F.dense_rank().over(window_catagory),
    )
    .withColumn(
        "top_10_pct",
        F.when(
            F.ntile(10).over(window_catagory) == 1,
            True,
        ).otherwise(False),
    )
)

df_comparison.select(
    [
        "athlete_id",
        "nom",
        "epreuve",
        "categorie_age",
        "date_competition",
        "temps_secondes",
        "temps_moyen_categorie",
        "ecart_vs_moyenne",
        "percentile_categorie",
        "rang_categorie",
        "top_10_pct",
    ]
).orderBy(["epreuve", "categorie_age", "date_competition"]).show()

# ### Exercice 2.4 : Polyvalence des nageurs

# **Objectif** : Identifier les nageurs les plus polyvalents (performants sur plusieurs styles)

# **Attendu** :

# - Par athlète, calculer :
#   - `nb_epreuves_differentes` : nombre d'épreuves distinctes nagées
#   - `nb_styles_differents` : nombre de styles de nage différents
#   - `meilleur_style` : style où l'athlète a le meilleur classement moyen
#   - `rang_moyen_toutes_epreuves` : rang moyen sur toutes ses participations
#   - `est_polyvalent` : booléen (True si >= 3 styles différents)

# TODO meilleur_style

df_groupBy1 = df_comparison.groupBy("athlete_id").agg(
    F.count_distinct("epreuve").alias("nb_epreuves_differentes"),
    F.count_distinct("nage").alias("nb_styles_differents"),
    F.avg("rang_categorie").alias("rang_moyen_toutes_epreuves"),
)

df_polyvalent = df_comparison.join(df_groupBy1, "athlete_id", "left")
df_polyvalent = df_polyvalent.withColumn(
    "est_polyvalent",
    F.when(F.col("nb_styles_differents") >= 3, True).otherwise(False),
)

# **Filtrer** : Athlètes ayant participé à au moins 5 compétitions

df_polyvalent.select(
    [
        "athlete_id",
        "nom",
        "epreuve",
        "nage",
        "rang_categorie",
        "nb_epreuves_differentes",
        "nb_styles_differents",
        "rang_moyen_toutes_epreuves",
        "est_polyvalent",
    ]
).orderBy(["athlete_id", "epreuve", "nage"]).show()

# ### Exercice 2.5 : Tendance de performance

# **Objectif** : Calculer une moyenne mobile pour détecter les tendances

# **Attendu** :

# - Pour chaque athlète sur son épreuve favorite (celle qu'il nage le plus)
# - `moyenne_mobile_3comp` : moyenne des temps sur les 3 dernières compétitions
# - `tendance` : "Amélioration", "Stable" ou "Dégradation"
#   - Amélioration : temps actuel < moyenne mobile
#   - Dégradation : temps actuel > moyenne mobile + 1 seconde
#   - Stable : entre les deux
# - `nb_competitions` : nombre de compétitions de l'athlète sur cette épreuve

# TODO épreuve FAVORITE uniquement

window_frame_3 = (
    Window.partitionBy("athlete_id").orderBy("date_competition").rowsBetween(-3, -1)
)


def get_tendance(temps_secondes: float, moyenne_mobile: float) -> str:
    if temps_secondes < moyenne_mobile:
        return "Amélioration"
    if temps_secondes > moyenne_mobile + 1:
        return "Dégradation"
    return "Stable"


getTendance = F.udf(get_tendance, StringType())

df_mean = df_polyvalent.withColumn(
    "moyenne_mobile_3comp",
    F.avg("temps_secondes").over(window_frame_3),
).withColumn(
    "tendance",
    getTendance(F.col("temps_secondes"), F.col("moyenne_mobile_3comp")),
)

df_groupBy2 = df_cleaned.groupBy(["athlete_id", "epreuve"]).agg(
    F.count(F.col("date_competition")).alias("nb_competitions")
)
df_mean = df_mean.join(df_groupBy2, ["athlete_id", "epreuve"], "left")

df_mean.select(
    [
        "athlete_id",
        "nom",
        "epreuve",
        "temps_secondes",
        "moyenne_mobile_3comp",
        "tendance",
        "nb_competitions",
    ]
).orderBy(["athlete_id", "epreuve"]).show()

# ### Exercice 2.6 : Performance relative par pays

# **Objectif** : Comparer les athlètes à la performance moyenne de leur pays

# **Attendu** :

# - `meilleur_temps_pays` : meilleur temps du pays sur cette épreuve
# - `temps_moyen_pays` : temps moyen du pays sur cette épreuve
# - `rang_dans_pays` : classement de l'athlète parmi ses compatriotes
# - `ecart_vs_meilleur_pays` : différence avec le meilleur de son pays
# - `est_meilleur_pays` : booléen (meilleur temps de son pays sur cette épreuve)

window_pays = Window.partitionBy(["pays", "epreuve", "nage"])

df_comparison_perf = (
    df_mean.withColumn(
        "meilleur_temps_pays",
        F.min("temps_secondes").over(window_pays),
    )
    .withColumn(
        "temps_moyen_pays",
        F.avg("temps_secondes").over(window_pays),
    )
    .withColumn(
        "rang_dans_pays",
        F.dense_rank().over(window_pays),
    )
    .withColumn(
        "ecart_vs_meilleur_pays",
        F.col("temps_secondes") - F.col("meilleur_temps_pays"),
    )
    .withColumn(
        "est_meilleur_pays",
        F.col("temps_secondes") == F.col("meilleur_temps_pays"),
    )
)

df_comparison_perf.select(
    [
        "athlete_id",
        "nom",
        "pays",
        "epreuve",
        "meilleur_temps_pays",
        "temps_moyen_pays",
        "rang_dans_pays",
        "ecart_vs_meilleur_pays",
        "est_meilleur_pays",
    ]
).orderBy(["pays", "epreuve", "temps_secondes"]).show()

# Terminate program
map_pays_broadcast.unpersist()
spark.stop()
