# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/exo2_part2.py
# ===


import time

import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.classification import (
    GBTClassifier,
    LogisticRegression,
    RandomForestClassifier,
)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import (
    Imputer,
    OneHotEncoder,
    StandardScaler,
    StringIndexer,
    VectorAssembler,
)
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("Exercice_Jour2_Rain")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/rain_prediction.csv")
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
print("Distribution 'will_rain':")
print(f"{'=' * 64}")
df.groupBy("will_rain").agg(F.count("*")).show()

print("---> Class imbalance")

# ===
# Pipeline
# ===

print(f"\n{'=' * 64}")
print("Compute pipeline")
print(f"{'=' * 64}")
print("[01/11] Imputer")
imputer = Imputer(
    inputCols=["humidity", "pressure_hpa", "dew_point"],
    outputCols=["humidity_imp", "pressure_imp", "dew_point_imp"],
    strategy="median",
)

print("[02/11] StringIndexer")
string_indexer = StringIndexer(
    inputCols=["season", "region"],
    outputCols=["season_idx", "region_idx"],
    handleInvalid="keep",
)

print("[03/11] OneHotEncoder")
one_hit_encoder = OneHotEncoder(
    inputCols=["season_idx", "region_idx"],
    outputCols=["season_ohe", "region_ohe"],
    dropLast=True,
)

print("[04/11] VectorAssembler")
vector_assembler = VectorAssembler(
    inputCols=[
        "humidity_imp",
        "pressure_imp",
        "wind_speed_kmh",
        "cloud_cover_pct",
        "temperature_morning",
        "dew_point_imp",
        "season_ohe",
        "region_ohe",
    ],
    outputCol="features",
    handleInvalid="skip",
)

print("[05/11] StandardScaler")
standard_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_scaled",
    withMean=True,
    withStd=True,
)

print("[06/11] Preprocessor pipeline")
preprocessor = Pipeline(
    stages=[
        imputer,
        string_indexer,
        one_hit_encoder,
        vector_assembler,
        standard_scaler,
    ]
)

print("[07/11] Split 80/20")
train_df, test_df = df.randomSplit(weights=[0.8, 0.2], seed=42)

print("[08/11] MulticlassClassificationEvaluator")
evaluator = MulticlassClassificationEvaluator(
    predictionCol="prediction",
    labelCol="will_rain",
)
results = {}
preds = {}

print("[09/11] LogisticRegression")
lr = LogisticRegression(
    featuresCol="features_scaled",
    labelCol="will_rain",
    predictionCol="prediction",
    maxIter=100,
    regParam=0.05,
    family="binomial",
)
pipeline_lr = Pipeline(stages=preprocessor.getStages() + [lr])

# Entrainement du modèle
t0_lr = time.time()
model_lr = pipeline_lr.fit(train_df)
t1_lr = time.time()

# Prédiction
pred_lr = model_lr.transform(test_df)
preds["LogisticRegression"] = pred_lr

# Métriques
results["LogisticRegression"] = {
    "accuracy": evaluator.evaluate(pred_lr, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_lr, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_lr, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(pred_lr, {evaluator.metricName: "weightedRecall"}),
    "time(s)": t1_lr - t0_lr,
}

print("[10/11] RandomForestClassifier")
rf = RandomForestClassifier(
    featuresCol="features_scaled",
    labelCol="will_rain",
    predictionCol="prediction",
    numTrees=100,
    maxDepth=8,
    seed=42,
)
pipeline_rf = Pipeline(stages=preprocessor.getStages() + [rf])

# Entrainement du modèle
t0_rf = time.time()
model_rf = pipeline_rf.fit(train_df)
t1_rf = time.time()

# Prédiction
pred_rf = model_rf.transform(test_df)
preds["LogisticRegression"] = pred_rf

# Métriques
results["RandomForestClassifier"] = {
    "accuracy": evaluator.evaluate(pred_rf, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_rf, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_rf, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(pred_rf, {evaluator.metricName: "weightedRecall"}),
    "time(s)": t1_rf - t0_rf,
}

print("[11/11] GBTClassifier")
gbt = GBTClassifier(
    featuresCol="features_scaled",
    labelCol="will_rain",
    predictionCol="prediction",
    maxIter=50,
    stepSize=0.1,
    maxDepth=5,
    seed=42,
)
pipeline_gbt = Pipeline(stages=preprocessor.getStages() + [gbt])

# Entrainement du modèle
t0_gbt = time.time()
model_gbt = pipeline_gbt.fit(train_df)
t1_gbt = time.time()

# Prédiction
pred_gbt = model_gbt.transform(test_df)
preds["GBTClassifier"] = pred_gbt

# Métriques
results["GBTClassifier"] = {
    "accuracy": evaluator.evaluate(pred_gbt, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_gbt, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_gbt, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(pred_gbt, {evaluator.metricName: "weightedRecall"}),
    "time(s)": t1_gbt - t0_gbt,
}

print("\nPipeline ends successfully")

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(
    f"{'Model':<30} | {'accuracy':<10} | {'f1':<10} | {'precision':<10} | {'recall':<10} | {'time(s)':<10}"
)
for model, result in results.items():
    print(
        f"{model:<30} | {result['accuracy']:<10.4f} | {result['f1']:<10.4f} | {result['precision']:<10.4f} | {result['recall']:<10.4f} | {result['time(s)']:<10.4f}"
    )

# Best model
best_model_name = max(results, key=lambda x: results[x]["f1"])
print(f"---> Best model: {best_model_name}")

# Confusion matrix
preds_and_labels = (
    preds[best_model_name]
    .select(["prediction", "will_rain"])
    .withColumn("label", F.col("will_rain").cast(FloatType()))
    .orderBy("prediction")
)
preds_and_labels = preds_and_labels.select(["prediction", "label"])
metrics = MulticlassMetrics(preds_and_labels.rdd.map(tuple))

confusion_matrix = metrics.confusionMatrix().toArray()
tn = confusion_matrix[0, 0]
fp = confusion_matrix[0, 1]
fn = confusion_matrix[1, 0]
tp = confusion_matrix[1, 1]
print(f"\n{'=' * 64}")
print(f"Confusion matrix of {best_model_name}:")
print(f"{'=' * 64}")
print("        Prediction")
print(f"Label   TP: {tp:<10} | FN: {fn:<10}")
print(f"        FP: {fp:<10} | TN: {tn:<10}")

# Autre méthode
confusion = preds_and_labels.agg(
    F.sum(
        F.when((F.col("prediction") == 1.0) & (F.col("label") == 1.0), 1).otherwise(0)
    ).alias("TP"),
    F.sum(
        F.when((F.col("prediction") == 1.0) & (F.col("label") == 0.0), 1).otherwise(0)
    ).alias("FP"),
    F.sum(
        F.when((F.col("prediction") == 0.0) & (F.col("label") == 1.0), 1).otherwise(0)
    ).alias("FN"),
    F.sum(
        F.when((F.col("prediction") == 0.0) & (F.col("label") == 0.0), 1).otherwise(0)
    ).alias("TN"),
).collect()[0]

tp, fp, fn, tn = confusion["TP"], confusion["FP"], confusion["FN"], confusion["TN"]

print(f"\n{'=' * 64}")
print(f"Confusion matrix of {best_model_name}:")
print(f"{'=' * 64}")
print("        Prediction")
print(f"Label   TP: {tp:<10} | FN: {fn:<10}")
print(f"        FP: {fp:<10} | TN: {tn:<10}")
