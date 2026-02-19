# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/tp2.py
# ===


import time

import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.classification import (
    GBTClassifier,
    LogisticRegression,
    RandomForestClassificationModel,
    RandomForestClassifier,
)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, RegressionEvaluator
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
    RandomForestRegressor,
)
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("Exercice_Jour2_Flights")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/flights.csv")
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
size_df = df.count()
print("Total number of lines: ", size_df)
print("Total number of columns: ", len(df.columns))

print(f"\n{'=' * 64}")
print("Statistics:")
print(f"{'=' * 64}")
df.drop("flight_id").describe().show()

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
print("Statistics 'delay_minutes':")
print(f"{'=' * 64}")
df.select(
    F.mean("delay_minutes").alias("mean"),
    F.min("delay_minutes").alias("min"),
    F.percentile("delay_minutes", 0.25).alias("q1"),
    F.median("delay_minutes").alias("median"),
    F.percentile("delay_minutes", 0.75).alias("q3"),
    F.max("delay_minutes").alias("max"),
    (F.sum(F.when(F.col("delay_minutes") > 0, 1).otherwise(0)) / size_df * 100).alias(
        "delay_rate"
    ),
).show()

print(f"\n{'=' * 64}")
print("Average 'delay_minutes' per 'airline':")
print(f"{'=' * 64}")
df.groupBy("airline").agg(F.mean("delay_minutes").alias("mean")).orderBy(
    F.col("mean").desc()
).show()

print(f"\n{'=' * 64}")
print("Average 'delay_minutes' per 'origin':")
print(f"{'=' * 64}")
df.groupBy("origin").agg(F.mean("delay_minutes").alias("mean")).orderBy(
    F.col("mean").desc()
).show()

# ===
# Regression Pipeline
# ===

print(f"\n{'=' * 64}")
print("Compute regression pipeline")
print(f"{'=' * 64}")
print("[01/12] Imputer")
imputer = Imputer(
    inputCols=["weather_score", "runway_congestion"],
    outputCols=["weather_score_imp", "runway_congestion_imp"],
    strategy="median",
)

print("[02/12] SQLTransformer")
sql_transformer = SQLTransformer(
    statement="""
    SELECT
        *,
        CASE
            WHEN departure_hour IN (7, 8, 17, 18, 19) THEN 1
            ELSE 0
        END AS is_peak_departure
    FROM __THIS__
    """
)

print("[03/12] StringIndexer")
string_indexer = StringIndexer(
    inputCols=["airline", "origin"],
    outputCols=["airline_idx", "origin_idx"],
    handleInvalid="keep",
)

print("[04/12] OneHotEncoder")
one_hit_encoder = OneHotEncoder(
    inputCols=["airline_idx", "origin_idx"],
    outputCols=["airline_ohe", "origin_ohe"],
    dropLast=True,
)

print("[06/12] VectorAssembler")
vector_assembler = VectorAssembler(
    inputCols=[
        "distance_km",
        "nb_passengers",
        "weather_score_imp",
        "runway_congestion_imp",
        "aircraft_age_years",
        "departure_hour",
        "is_peak_departure",
        "airline_ohe",
        "origin_ohe",
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
evaluator_reg = RegressionEvaluator(
    predictionCol="prediction",
    labelCol="delay_minutes",
)
results_reg = {}

print("[10/12] LinearRegression")
lr_reg = LinearRegression(
    featuresCol="features_scaled",
    labelCol="delay_minutes",
    maxIter=100,
    regParam=0.1,
)
pipeline_lr_reg = Pipeline(stages=preprocessor.getStages() + [lr_reg])

# Entrainement du modèle
t0_lr_reg = time.time()
model_lr_reg = pipeline_lr_reg.fit(train_df)
t1_lr_reg = time.time()

# Prédiction
pred_lr_reg = model_lr_reg.transform(test_df)

# Métriques
results_reg["LinearRegression"] = {
    "RMSE": evaluator_reg.evaluate(pred_lr_reg, {evaluator_reg.metricName: "rmse"}),
    "R²": evaluator_reg.evaluate(pred_lr_reg, {evaluator_reg.metricName: "r2"}),
    "MAE": evaluator_reg.evaluate(pred_lr_reg, {evaluator_reg.metricName: "mae"}),
    "time(s)": t1_lr_reg - t0_lr_reg,
}

print("[11/12] RandomForestRegressor")
rf_reg = RandomForestRegressor(
    featuresCol="features_scaled",
    labelCol="delay_minutes",
    numTrees=100,
    maxDepth=8,
    seed=42,
)
pipeline_rf_reg = Pipeline(stages=preprocessor.getStages() + [rf_reg])

# Entrainement du modèle
t0_rf_reg = time.time()
model_rf_reg = pipeline_rf_reg.fit(train_df)
t1_rf_reg = time.time()

# Prédiction
pred_rf_reg = model_rf_reg.transform(test_df)

# Métriques
results_reg["RandomForestRegressor"] = {
    "RMSE": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "rmse"}),
    "R²": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "r2"}),
    "MAE": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "mae"}),
    "time(s)": t1_rf_reg - t0_rf_reg,
}

print("[12/12] GBTRegressor")
gbt_reg = GBTRegressor(
    featuresCol="features_scaled",
    labelCol="delay_minutes",
    maxIter=50,
    stepSize=0.1,
    maxDepth=5,
    seed=42,
)
pipeline_gbt_reg = Pipeline(stages=preprocessor.getStages() + [gbt_reg])

# Entrainement du modèle
t0_gbt_reg = time.time()
model_gbt_reg = pipeline_gbt_reg.fit(train_df)
t1_gbt_reg = time.time()

# Prédiction
pred_gbt_reg = model_gbt_reg.transform(test_df)

# Métriques
results_reg["GBTRegressor"] = {
    "RMSE": evaluator_reg.evaluate(pred_gbt_reg, {evaluator_reg.metricName: "rmse"}),
    "R²": evaluator_reg.evaluate(pred_gbt_reg, {evaluator_reg.metricName: "r2"}),
    "MAE": evaluator_reg.evaluate(pred_gbt_reg, {evaluator_reg.metricName: "mae"}),
    "time(s)": t1_gbt_reg - t0_gbt_reg,
}
print("\nPipeline ends successfully")

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(f"{'Model':<30} | {'RMSE':<10} | {'R²':<10} | {'MAE':<10} | {'time(s)':<10}")
for model, result in results_reg.items():
    print(
        f"{model:<30} | {result['RMSE']:<10.6f} | {result['R²']:<10.6f} | {result['MAE']:<10.6f} | {result['time(s)']:<10.6f}"
    )
best_model_reg_name = max(results_reg, key=lambda x: results_reg[x]["R²"])
print(f"---> Best model: {best_model_reg_name}")

# ===
# Target Analysis
# ===

print(f"\n{'=' * 64}")
print("Distribution 'severe_delay':")
print(f"{'=' * 64}")
df.groupBy("severe_delay").agg((F.count("*") / size_df * 100).alias("rate")).show()

print("---> Class imbalance")

# ===
# Pipeline Classification
# ===

print(f"\n{'=' * 64}")
print("Compute classification pipeline")
print(f"{'=' * 64}")
print("[01-07/11] Preprocessing")
print("[08/11] MulticlassClassificationEvaluator")
evaluator = MulticlassClassificationEvaluator(
    predictionCol="prediction",
    labelCol="severe_delay",
)
results_clf = {}
preds_clf = {}

print("[09/11] LogisticRegression")
lr_clf = LogisticRegression(
    featuresCol="features_scaled",
    labelCol="severe_delay",
    predictionCol="prediction",
    maxIter=100,
    regParam=0.05,
    family="binomial",
)
pipeline_lr_clf = Pipeline(stages=preprocessor.getStages() + [lr_clf])

# Entrainement du modèle
t0_lr_clf = time.time()
model_lr_clf = pipeline_lr_clf.fit(train_df)
t1_lr_clf = time.time()

# Prédiction
pred_lr_clf = model_lr_clf.transform(test_df)
preds_clf["LogisticRegression"] = pred_lr_clf

# Métriques
results_clf["LogisticRegression"] = {
    "accuracy": evaluator.evaluate(pred_lr_clf, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_lr_clf, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_lr_clf, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(pred_lr_clf, {evaluator.metricName: "weightedRecall"}),
    "time(s)": t1_lr_clf - t0_lr_clf,
}

print("[10/11] RandomForestClassifier")
rf_clf = RandomForestClassifier(
    featuresCol="features_scaled",
    labelCol="severe_delay",
    predictionCol="prediction",
    numTrees=100,
    maxDepth=8,
    seed=42,
)
pipeline_rf_clf = Pipeline(stages=preprocessor.getStages() + [rf_clf])

# Entrainement du modèle
t0_rf_clf = time.time()
model_rf_clf = pipeline_rf_clf.fit(train_df)
t1_rf_clf = time.time()

# Prédiction
pred_rf_clf = model_rf_clf.transform(test_df)
preds_clf["RandomForestClassifier"] = pred_rf_clf

# Métriques
results_clf["RandomForestClassifier"] = {
    "accuracy": evaluator.evaluate(pred_rf_clf, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_rf_clf, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_rf_clf, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(pred_rf_clf, {evaluator.metricName: "weightedRecall"}),
    "time(s)": t1_rf_clf - t0_rf_clf,
}

print("[11/11] GBTClassifier")
gbt_clf = GBTClassifier(
    featuresCol="features_scaled",
    labelCol="severe_delay",
    predictionCol="prediction",
    maxIter=50,
    stepSize=0.1,
    maxDepth=5,
    seed=42,
)
pipeline_gbt_clf = Pipeline(stages=preprocessor.getStages() + [gbt_clf])

# Entrainement du modèle
t0_gbt_clf = time.time()
model_gbt_clf = pipeline_gbt_clf.fit(train_df)
t1_gbt_clf = time.time()

# Prédiction
pred_gbt_clf = model_gbt_clf.transform(test_df)
preds_clf["GBTClassifier"] = pred_gbt_clf

# Métriques
results_clf["GBTClassifier"] = {
    "accuracy": evaluator.evaluate(pred_gbt_clf, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_gbt_clf, {evaluator.metricName: "f1"}),
    "precision": evaluator.evaluate(
        pred_gbt_clf, {evaluator.metricName: "weightedPrecision"}
    ),
    "recall": evaluator.evaluate(
        pred_gbt_clf, {evaluator.metricName: "weightedRecall"}
    ),
    "time(s)": t1_gbt_clf - t0_gbt_clf,
}

print("\nPipeline ends successfully")

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(
    f"{'Model':<30} | {'accuracy':<10} | {'f1':<10} | {'precision':<10} | {'recall':<10} | {'time(s)':<10}"
)
for model, result in results_clf.items():
    print(
        f"{model:<30} | {result['accuracy']:<10.6f} | {result['f1']:<10.6f} | {result['precision']:<10.6f} | {result['recall']:<10.6f} | {result['time(s)']:<10.6f}"
    )

# Best model
best_model_clf_name = max(results_clf, key=lambda x: results_clf[x]["f1"])
print(f"---> Best model: {best_model_clf_name}")

# Confusion matrix
preds_and_labels = (
    preds_clf[best_model_clf_name]
    .select(["prediction", "severe_delay"])
    .withColumn("label", F.col("severe_delay").cast(FloatType()))
    .orderBy("prediction")
)
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
print(f"Confusion matrix of {best_model_clf_name}:")
print(f"{'=' * 64}")
print("        Prediction")
print(f"Label   TP: {tp:<10} | FN: {fn:<10}")
print(f"        FP: {fp:<10} | TN: {tn:<10}")


# Feature importance
rf_model: RandomForestClassificationModel = model_rf_clf.stages[-1]
importances = rf_model.featureImportances.toArray()
features_names = [
    "distance_km",
    "nb_passengers",
    "weather_score_imp",
    "runway_congestion_imp",
    "aircraft_age_years",
    "departure_hour",
    "is_peak_departure",
    "airline_ohe",
    "origin_ohe",
]
fi_pairs = sorted(
    zip(features_names[: len(importances)], importances), key=lambda x: -x[1]
)

print(f"\n{'=' * 64}")
print("Top 5 feature importance RandomForestClassifier:")
print(f"{'=' * 64}")
print(f"{'feature':<30} | {'importance':<10} | {'bar'}")
for fname, importance in fi_pairs[:5]:
    bar = "▮" * int(importance * 100)
    print(f"{fname:<30} | {importance:<10.2f} | {bar}")


spark.stop()
