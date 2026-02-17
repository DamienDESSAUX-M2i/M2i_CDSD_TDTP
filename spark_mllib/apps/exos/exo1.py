# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/exo1.py
# ===


import pyspark.sql.functions as F
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
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
    builder.appName("Exercice_Jour1_Fitness")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/fitness_sessions.csv")
)

print(f"\n{'=' * 64}")
print("Schema:")
df.printSchema()

print(f"\n{'=' * 64}")
print("First 5 lines:")
df.show(5)

print(f"\n{'=' * 64}")
print("Total number of lines: ", df.count())
print("Total number of columns: ", len(df.columns))

print(f"\n{'=' * 64}")
print("Statistics:")
df.describe().show()

print(f"\n{'=' * 64}")
print("Number of null per column:")
df.select(
    [F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]
).show()

print(f"\n{'=' * 64}")
print("statistics column named 'calories_burned':")
df.select(
    F.min("calories_burned").alias("min"),
    F.max("calories_burned").alias("max"),
    F.mean("calories_burned").alias("mean"),
    F.median("calories_burned").alias("median"),
).show()

print("Average 'calories_burned' per 'activity_type':")
df.groupBy("activity_type").agg(F.mean("calories_burned").alias("mean")).show()

print(f"\n{'=' * 64}")
print("[01/11] Imputer")
imputer = Imputer(
    inputCols=["duration_minutes", "heart_rate_avg", "steps_count"],
    outputCols=["duration_imp", "heart_rate_imp", "steps_imp"],
    strategy="median",
)

print("[02/11] SQLTransformer")
new_features = SQLTransformer(
    statement="""
    SELECT
        *,
        (heart_rate_imp * duration_imp / 60.0) AS effort_score,
        CASE
            WHEN activity_type IN ('running', 'cycling', 'swimming') THEN 1
            ELSE 0
        END AS is_active_sport
    FROM __THIS__
    """
)

print("[03/11] StringIndexer")
multi_idx = StringIndexer(
    inputCols=["activity_type", "intensity_level"],
    outputCols=["activity_idx", "intensity_idx"],
    handleInvalid="keep",
)

print("[04/11] OneHotEncoder")
ohe = OneHotEncoder(
    inputCol="intensity_idx",
    outputCol="intensity_ohe",
    dropLast=True,
)

print("[05/11] VectorAssembler")
assembler = VectorAssembler(
    inputCols=[
        "activity_idx",
        "intensity_ohe",
        "duration_imp",
        "heart_rate_imp",
        "distance_km",
        "steps_imp",
        "sleep_hours_prev",
        "user_age",
        "is_morning",
        "effort_score",
        "is_active_sport",
    ],
    outputCol="features",
    handleInvalid="skip",
)

print("[06/11] StandardScaler")
std_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std",
    withMean=True,
    withStd=True,
)

print("[07/11] Split data 80/20")
train_df, test_df = df.randomSplit(weights=[0.8, 0.2], seed=42)

print("[08/11] Pipeline")
pipeline = Pipeline(
    stages=[
        imputer,
        new_features,
        multi_idx,
        ohe,
        assembler,
        std_scaler,
    ]
)

pipeline_model = pipeline.fit(train_df)

print("[09/11] Save pipeline")
pipeline_path = "/data/models/exo1_pipeline"
pipeline_model.write().overwrite().save(pipeline_path)

print("[10/11] Load pipeline")
pipeline_load = PipelineModel.load(pipeline_path)

print("[11/11] Transform data")
train_prepared = pipeline_load.transform(train_df)
test_prepared = pipeline_load.transform(test_df)

print(f"\n{'=' * 64}")
print("DataFrame train prepared:")
train_prepared.select("features_std").show(5, truncate=False)

print(f"\n{'=' * 64}")
print("DataFrame test prepared:")
test_prepared.select("features_std").show(5, truncate=False)

spark.stop()
