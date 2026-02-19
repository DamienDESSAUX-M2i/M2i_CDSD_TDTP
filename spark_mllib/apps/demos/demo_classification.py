import time

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
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import sum as spark_sum

spark = (
    SparkSession.builder.appName("demo_regression")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = spark.read.csv("/data/titanic.csv", header=True, inferSchema=True)

df.show()

df.select(
    [spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]
).show()

df = df.select(
    col("Pclass").cast("int"),
    col("Sex"),
    col("Age").cast("int"),
    col("Parch").cast("int"),
    col("Fare").cast("float"),
    col("Embarked"),
    col("Survived"),
    col("SibSp").cast("int"),
)

# preprocessing
imputer = Imputer(inputCols=["Age"], outputCols=["Age_imp"], strategy="median")

indexer = StringIndexer(
    inputCols=["Sex", "Embarked"],
    outputCols=["Sex_idx", "Embarked_idx"],
    handleInvalid="keep",
)

ohe = OneHotEncoder(
    inputCols=["Sex_idx", "Embarked_idx"],
    outputCols=["Sex_ohe", "Embarked_ohe"],
    dropLast=True,
)

assembler = VectorAssembler(
    inputCols=[
        "Pclass",
        "Sex_ohe",
        "Age_imp",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked_ohe",
    ],
    outputCol="features",
    handleInvalid="skip",
)

scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std",
)

preprocessing = Pipeline(stages=[imputer, indexer, ohe, assembler, scaler])

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

pipeline_model = preprocessing.fit(train_df)
train_prepared = pipeline_model.transform(train_df)
test_prepared = pipeline_model.transform(test_df)

evaluator_f1 = MulticlassClassificationEvaluator(
    labelCol="Survived", predictionCol="prediction", metricName="f1"
)
evaluator_acc = MulticlassClassificationEvaluator(
    labelCol="Survived", predictionCol="prediction", metricName="accuracy"
)
evaluator_recall = MulticlassClassificationEvaluator(
    labelCol="Survived", predictionCol="prediction", metricName="weightedRecall"
)
evaluator_precision = MulticlassClassificationEvaluator(
    labelCol="Survived", predictionCol="prediction", metricName="weightedPrecision"
)
results = {}

# lr
lr = LogisticRegression(featuresCol="features_std", labelCol="Survived")

pipeline_lr = Pipeline(stages=preprocessing.getStages() + [lr])
t0 = time.time()
model_lr = pipeline_lr.fit(train_df)
time_lr = time.time() - t0

pred_lr = model_lr.transform(test_df)

f1_lr = evaluator_f1.evaluate(pred_lr)
acc_lr = evaluator_acc.evaluate(pred_lr)
prec_lr = evaluator_precision.evaluate(pred_lr)
recall_lr = evaluator_recall.evaluate(pred_lr)
results["LogisticRegression"] = {
    "f1": f1_lr,
    "accuracy": acc_lr,
    "precision": prec_lr,
    "recall": recall_lr,
    "temps": time_lr,
}

print(
    f"f1 : {f1_lr}, accuracy: {acc_lr}, precision: {prec_lr},recall : {recall_lr} , temps: {time_lr}"
)

# Matrice de confusion
pred_lr.groupBy("Survived", "prediction").count().orderBy(
    "Survived", "prediction"
).show()

# lr
rf = RandomForestClassifier(featuresCol="features_std", labelCol="Survived", seed=42)

pipeline_rf = Pipeline(stages=preprocessing.getStages() + [rf])
t0 = time.time()
model_rf = pipeline_rf.fit(train_df)
time_rf = time.time() - t0

pred_rf = model_rf.transform(test_df)

f1_rf = evaluator_f1.evaluate(pred_rf)
acc_rf = evaluator_acc.evaluate(pred_rf)
prec_rf = evaluator_precision.evaluate(pred_rf)
recall_rf = evaluator_recall.evaluate(pred_rf)
results["RandomForest"] = {
    "f1": f1_rf,
    "accuracy": acc_rf,
    "precision": prec_rf,
    "recall": recall_rf,
    "temps": time_rf,
}

print(
    f"f1 : {f1_rf}, accuracy: {acc_rf}, precision: {prec_rf},recall : {recall_rf} , temps: {time_rf}"
)

gbt = GBTClassifier(featuresCol="features_std", labelCol="Survived", seed=42)

pipeline_gbt = Pipeline(stages=preprocessing.getStages() + [gbt])
t0 = time.time()
model_gbt = pipeline_gbt.fit(train_df)
time_gbt = time.time() - t0

pred_gbt = model_gbt.transform(test_df)

f1_gbt = evaluator_f1.evaluate(pred_gbt)
acc_gbt = evaluator_acc.evaluate(pred_gbt)
prec_gbt = evaluator_precision.evaluate(pred_gbt)
recall_gbt = evaluator_recall.evaluate(pred_gbt)
results["GBTClassifier"] = {
    "f1": f1_gbt,
    "accuracy": acc_gbt,
    "precision": prec_gbt,
    "recall": recall_gbt,
    "temps": time_gbt,
}

print(
    f"f1 : {f1_gbt}, accuracy: {acc_gbt}, precision: {prec_gbt},recall : {recall_gbt} , temps: {time_gbt}"
)
