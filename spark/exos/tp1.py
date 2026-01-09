import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    StringType,
    StructField,
    StructType,
)

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("tp1").getOrCreate()

students = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv(
        "C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/StudentsPerformance.csv"
    )
)


# ===
# Niveau 1 : Manipulation de Base des DataFrames
# ===


# Exercice 1.1 - Exploration

# TODO 1: Afficher le schéma
print(f"Schema: {students.schema}")

# TODO 2: Compter le nombre d'étudiants
print(f"Number of students: {students.count()}")

# TODO 3: Afficher les 10 premières lignes
print("10 first lines :")
students.show(10)

# TODO 4: Afficher les statistiques descriptives (describe)
print("Statistics:")
students.describe().show()

# Exercice 1.2 - Sélections et Filtres

# TODO 1: Sélectionner uniquement gender et les 3 scores
students["gender", "math score", "reading score", "writing score"].show(5)

# TODO 2: Filtrer les étudiants qui ont > 90 en maths
students.filter(students["math score"] > 90).show(5)

# TODO 3: Filtrer les étudiants avec lunch = "free/reduced"
students.filter(students["lunch"] == "free/reduced").show(5)

# TODO 4: Compter combien d'étudiants ont complété le prep course
result = students.filter(students["test preparation course"] == "completed").count()
print(f"{result} students have completed their test preparation.")

# TODO 5: Trouver les 10 meilleurs scores en lecture
print("10 best reading score:")
for k, row in enumerate(
    students.sort(F.col("reading score").desc()).limit(10).collect(), start=1
):
    print(f"{k} - {row['reading score']}")

# Exercice 1.3 - Agrégations

# TODO 1: Calculer la moyenne de chaque matière
print("Mean of each topic:")
students.select(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
).show()

# TODO 2: Compter le nombre d'étudiants par genre
print("Number of students by gender:")
students.groupBy("gender").agg(F.count("gender").alias("number of students")).show()

# TODO 3: Calculer la moyenne des scores par genre
print("Mean of each topic by gender:")
students.groupBy("gender").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
).show()

# TODO 4: Trouver le score max et min en maths
print("Max and min score in maths:")
students.select(
    F.max("math score").alias("max math score"),
    F.min("math score").alias("min math score"),
).show()

# TODO 5: Calculer la moyenne par groupe ethnique (race/ethnicity)
print("Mean of each topic by race/ethnicity:")
students.groupBy("race/ethnicity").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
).show()


# ===
# Niveau 2 : Jointures
# ===


# Créer une table de catégories de scores
grades_ref = spark.createDataFrame(
    [("A", 90, 100), ("B", 80, 89), ("C", 70, 79), ("D", 60, 69), ("F", 0, 59)],
    ["grade", "min_score", "max_score"],
)

print("Table grade_ref:")
grades_ref.show()

# Créer une table de départements
departments = spark.createDataFrame(
    [
        ("group A", "Sciences"),
        ("group B", "Arts"),
        ("group C", "Commerce"),
        ("group D", "Ingénierie"),
        ("group E", "Médecine"),
    ],
    ["ethnicity", "department"],
)

print("Table departments:")
departments.show()

# Exercice 2.1 - Jointure simple

# TODO 1: Joindre students avec departments
# Sur la colonne race/ethnicity = ethnicity
# Afficher : gender, ethnicity, department, math score
print("Joining students and departments:")
students_departments = students.join(
    departments, students["race/ethnicity"] == departments["ethnicity"], "inner"
)
students_departments["gender", "ethnicity", "department", "math score"].show(5)

# TODO 2: Compter le nombre d'étudiants par département
print("Number of students by departments:")
students_departments.groupBy("department").agg(
    F.count("department").alias("number of students")
).show()

# TODO 3: Calculer la moyenne des scores par département
print("Mean of scores by departments:")
students_departments.groupBy("department").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
).show()

# Exercice 2.2 - Transformation et jointure

# TODO 1: Créer un DataFrame avec student_id et score moyen
# Calculer la moyenne des 3 matières pour chaque étudiant
students_with_id = students.withColumn(
    "student_id", F.monotonically_increasing_id()
)  # Ajouter un student_id
marksColumns = [F.col("math score"), F.col("reading score"), F.col("writing score")]
averageFunc = sum(x for x in marksColumns) / len(marksColumns)
students_with_id = students_with_id.withColumn("mean score", averageFunc)

print("Add student_id and compute mean of each student:")
students_with_id.show(5)

# TODO 2: "Joindre" ce DataFrame avec la table grades_ref
print("Joining with grades_ref:")
students_grades = students_with_id.join(
    grades_ref,
    (grades_ref["min_score"] <= students_with_id["mean score"])
    & (students_with_id["mean score"] < grades_ref["max_score"]),
    "inner",
)
students_grades.show(20)

# TODO 3: Compter combien d'étudiants ont chaque grade (A, B, C, D, F)
print("Number of students by grades:")
students_grades.groupBy("grade").agg(
    F.count("grade").alias("number of students")
).show()

# Exercice 2.3 - Analyse croisée

# TODO 1: Joindre students avec departments
# Calculer la moyenne par département ET par genre
print("Mean by departments and by gender:")
students_departments.groupBy("department", "gender").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
).orderBy(F.col("department"), F.col("gender")).show()

# TODO 2: Identifier le département avec les meilleurs résultats
dfStats3 = students_departments.groupBy("department").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
    F.count("math score").alias("count math score"),
    F.count("reading score").alias("count reading score"),
    F.count("writing score").alias("count writing score"),
)
marksColumnsAvg = [
    F.col("avg math score"),
    F.col("avg reading score"),
    F.col("avg writing score"),
]
marksColumnsCount = [
    F.col("count math score"),
    F.col("count reading score"),
    F.col("count writing score"),
]
averageFunc = sum([x * y for x, y in zip(marksColumnsAvg, marksColumnsCount)]) / sum(
    [y for y in marksColumnsCount]
)
dfStats3 = dfStats3.withColumn("avg", averageFunc)

print("Mean by departments:")
dfStats3["department", "avg"].orderBy(F.col("avg").desc()).show()

# TODO 3: Analyser l'impact du prep course par département
# Comparer moyenne avec/sans prep course pour chaque département
dfStats4 = students_departments.groupBy("department", "test preparation course").agg(
    F.avg("math score").alias("avg math score"),
    F.avg("reading score").alias("avg reading score"),
    F.avg("writing score").alias("avg writing score"),
    F.count("math score").alias("count math score"),
    F.count("reading score").alias("count reading score"),
    F.count("writing score").alias("count writing score"),
)
dfStats4 = dfStats4.withColumn("avg", averageFunc)

print("Mean by departments and test preparation course:")
dfStats4["department", "test preparation course", "avg"].orderBy(
    ["department", "test preparation course"]
).show()


# ===
# Niveau 3 : UDF
# ===


# Exercice 3.1 - UDF simple


# TODO 1: Créer une UDF pour convertir un score en grade
# A: 90-100, B: 80-89, C: 70-79, D: 60-69, E: 0-59
def score_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "E"


scoreGrade = F.udf(f=score_grade, returnType=StringType())

# TODO 2: Appliquer cette UDF aux 3 matières
# Créer 3 nouvelles colonnes : math_grade, reading_grade, writing_grade

students_with_grades = (
    students.withColumn(colName="math grade", col=scoreGrade(F.col("math score")))
    .withColumn(colName="reading grade", col=scoreGrade(F.col("reading score")))
    .withColumn(colName="writing grade", col=scoreGrade(F.col("writing score")))
)

print("Add grades:")
students_with_grades.show(5)

# TODO 3: Compter la distribution des grades en maths
print("Number of students by grades:")
students_with_grades.groupBy("math grade").agg(
    F.count("math grade").alias("number of students")
).orderBy("number of students").show()

# Exercice 3.2 - UDF avec plusieurs paramètres

# TODO 1: Créer une UDF pour calculer la moyenne pondérée
# Math: 40%, Reading: 30%, Writing: 30%
WEIGHT_MAP = {"math": 40, "reading": 30, "writing": 30}


def weighted_avg(
    math_score: float, reading_score: float, writing_score: float
) -> float:
    return (
        math_score * WEIGHT_MAP["math"]
        + reading_score * WEIGHT_MAP["reading"]
        + writing_score * WEIGHT_MAP["writing"]
    ) / sum(WEIGHT_MAP.values())


weightedAvg = F.udf(weighted_avg, DoubleType())

# TODO 2: Combiner avec la UDF de grade pour obtenir le grade final
print("Add weighted average and grade:")
students_with_weighted_avg = students.withColumn(
    "weighted avg",
    weightedAvg(F.col("math score"), F.col("reading score"), F.col("writing score")),
).withColumn(
    "grade",
    scoreGrade(F.col("weighted avg")),
)
students_with_weighted_avg.show(5)

# Exercice 3.3 - UDF avec logique conditionnelle


# TODO 1: Créer une UDF pour catégoriser la performance
# "Excellent" : moyenne >= 85
# "Très bien" : moyenne >= 75
# "Bien" : moyenne >= 65
# "Passable" : moyenne >= 50
# "Insuffisant" : moyenne < 50
def score_category(score: float) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 75:
        return "Très bien"
    if score >= 65:
        return "Bien"
    if score >= 50:
        return "Passable"
    return "Insuffisant"


scoreCategory = F.udf(score_category, StringType())

# TODO 2: Appliquer cette UDF et compter les étudiants par catégorie
students_with_category = students.withColumn(
    "weighted avg",
    weightedAvg(F.col("math score"), F.col("reading score"), F.col("writing score")),
).withColumn(
    "category",
    scoreCategory(F.col("weighted avg")),
)

print("Number of students by categories:")
students_with_category.groupBy("category").agg(
    F.count("category").alias("number of students")
).orderBy("category").show(5)

# Exercice 3.4 - UDF avec struct (bonus)

# TODO: Créer une UDF qui retourne plusieurs informations
# Input: score
# Output: struct avec {grade, passed (bool), level}
schema = StructType(
    [
        StructField("grade", StringType(), False),
        StructField("passed", BooleanType(), False),
        StructField("level", StringType(), False),
    ]
)


def score_transformation(score: float) -> tuple[str, bool, str]:
    return score_grade(score), (score >= 50), score_category(score)


scoreTransformation = F.udf(score_transformation, schema)

students_score_transformation = students.withColumn(
    "weighted avg",
    weightedAvg(F.col("math score"), F.col("reading score"), F.col("writing score")),
).withColumn("score transformation", scoreTransformation(F.col("weighted avg")))

print("Score transformation:")
students_score_transformation.show(5)
