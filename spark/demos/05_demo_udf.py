import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("demo_udf").getOrCreate()

# Data
data = [
    ("Toto", 25, "Ingénieur", 50000.0),
    ("Tata", 38, "Manager", 60000.0),
    ("Titi", 35, "Développeur", 30000.0),
]

# DataFrame
df = spark.createDataFrame(data=data, schema=["nom", "age", "poste", "salaire"])


# UDF
def categorie_age(age: int) -> str:
    if age < 30:
        return "Junior"
    elif age < 40:
        return "Expérimenté"
    else:
        return "Senior"


def salaire_bonus(salaire: float) -> float:
    return salaire * 1.1


categorieAge = F.udf(f=categorie_age, returnType=StringType())
salaireBonus = F.udf(f=salaire_bonus, returnType=DoubleType())

dfWithUdf = df.withColumn(
    colName="categorie_age", col=categorieAge(F.col("age"))
).withColumn(colName="salaire_bonus", col=salaireBonus(F.col("salaire")))
