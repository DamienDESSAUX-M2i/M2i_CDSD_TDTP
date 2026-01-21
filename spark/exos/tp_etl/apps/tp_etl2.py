import re

import pyspark.sql.functions as spark_func
from pyspark.sql import SparkSession
from pyspark.sql.types import BooleanType, StringType, StructField, StructType

builder: SparkSession.Builder = SparkSession.builder

spark = builder.appName("demo_regex").master("spark://spark-master:7077").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

data = [
    (
        "2024-01-15 10:23:45 [INFO] User: jean.dupont@company.fr logged in from IP: 192.168.1.100",
    ),
    (
        "2024-01-15 11:45:12 [ERROR] User: marie_martin@gmail.com failed login from IP: 10.0.0.25",
    ),
    (
        "2024-01-15 14:30:00 [INFO] User: pierre.durant@yahoo.fr logged in from IP: 172.16.0.5",
    ),
    (
        "2024-01-15 15:22:33 [WARNING] User: sophie@invalid-email logged in from IP: 192.168.2.200",
    ),
    (
        "2024-01-15 16:10:05 [INFO] User: luc.moreau@outlook.com logged in from IP: 8.8.8.8",
    ),
]

schema = StructType([StructField("log_message", StringType(), True)])

df = spark.createDataFrame(data, schema)

print("\nDataFrame:")
df.show(truncate=False)

# EXERCICE 1 : Extraction de la date et heure

# Extraire le timestamp au format `YYYY-MM-DD HH:MM:SS`

# - **Colonne à créer** : `timestamp`
# - **Exemple résultat** : `2024-01-15 10:23:45`

df = df.withColumn(
    "timestamp",
    spark_func.regexp_extract(
        spark_func.col("log_message"), r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", 0
    ),
)

print("\nTimestamp:")
df.show(truncate=False)

# EXERCICE 2 : Extraction du niveau de log

# Extraire le niveau entre crochets (INFO, ERROR, WARNING)

# - **Colonne à créer** : `niveau`
# - **Exemple résultat** : `INFO`

# df = df.withColumn(
#     "niveau",
#     spark_func.regexp_replace(
#         spark_func.regexp_extract(spark_func.col("log_message"), r"\[[A-Z]+\]", 0),
#         r"(\[|\])",
#         "",
#     ),
# )

df = df.withColumn(
    "niveau",
    spark_func.regexp_extract(spark_func.col("log_message"), r"\[([A-Z]+)\]", 1),
)

print("\nLevel:")
df.show(truncate=False)

# EXERCICE 3 : Extraction de l'email complet

# Extraire l'adresse email complète après "User: "

# - **Colonne à créer** : `email`
# - **Exemple résultat** : `jean.dupont@company.fr`

df = df.withColumn(
    "email",
    spark_func.regexp_extract(
        spark_func.col("log_message"), r"[A-Za-z0-9._-]+@[A-Za-z0-9._-]+", 0
    ),
)

print("\nEmail:")
df.show(truncate=False)

# EXERCICE 4 : Extraction du nom d'utilisateur

# Extraire uniquement la partie avant le @ de l'email

# - **Colonne à créer** : `username`
# - **Exemple résultat** : `jean.dupont`

df = df.withColumn(
    "username",
    spark_func.lower(
        spark_func.regexp_replace(
            spark_func.regexp_extract(spark_func.col("email"), r"^[A-Za-z0-9._-]+", 0),
            r"\.|_",
            " ",
        )
    ),
)

# df = df.withColumn(
#     "username",
#     spark_func.regexp_extract(spark_func.col("email"), r"^[A-Za-z._]+", 0),
# )

print("\nUsername:")
df.show(truncate=False)

# EXERCICE 5 : Extraction du domaine

# Extraire uniquement la partie après le @ de l'email

# - **Colonne à créer** : `domaine`
# - **Exemple résultat** : `company.fr`

df = df.withColumn(
    "domaine",
    spark_func.regexp_replace(
        spark_func.regexp_extract(spark_func.col("email"), r"@[A-Za-z.-]+", 0),
        r"@",
        "",
    ),
)

print("\nDomaine:")
df.show(truncate=False)

# EXERCICE 6 : Extraction de l'adresse IP

# Extraire l'adresse IP après "IP: "

# - **Colonne à créer** : `ip_address`
# - **Exemple résultat** : `192.168.1.100`

df = df.withColumn(
    "ip_address",
    spark_func.regexp_extract(
        spark_func.col("log_message"), r"(\d+\.\d+\.\d+\.\d+)", 0
    ),
)

print("\nIP address:")
df.show(truncate=False)

# EXERCICE 7 : Extraction de l'action

# Extraire le type d'action (logged in ou failed login)

# - **Colonne à créer** : `action`
# - **Exemple résultat** : `logged in`

df = df.withColumn(
    "action",
    spark_func.regexp_extract(spark_func.col("log_message"), r"logged|failed", 0),
)

print("\nAction:")
df.show(truncate=False)

# EXERCICE 8 : Validation de l'email

# Vérifier si l'email est valide (format correct)

# - **Colonne à créer** : `email_valide`
# - **Résultat** : `OUI` ou `NON`

EMAIL_REGEX = re.compile(r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$")


def email_validator(email: str) -> bool:
    if EMAIL_REGEX.match(email):
        return True

    return False


emailValidator = spark_func.udf(email_validator, BooleanType())

df = df.withColumn(
    "email_valide",
    emailValidator(spark_func.col("email")),
)

print("\nAction:")
df.show(truncate=False)


spark.stop()
