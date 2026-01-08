from pyspark.sql import Row, SparkSession
from pyspark.sql.types import StringType, StructField, StructType

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("demo_join").getOrCreate()

# Schéma Livres
livresSchema = StructType(
    [
        StructField(name="book_id", dataType=StringType(), nullable=False),
        StructField(name="title", dataType=StringType(), nullable=False),
        StructField(name="author_id", dataType=StringType(), nullable=True),
    ]
)

# Data Livres
livresData = [
    Row("L1", "Livre 1", "A1"),
    Row("L2", "Livre 2", "A2"),
    Row("L3", "Livre 3", "A1"),
    Row("L4", "Livre 4", "A3"),
    Row("L5", "Livre 5", None),
]

# RDD Livres
livresDRR = spark.sparkContext.parallelize(livresData)

# DataFrame Livres
dfLivres = spark.createDataFrame(data=livresData, schema=livresSchema)

# Schéma Authors
authorsSchema = StructType(
    [
        StructField(name="author_id", dataType=StringType(), nullable=False),
        StructField(name="name", dataType=StringType(), nullable=False),
    ]
)

# Data Authors
authorsData = [
    Row("A1", "Nom 1"),
    Row("A2", "Nom 2"),
    Row("A3", "Nom 3"),
    Row("A4", "Nom 4"),
]

# RDD Authors
authorsDRR = spark.sparkContext.parallelize(authorsData)

# DataFrame Authors
dfAuthors = spark.createDataFrame(data=authorsData, schema=authorsSchema)

# Inner Join
dfInnerJoin = dfLivres.join(other=dfAuthors, on="author_id", how="inner")
dfInnerJoin.show()

# Left Join
dfLeftJoin = dfLivres.join(
    other=dfAuthors, on=(dfLivres["author_id"] == dfAuthors["author_id"]), how="left"
)
dfLeftJoin.show()

# Anti Join
dfAntiJoin = dfLivres.join(other=dfAuthors, on=["author_id"], how="anti")
dfAntiJoin.show()
