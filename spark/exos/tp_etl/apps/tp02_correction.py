from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructField, StructType, StringType

spark = SparkSession.builder \
    .appName("tp02") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

logs_data = [
    ("2024-01-15 10:23:45 [INFO] User: jean.dupont@company.fr logged in from IP: 192.168.1.100"),
    ("2024-01-15 11:45:12 [ERROR] User: marie_martin@gmail.com failed login from IP: 10.0.0.25"),
    ("2024-01-15 14:30:00 [INFO] User: pierre.durant@yahoo.fr logged in from IP: 172.16.0.5"),
    ("2024-01-15 15:22:33 [WARNING] User: sophie@invalid-email logged in from IP: 192.168.2.200"),
    ("2024-01-15 16:10:05 [INFO] User: luc.moreau@outlook.com logged in from IP: 8.8.8.8"),
]

schema = StructType([StructField("log_message", StringType(), True)])
df_logs = spark.createDataFrame([(log,) for log in logs_data], schema)

df_logs.show()

# EXERCICE 1 : Extraction de la date et heure
df = df_logs.withColumn(
    "timestamp",
    F.regexp_extract(F.col("log_message"), "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})", 0)
)

# EXERCICE 2 : Extraction du niveau de log
df = df.withColumn(
    "niveau",
    F.regexp_extract(F.col("log_message"), "\\[(INFO|ERROR|WARNING)\\]", 1)
)

# EXERCICE 3 : Extraction de l'email complet
df = df.withColumn(
    "email",
    F.regexp_extract(F.col("log_message"), "User: ([a-z0-9._-]+@[a-z0-9.-]+)", 1)
)

# EXERCICE 4 : Extraction du nom d'utilisateur
df = df.withColumn(
    "username",
    F.regexp_extract(F.col("email"), "^([^@]+)", 1)
)

# EXERCICE 5 : Extraction du domaine
df = df.withColumn(
    "domaine",
    F.regexp_extract(F.col("email"), "@(.+)$", 1)
)

# EXERCICE 6 : Extraction de l'adresse IP
df = df.withColumn(
    "ip_address",
    F.regexp_extract(F.col("log_message"), "IP: (\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})", 1)
)

# EXERCICE 7 : Extraction de l'action
df = df.withColumn(
    "action",
    F.regexp_extract(F.col("log_message"), "(logged in|failed login)", 1)
)

# EXERCICE 8 : Validation de l'email
df = df.withColumn(
    "email_valide",
    F.when(F.col("email").rlike("^[a-z0-9._-]+@[a-z0-9.-]+\\.[a-z]{2,}$"), "OUI").otherwise("NON")
)

df.show()
spark.stop()