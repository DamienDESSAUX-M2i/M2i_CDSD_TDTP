# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/demos/demo_transformers.py
# ===


import time
from itertools import chain

import pyspark.sql.functions as F
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import (
    Bucketizer,
    Imputer,
    OneHotEncoder,
    SQLTransformer,
    StandardScaler,
    StringIndexer,
    VectorAssembler,
)
from pyspark.ml.regression import GBTRegressor, LinearRegression, RandomForestRegressor
from pyspark.sql import SparkSession

builder: SparkSession.Builder = SparkSession.builder
spark = (
    builder.appName("demo_transformers")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

neighborhood_map = {0: "Centre", 1: "Nord", 2: "Sud", 3: "Est", 4: "Ouest"}
house_type_map = {0: "house", 1: "apartment", 2: "studio"}
n_map = F.create_map([F.lit(x) for x in chain(*neighborhood_map.items())])
h_map = F.create_map([F.lit(x) for x in chain(*house_type_map.items())])

df = spark.range(100).select(
    n_map[(F.rand(seed=1) * 5).cast("int").cast("string")].alias("neighborhood"),
    h_map[(F.rand(seed=2) * 3).cast("int").cast("string")].alias("house_type"),
    F.when(F.rand(seed=3) > 0.15, (F.rand(seed=3) * 4 + 1).cast("int"))
    .otherwise(None)
    .alias("bedrooms"),
    F.when(F.rand(seed=4) > 0.10, (F.rand(seed=4) * 3 + 1).cast("int"))
    .otherwise(None)
    .alias("bathrooms"),
    F.when(F.rand(seed=5) > 0.12, (F.rand(seed=5) * 150 + 30).cast("float"))
    .otherwise(None)
    .alias("sqft"),
    (F.rand(seed=6) * 50).cast("int").alias("age_years"),
    (F.rand(seed=7) > 0.4).cast("int").alias("garage"),
    (F.rand(seed=8) * 300_000 + 80_000).cast("float").alias("price"),
)

df.show(6)

df.select(
    [F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]
).show()

imputer = Imputer(
    inputCols=["bedrooms", "bathrooms", "sqft"],
    outputCols=["bedrooms_imp", "bathrooms_imp", "sqft_imp"],
    strategy="median",
)

# imputer_model = imputer.fit(df)
# df_imputed = imputer_model.transform(df)

# df_imputed.select(
#     [
#         F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
#         for c in df_imputed.columns
#     ]
# ).show()

# SQLTransformer : Ajout de nouvelles features
# __THIS__ désigne le df en entrée
total_rooms = SQLTransformer(
    statement="SELECT *, (bedrooms_imp + bathrooms_imp) AS total_rooms FROM __THIS__"
)

# df_tr = total_rooms.transform(df_imputed)

# StringIndexer : Encodage catégoriel => numerique
# handleInvalid :
#   - skip => supprime la ligne
#   - error => lève une erreur
#   - keep => assigne un index spécial (nb_categories)
multi_idx = StringIndexer(
    inputCols=["neighborhood", "house_type"],
    outputCols=["neighborhood_idx", "house_type_idx"],
    handleInvalid="keep",
)

# model_multi = multi_idx.fit(df_tr)
# df_idx = model_multi.transform(df_tr)

# OneHotEncoder : index => vecteur binaire
ohe = OneHotEncoder(
    inputCol="house_type_idx",
    outputCol="house_type_ohe",
)

# ohe_model = ohe.fit(df_idx)
# df_ohe = ohe_model.transform(df_idx)

# df_ohe.select("house_type", "house_type_idx", "house_type_ohe").show()

# Bucketizer : Transforme une variable continue en classe
bucketizer = Bucketizer(
    splits=[0, 10, 30, 200], inputCol="age_years", outputCol="age_bucket"
)

# df_bucket = bucketizer.transform(df_ohe)

# VectorAssembler
# /!\ Ne pas mettre
assembler = VectorAssembler(
    inputCols=[
        "bedrooms_imp",
        "bathrooms_imp",
        "sqft_imp",
        "total_rooms",
        "age_bucket",
        "neighborhood_idx",
        "house_type_ohe",
        "garage",
    ],
    outputCol="features",
    handleInvalid="skip",
)

# df_assembled = assembler.transform(df_bucket)

# StandardScaler : Standardisation
std_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std",
)

# std_model = std_scaler.fit(df_assembled)
# df_std = std_model.transform(df_assembled)

# df_std.show()

train_df, test_df = df.randomSplit(weights=[0.8, 0.2], seed=42)

preprocessing = Pipeline(
    stages=[
        imputer,
        total_rooms,
        multi_idx,
        ohe,
        bucketizer,
        assembler,
        std_scaler,
    ]
)

# fir uniquement sur train
preprocessing_model = preprocessing.fit(train_df)

# transform sut train et test
train_prepared = preprocessing_model.transform(train_df)
test_prepared = preprocessing_model.transform(test_df)

# Sauvegarde de la pipeline
save_path = "/data/models/demo_house_pipeline"
preprocessing_model.write().overwrite().save(save_path)

# Chargement
preprocessing_reload = PipelineModel.load(save_path)
test_reload = preprocessing_reload.transform(test_df)

# Evaluateur Régression
evaluator = RegressionEvaluator(
    predictionCol="prediction",
    labelCol="price",
)

results = {}

# Régression linéaire
lr = LinearRegression(
    featuresCol="features_std",
    labelCol="price",
)

pipeline_lr = Pipeline(stages=preprocessing.getStages() + [lr])

# Entrainement du modèle
t0 = time.time()
model_lr = pipeline_lr.fit(train_df)
t1 = time.time()

# Prédiction
pred_lr = model_lr.transform(test_df)

# Métriques
rmse_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "rmse"})
r2_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "r2"})
mae_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "mae"})

results["LinearRegression"] = {"RMSE": rmse_lr, "R²": r2_lr, "MAE": mae_lr}

# RandomForestRegressor
rf = RandomForestRegressor(
    featuresCol="features_std",
    labelCol="price",
    seed=42,
)

pipeline_rf = Pipeline(stages=preprocessing.getStages() + [rf])

# Entrainement du modèle
t0 = time.time()
model_rf = pipeline_rf.fit(train_df)
t1 = time.time()

# Prédiction
pred_rf = model_rf.transform(test_df)

# Métriques
rmse_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "rmse"})
r2_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "r2"})
mae_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "mae"})

results["RandomForestRegressor"] = {"RMSE": rmse_rf, "R²": r2_rf, "MAE": mae_rf}

# Feature importance
rf_model = model_rf.stages[-1]  # Dernier stage qui est un RandomForestRegressionModel
importances = rf_model.featureImportances.toArray()
features_names = [
    "bedrooms_imp",
    "bathrooms_imp",
    "sqft_imp",
    "total_rooms",
    "age_bucket",
    "neighborhood_idx",
    "house_type_ohe",
    "garage",
]
fi_pairs = sorted(
    zip(features_names[: len(importances)], importances), key=lambda x: -x[1]
)

print(f"\n{'=' * 64}")
print("Feature importance:")
print(f"{'=' * 64}")
print(f"{'feature':<30} | {'importance':<10} | {'bar'}")
for fname, importance in fi_pairs:
    bar = "*" * int(importance * 100)
    print(f"{fname:<30} | {importance:<10.2f} | {bar}")

# GBTRegressor
gbt = GBTRegressor(
    featuresCol="features_std",
    labelCol="price",
    seed=42,
)

pipeline_gbt = Pipeline(stages=preprocessing.getStages() + [gbt])

# Entrainement du modèle
t0 = time.time()
model_gbt = pipeline_gbt.fit(train_df)
t1 = time.time()

# Prédiction
pred_gbt = model_gbt.transform(test_df)

# Métriques
rmse_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "rmse"})
r2_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "r2"})
mae_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "mae"})

results["GBTRegressor"] = {"RMSE": rmse_gbt, "R²": r2_gbt, "MAE": mae_gbt}

print(f"\n{'=' * 64}")
print("Metrics:")
print(f"{'=' * 64}")
print(f"{'Model':<30} | {'RMSE':<10} | {'R²':<10} | {'MAE':<10}")
for model, result in results.items():
    print(
        f"{model:<30} | {result['RMSE']:<10.2f} | {result['R²']:<10.2f} | {result['MAE']:<10.2f}"
    )

spark.stop()
