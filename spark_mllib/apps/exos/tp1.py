# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/tp1.py
# ===


import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    Bucketizer,
    Imputer,
    OneHotEncoder,
    SQLTransformer,
    StandardScaler,
    StringIndexer,
    VectorAssembler,
)
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("TP_SoundStream_J1")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/streams.csv")
)

print(f"\n{'=' * 64}")
print("Schema:")
print(f"{'=' * 64}")
df.printSchema()

print(f"\n{'=' * 64}")
print("First 10 lines:")
print(f"{'=' * 64}")
df.show(10)

print(f"\n{'=' * 64}")
print("Dimensions")
print(f"{'=' * 64}")
nb_lines = df.count()
print("Total number of lines: ", nb_lines)
print("Total number of columns: ", len(df.columns))

print(f"\n{'=' * 64}")
print("Statistics:")
print(f"{'=' * 64}")
df.describe().show()

print(f"\n{'=' * 64}")
print("Null per column:")
print(f"{'=' * 64}")
null_counts_df = df.select(
    [F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]
)
stack_expr = "stack({0}, {1}) as (column_name, null_count)".format(
    len(df.columns), ", ".join([f"'{c}', {c}" for c in df.columns])
)
result_df = null_counts_df.selectExpr(stack_expr).withColumn(
    "null_percentage", F.round(F.col("null_count") / nb_lines * 100, 2)
)
result_df.show()

print(f"\n{'=' * 64}")
print("Distribution per 'genre':")
print(f"{'=' * 64}")
df.groupBy("genre").agg(F.count("*").alias("count")).orderBy(
    F.col("genre").desc()
).show()

print(f"\n{'=' * 64}")
print("Distribution per 'sub_type':")
print(f"{'=' * 64}")
df.groupBy("sub_type").agg(F.count("*").alias("count")).orderBy(
    F.col("sub_type").desc()
).show()

print(f"\n{'=' * 64}")
print("Distribution per 'device_type':")
print(f"{'=' * 64}")
df.groupBy("device_type").agg(F.count("*").alias("count")).orderBy(
    F.col("device_type").desc()
).show()

print(f"\n{'=' * 64}")
print("Statistics column 'engagement_score':")
print(f"{'=' * 64}")
df.select(
    F.min("engagement_score").alias("min"),
    F.percentile("engagement_score", 0.25).alias("q1"),
    F.median("engagement_score").alias("median"),
    F.mean("engagement_score").alias("mean"),
    F.percentile("engagement_score", 0.75).alias("q3"),
    F.max("engagement_score").alias("max"),
).show()

print(f"\n{'=' * 64}")
print("Distribution column 'engagement_score':")
print(f"{'=' * 64}")
df_score_bucket = df.withColumn(
    "engagement_score_bucket",
    F.when(F.col("engagement_score") < 25, "0-24")
    .when((F.col("engagement_score") >= 25) & (F.col("engagement_score") < 50), "25-49")
    .when((F.col("engagement_score") >= 50) & (F.col("engagement_score") < 75), "50-74")
    .otherwise("75+"),
)
df_score_bucket.groupBy("engagement_score_bucket").count().orderBy(
    "engagement_score_bucket"
).show()

print(f"\n{'=' * 64}")
print("Preprocessing pipeline")
print(f"{'=' * 64}")
print("[01/12] Imputer")
imputer = Imputer(
    inputCols=["listen_duration_s", "nb_likes"],
    outputCols=["listen_duration_imp", "nb_likes_imp"],
    strategy="median",
)

print("[02/12] SQLTransformer")
sql_transformer = SQLTransformer(
    statement="""
    SELECT
        *,
        (listen_duration_imp / 60.0) AS listen_minutes,
        (engagement_score / (nb_likes_imp + 1)) AS engagement_per_like,
        CASE
            WHEN hour_of_day BETWEEN 18 AND 22 THEN 1
            ELSE 0
        END AS peak_hour
    FROM __THIS__
    """
)

print("[03/12] Bucketizer")
bucketizer = Bucketizer(
    splits=[0, 12, 18, 24],
    inputCol="hour_of_day",
    outputCol="time_slot",
)

print("[04/12] StringIndexer")
string_indexer = StringIndexer(
    inputCols=["genre", "sub_type", "device_type"],
    outputCols=["genre_idx", "sub_type_idx", "device_type_idx"],
    handleInvalid="keep",
)

print("[05/12] OneHotEncoder")
one_hit_encoder = OneHotEncoder(
    inputCols=["genre_idx", "device_type_idx"],
    outputCols=["genre_ohe", "device_type_ohe"],
    dropLast=True,
)

print("[06/12] VectorAssembler")
vector_assembler = VectorAssembler(
    inputCols=[
        "genre_ohe",
        "sub_type_idx",
        "hour_of_day",
        "listen_duration_imp",
        "nb_skips",
        "nb_likes_imp",
        "device_type_ohe",
        "explicit_content",
        "listen_minutes",
        "engagement_per_like",
        "peak_hour",
    ],
    outputCol="features",
    handleInvalid="skip",
)

print("[07/12] StandardScaler")
standard_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std",
    withMean=True,
    withStd=True,
)

print("[08/12] Split 80/20")
train_df, test_df = df.randomSplit(
    weights=[0.8, 0.2],
    seed=42,
)

print("[09/12] Pipeline")
pipeline = Pipeline(
    stages=[
        imputer,
        sql_transformer,
        bucketizer,
        string_indexer,
        one_hit_encoder,
        vector_assembler,
        standard_scaler,
    ]
)

print("[10/12] fit on train")
pipeline_model = pipeline.fit(train_df)

print("[11/12] transform train and test")
train_transformed = pipeline_model.transform(train_df)
test_transformed = pipeline_model.transform(test_df)

print("[12/12] Save pipeline")
pipeline_model.write().overwrite().save("/data/models/tp1_pipeline")

print("\nPipeline ends successfully")
spark.stop()
