# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/exos/tp_final_partB.py
# ===

import json
import time
from pathlib import Path

import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.classification import (
    RandomForestClassificationModel,
    RandomForestClassifier,
)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, RegressionEvaluator
from pyspark.ml.feature import (
    Imputer,
    OneHotEncoder,
    StandardScaler,
    StringIndexer,
    VectorAssembler,
)
from pyspark.ml.regression import (
    RandomForestRegressionModel,
    RandomForestRegressor,
)
from pyspark.sql import SparkSession

EXOS_PATH = Path(__file__).parent.resolve()

# ## Partie B — Implémentation Spark MLlib

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("tp_final_partB")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "1g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .csv("/data/crop_yield.csv")
).drop("_c0")

# ### B.2 Analyse exploratoire Spark

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
print("Statistics 'hg/ha_yield':")
print(f"{'=' * 64}")
df.select(
    F.mean("hg/ha_yield").alias("mean"),
    F.min("hg/ha_yield").alias("min"),
    F.percentile("hg/ha_yield", 0.25).alias("q1"),
    F.median("hg/ha_yield").alias("median"),
    F.percentile("hg/ha_yield", 0.75).alias("q3"),
    F.max("hg/ha_yield").alias("max"),
).show()

# - Afficher le rendement moyen par type de culture (`Item`) — top 10
print(f"\n{'=' * 64}")
print("Top 10 average 'hg/ha_yield' per 'Item':")
print(f"{'=' * 64}")
df.groupby("Item").agg(F.mean("hg/ha_yield").alias("mean")).orderBy(
    F.col("mean").desc()
).show(10)

# - Afficher le rendement moyen par pays (`Area`) — top 10
print(f"\n{'=' * 64}")
print("Top 10 average 'hg/ha_yield' per 'Area':")
print(f"{'=' * 64}")
df.groupby("Area").agg(F.mean("hg/ha_yield").alias("mean")).orderBy(
    F.col("mean").desc()
).show(10)

# ### B.3 Création de la cible de classification
print(f"\n{'=' * 64}")
print("Compute 'high_yield':")
print(f"{'=' * 64}")
median_yield_spark = df.approxQuantile("hg/ha_yield", [0.5], 0.001)[0]
print(f"Median 'high_yield': {median_yield_spark:.0f} hg/ha")

df = df.withColumn(
    "high_yield", F.when(F.col("hg/ha_yield") > median_yield_spark, 1).otherwise(0)
)

print("Distribution 'high_yield':")
df.groupBy("high_yield").count().show()

# ### B.4 Pipeline MLlib — Régression
imputer = Imputer(
    inputCols=[
        "Year",
        "average_rain_fall_mm_per_year",
        "pesticides_tonnes",
        "avg_temp",
    ],
    outputCols=[
        "Year_imp",
        "average_rain_fall_mm_per_year_imp",
        "pesticides_tonnes_imp",
        "avg_temp_imp",
    ],
    strategy="median",
)

string_indexer = StringIndexer(
    inputCols=["Area", "Item"],
    outputCols=["Area_idx", "Item_idx"],
    handleInvalid="keep",
)

one_hit_encoder = OneHotEncoder(
    inputCols=["Area_idx", "Item_idx"],
    outputCols=["Area_ohe", "Item_ohe"],
    dropLast=True,
)

vector_assembler = VectorAssembler(
    inputCols=[
        "Year_imp",
        "average_rain_fall_mm_per_year_imp",
        "pesticides_tonnes_imp",
        "avg_temp_imp",
        "Area_ohe",
        "Item_ohe",
    ],
    outputCol="features",
    handleInvalid="skip",
)

standard_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_scaled",
    withMean=True,
    withStd=True,
)

preprocessor = Pipeline(
    stages=[
        imputer,
        string_indexer,
        one_hit_encoder,
        vector_assembler,
        standard_scaler,
    ]
)

rf_reg = RandomForestRegressor(
    featuresCol="features_scaled",
    labelCol="hg/ha_yield",
    seed=42,
)
pipeline_rf_reg = Pipeline(stages=preprocessor.getStages() + [rf_reg])

# ### B.5 Pipeline MLlib — Classification

# Réutiliser les mêmes étapes de prétraitement, changer uniquement le modèle final

rf_clf = RandomForestClassifier(
    featuresCol="features_scaled",
    labelCol="high_yield",
    predictionCol="prediction",
    numTrees=100,
    maxDepth=8,
    seed=42,
)
pipeline_rf_clf = Pipeline(stages=preprocessor.getStages() + [rf_clf])

# ### B.6 Split et entraînement avec mesure du temps

train_df, test_df = df.randomSplit(weights=[0.8, 0.2], seed=42)

print(f"\n{'=' * 64}")
print("Regressor Pipeline:")
print(f"{'=' * 64}")

t0_rf_reg = time.time()
model_rf_reg = pipeline_rf_reg.fit(train_df)
t1_rf_reg = time.time()

print("Fitting Regressor Pipeline completed")

print(f"\n{'=' * 64}")
print("Classifier Pipeline:")
print(f"{'=' * 64}")

t0_rf_clf = time.time()
model_rf_clf = pipeline_rf_clf.fit(train_df)
t1_rf_clf = time.time()

print("Fitting Classifier Pipeline completed")

# ### B.7 Évaluation

# **Régression :**

# - MAE
# - RMSE
# - R²

evaluator_reg = RegressionEvaluator(
    predictionCol="prediction",
    labelCol="hg/ha_yield",
)
results_reg = {}

pred_rf_reg = model_rf_reg.transform(test_df)

results_reg["regression"] = {
    "rmse": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "rmse"}),
    "r2": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "r2"}),
    "mae": evaluator_reg.evaluate(pred_rf_reg, {evaluator_reg.metricName: "mae"}),
    "time": t1_rf_reg - t0_rf_reg,
}

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(f"{'regression':<30} | {'rmse':<10} | {'r2':<10} | {'mae':<10} | {'time':<10}")
for type_, result in results_reg.items():
    print(
        f"{'RandomForestRegressor':<30} | {result['rmse']:<10.2f} | {result['r2']:<10.6f} | {result['mae']:<10.2f} | {result['time']:<10.6f}"
    )

# **Classification :**

# - Accuracy
# - F1-score
# - Matrice de confusion

evaluator = MulticlassClassificationEvaluator(
    predictionCol="prediction",
    labelCol="high_yield",
)
results_clf = {}

pred_rf_clf = model_rf_clf.transform(test_df)

results_clf["classification"] = {
    "accuracy": evaluator.evaluate(pred_rf_clf, {evaluator.metricName: "accuracy"}),
    "f1": evaluator.evaluate(pred_rf_clf, {evaluator.metricName: "f1"}),
    "time": t1_rf_clf - t0_rf_clf,
}

print()
print(f"{'classification':<30} | {'accuracy':<10} | {'f1':<10} | {'time':<10}")
for model, result in results_clf.items():
    print(
        f"{'RandomForestClassifier':<30} | {result['accuracy']:<10.6f} | {result['f1']:<10.6f} | {result['time']:<10.6f}"
    )

# ### B.8 Feature Importances Spark
print(f"\n{'=' * 64}")
print("Feature importance:")
print(f"{'=' * 64}")
df_before_scaling = train_df
for stage in model_rf_reg.stages[:-2]:
    df_before_scaling = stage.transform(df_before_scaling)
attrs = df_before_scaling.schema["features"].metadata["ml_attr"]["attrs"]

feature_names = [attr["name"] for attr_type in attrs for attr in attrs[attr_type]]

rf_reg_model: RandomForestRegressionModel = model_rf_reg.stages[-1]
importances_reg = rf_reg_model.featureImportances.toArray()

fi_pairs_reg = sorted(
    zip(feature_names[: len(importances_reg)], importances_reg), key=lambda x: -x[1]
)

print("Top 10 feature importance RandomForestClassifier:")
print(f"{'feature':<30} | {'importance':<10} | {'bar'}")
for fname, importance in fi_pairs_reg[:10]:
    bar = "▮" * int(importance * 100)
    print(f"{fname:<30} | {importance:<10.2f} | {bar}")

rf_clf_model: RandomForestClassificationModel = model_rf_clf.stages[-1]
importances_clf = rf_clf_model.featureImportances.toArray()

fi_pairs_clf = sorted(
    zip(feature_names[: len(importances_clf)], importances_clf), key=lambda x: -x[1]
)

print("\nTop 10 feature importance RandomForestClassifier:")
print(f"{'feature':<30} | {'importance':<10} | {'bar'}")
for fname, importance in fi_pairs_clf[:10]:
    bar = "▮" * int(importance * 100)
    print(f"{fname:<30} | {importance:<10.2f} | {bar}")

# ### B.9 Sauvegarde et export JSON

# - Sauvegarder les deux modèles MLlib avec `.write().overwrite().save()`
print(f"\n{'=' * 64}")
print("Save pipelines:")
print(f"{'=' * 64}")
save_path_reg = EXOS_PATH / "rf_reg_pipeline"
model_rf_reg.write().overwrite().save(save_path_reg.as_posix())
print("Regressor Pipeline save path: ", save_path_reg)

save_path_clf = EXOS_PATH / "rf_clf_pipeline"
model_rf_clf.write().overwrite().save(save_path_clf.as_posix())
print("Classifier Pipeline save path: ", save_path_clf)

# - Exporter les métriques dans un fichier `spark_results.json` avec la même structure que `sklearn_results.json` (voir A.8)
print(f"\n{'=' * 64}")
print("Save Spark results:")
print(f"{'=' * 64}")
data = {}
data.update(results_reg)
data.update(results_clf)
json_path = EXOS_PATH / "spark_results.json"
json_path.write_text(data=json.dumps(data), encoding="utf-8")
print("Spark results path: ", json_path)


spark.stop()
