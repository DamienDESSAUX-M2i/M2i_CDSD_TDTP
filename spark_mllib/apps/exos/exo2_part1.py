# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/exo2_part1.py
# ===

import time

import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import (
    Imputer,
    OneHotEncoder,
    SQLTransformer,
    StandardScaler,
    StringIndexer,
    VectorAssembler,
)
from pyspark.ml.regression import (
    GBTRegressor,
    LinearRegression,
    RandomForestRegressionModel,
    RandomForestRegressor,
)
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("Exercice_Jour2_Weather")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/weather_data.csv")
)

# ===
# DataFrame analysis
# ===

print(f"\n{'=' * 64}")
print("Schema:")
print(f"{'=' * 64}")
df.printSchema()

print(f"\n{'=' * 64}")
print("First 5 lines:")
print(f"{'=' * 64}")
df.show(5)

print(f"\n{'=' * 64}")
print("Dimensions:")
print(f"{'=' * 64}")
print("Total number of lines: ", df.count())
print("Total number of columns: ", len(df.columns))

print(f"\n{'=' * 64}")
print("Statistics:")
print(f"{'=' * 64}")
df.describe().show()

print(f"\n{'=' * 64}")
print("Number of null per column:")
print(f"{'=' * 64}")
df.select(
    [F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]
).show()

# ===
# Target Analysis
# ===

print(f"\n{'=' * 64}")
print("Statistics 'temperature_max':")
print(f"{'=' * 64}")
df.select("temperature_max").describe().show()

print(f"\n{'=' * 64}")
print("Average 'temperature_max' per 'season':")
print(f"{'=' * 64}")
df.groupBy("season").agg(F.mean("temperature_max").alias("mean")).orderBy(
    F.col("mean").desc()
).show()

print(f"\n{'=' * 64}")
print("Average 'temperature_max' per 'region':")
print(f"{'=' * 64}")
df.groupBy("region").agg(F.mean("temperature_max").alias("mean")).orderBy(
    F.col("mean").desc()
).show()

# ===
# Pipeline
# ===

print(f"\n{'=' * 64}")
print("Compute pipeline")
print(f"{'=' * 64}")
print("[01/12] Imputer")
imputer = Imputer(
    inputCols=["humidity", "pressure_hpa"],
    outputCols=["humidity_imp", "pressure_imp"],
    strategy="median",
)

print("[02/12] SQLTransformer")
sql_transformer = SQLTransformer(
    statement="""
    SELECT
        *,
        (humidity_imp * uv_index / 10.0) AS temp_humidity_interaction
    FROM __THIS__
    """
)

print("[03/12] StringIndexer")
string_indexer = StringIndexer(
    inputCols=["season", "region"],
    outputCols=["season_idx", "region_idx"],
    handleInvalid="keep",
)

print("[04/12] OneHotEncoder")
one_hit_encoder = OneHotEncoder(
    inputCols=["season_idx", "region_idx"],
    outputCols=["season_ohe", "region_ohe"],
    dropLast=True,
)

print("[06/12] VectorAssembler")
vector_assembler = VectorAssembler(
    inputCols=[
        "month",
        "humidity_imp",
        "pressure_imp",
        "wind_speed_kmh",
        "cloud_cover_pct",
        "uv_index",
        "temp_humidity_interaction",
        "season_ohe",
        "region_ohe",
    ],
    outputCol="features",
    handleInvalid="skip",
)

print("[06/12] StandardScaler")
standard_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_scaled",
    withMean=True,
    withStd=True,
)

print("[07/12] Preprocessor pipeline")
preprocessor = Pipeline(
    stages=[
        imputer,
        sql_transformer,
        string_indexer,
        one_hit_encoder,
        vector_assembler,
        standard_scaler,
    ]
)

print("[08/12] Split 80/20")
train_df, test_df = df.randomSplit(weights=[0.8, 0.2], seed=42)

print("[09/12] RegressionEvaluator")
evaluator = RegressionEvaluator(
    predictionCol="prediction",
    labelCol="temperature_max",
)
results = {}

print("[10/12] LinearRegression")
lr = LinearRegression(
    featuresCol="features_scaled",
    labelCol="temperature_max",
    maxIter=100,
)
pipeline_lr = Pipeline(stages=preprocessor.getStages() + [lr])

# Entrainement du modèle
t0_lr = time.time()
model_lr = pipeline_lr.fit(train_df)
t1_lr = time.time()

# Prédiction
pred_lr = model_lr.transform(test_df)

# Métriques
rmse_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "rmse"})
r2_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "r2"})
mae_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "mae"})

results["LinearRegression"] = {
    "RMSE": rmse_lr,
    "R²": r2_lr,
    "MAE": mae_lr,
    "time(s)": t1_lr - t0_lr,
}

print("[11/12] RandomForestRegressor")
rf = RandomForestRegressor(
    featuresCol="features_scaled",
    labelCol="temperature_max",
    numTrees=100,
    maxDepth=6,
    seed=42,
)
pipeline_rf = Pipeline(stages=preprocessor.getStages() + [rf])

# Entrainement du modèle
t0_rf = time.time()
model_rf = pipeline_rf.fit(train_df)
t1_rf = time.time()

# Prédiction
pred_rf = model_rf.transform(test_df)

# Métriques
rmse_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "rmse"})
r2_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "r2"})
mae_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "mae"})

results["RandomForestRegressor"] = {
    "RMSE": rmse_rf,
    "R²": r2_rf,
    "MAE": mae_rf,
    "time(s)": t1_rf - t0_rf,
}

print("[12/12] GBTRegressor")
gbt = GBTRegressor(
    featuresCol="features_scaled",
    labelCol="temperature_max",
    maxIter=50,
    stepSize=0.1,
    maxDepth=4,
    seed=42,
)
pipeline_gbt = Pipeline(stages=preprocessor.getStages() + [gbt])

# Entrainement du modèle
t0_gbt = time.time()
model_gbt = pipeline_gbt.fit(train_df)
t1_gbt = time.time()

# Prédiction
pred_gbt = model_gbt.transform(test_df)

# Métriques
rmse_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "rmse"})
r2_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "r2"})
mae_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "mae"})

results["GBTRegressor"] = {
    "RMSE": rmse_gbt,
    "R²": r2_gbt,
    "MAE": mae_gbt,
    "time(s)": t1_gbt - t0_gbt,
}
print("\nPipeline ends successfully")

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(f"{'Model':<30} | {'RMSE':<10} | {'R²':<10} | {'MAE':<10} | {'time(s)':<10}")
for model, result in results.items():
    print(
        f"{model:<30} | {result['RMSE']:<10.2f} | {result['R²']:<10.2f} | {result['MAE']:<10.2f} | {result['time(s)']:<10.2f}"
    )

# ===
# Feature importance
# ===

rf_model: RandomForestRegressionModel = model_rf.stages[-1]
importances = rf_model.featureImportances.toArray()
features_names = [
    "month",
    "humidity_imp",
    "pressure_imp",
    "wind_speed_kmh",
    "cloud_cover_pct",
    "uv_index",
    "temp_humidity_interaction",
    "season_ohe",
    "region_ohe",
]
fi_pairs = sorted(
    zip(features_names[: len(importances)], importances), key=lambda x: -x[1]
)

print(f"\n{'=' * 64}")
print("Top 5 feature importance:")
print(f"{'=' * 64}")
print(f"{'feature':<30} | {'importance':<10} | {'bar'}")
for fname, importance in fi_pairs[:5]:
    bar = "▮" * int(importance * 100)
    print(f"{fname:<30} | {importance:<10.2f} | {bar}")


spark.stop()
