# ===
# docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /apps/demos/demo_transformers.py
# ===


from itertools import chain

import pyspark.sql.functions as F
from pyspark.ml import Pipeline, PipelineModel
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

pipeline = Pipeline(
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
pipeline_model = pipeline.fit(train_df)

# transform sut train et test
train_prepared = pipeline_model.transform(train_df)
test_prepared = pipeline_model.transform(test_df)

# Sauvegarde de la pipeline
save_path = "/data/models/demo_house_pipeline"
pipeline_model.write().overwrite().save(save_path)

# Chargement
pipeline_reload = PipelineModel.load(save_path)
test_reload = pipeline_reload.transform(test_df)

spark.stop()
