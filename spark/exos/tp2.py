import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("tp1").getOrCreate()
sc = spark.sparkContext

# ===
# Partie 1 : Chargement et exploration
# ===

# 1. Charger le CSV en DataFrame avec l'option header
df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")
    .option("escape", '"')  # Important : Pour la gestion des doubles guillemets
    .csv(
        "C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/SampleSuperstore.csv"
    )
)

# 2. Afficher le schéma du DataFrame
print("Schema:")
print(df.schema)

# 3. Afficher les 20 premières lignes
print("DataFrame sample_df:")
df.show(20)

# 4. Compter le nombre total de lignes
print(f"Number of lines: {df.count()}")

# 5. Afficher les régions uniques (colonne `Region`)
print("Distinct region:")
df.select(df["Region"]).distinct().show()


# ===
# Partie 2 : Transformations simples
# ===

# 1. Créer une colonne `Profit Margin` = `Profit` / `Sales`
# 2. Créer une colonne `Year` en extrayant l'année de `Order Date`
# 3. Créer une colonne `Total Value` = `Sales` - `Discount`
df_enriched_1 = (
    df.withColumn("Profit Margin", (df["Profit"] / df["Sales"]))
    .withColumn("Year", F.year(F.to_date(col=df["Order Date"], format="M/d/yyyy")))
    .withColumn("Total Value", (df["Sales"] - df["Discount"]))
)

# 4. Afficher les 10 premières lignes avec ces nouvelles colonnes
print("DataFrame enriched (Profit Margin, Year, Total Value):")
df_enriched_1["Profit Margin", "Year", "Total Value"].show(10)

# 5. **Mettre ce DataFrame en cache** (vous allez le réutiliser plusieurs fois)
df_enriched_1.cache()

# ===
# Partie 3 : UDF - Catégorisation des ventes
# ===


# 1. Créer une UDF `categorizeSale` qui prend le montant `Sales` et retourne :
#    - "Petite vente" si < 100$
#    - "Vente moyenne" si entre 100$ et 500$
#    - "Grosse vente" si > 500$
def categorize_sale(sales: float) -> str:
    try:
        if sales > 500:
            return "Grosse vente"
        if sales >= 100:
            return "Vente moyenne"
        return "Petite vente"
    except Exception:
        return None


categorizeSale = F.udf(categorize_sale, StringType())

# 2. Appliquer cette UDF pour créer une colonne `Sale Category`
df_enriched_2 = df_enriched_1.withColumn(
    "Sales", F.col("Sales").cast(DoubleType())
).withColumn("Sale Category", categorizeSale(F.col("Sales")))

# 3. Afficher quelques lignes avec cette nouvelle colonne
print("DataFrame enriched (Sale Category):")
df_enriched_2.show(5)

# 4. Compter le nombre de ventes par catégorie (Petite/Moyenne/Grosse)
print("Number of sales by category:")
df_enriched_2.groupBy("Sale Category").agg(
    F.count("Sale Category").alias("Number of Sales")
).show()

# ===
# Partie 4 : UDF - Niveau de remise
# ===


# 1. Créer une UDF `discountLevel` qui prend `Discount` et retourne :
#    - "Pas de remise" si = 0
#    - "Remise faible" si entre 0 et 0.2
#    - "Remise forte" si > 0.2
def discount_level(discount: float) -> str:
    try:
        if discount > 0.2:
            return "Remise forte"
        if discount > 0:
            return "Remise faible"
        return "Pas de remise"
    except Exception:
        return None


discountLevel = F.udf(discount_level, StringType())

# 2. Appliquer cette UDF pour créer une colonne `Discount Level`
df_enriched_3 = df_enriched_2.withColumn(
    "Discount", F.col("Discount").cast(DoubleType())
).withColumn("Discount Level", discountLevel(F.col("Discount")))

# 3. Calculer le CA total par niveau de remise
print("CA by discount level:")
df_enriched_3.groupBy("Discount Level").agg(F.sum("Sales").alias("CA")).show()

# ===
# Partie 5 : Agrégations basiques
# ===

# 1. Calculer le CA total (`Sales`) par région
print("CA by region:")
df_enriched_3.groupBy("Region").agg(F.sum("Sales").alias("CA")).show()

# 2. Calculer le profit total par catégorie de produit (`Category`)
print("Total profit by product category:")
df_enriched_3.groupBy("Category").agg(F.sum("Profit").alias("Total Profit")).show()

# 3. Calculer le nombre de commandes par segment client (`Segment`)
print("Number of orders by segment:")
df_enriched_3.groupBy("Segment").agg(F.count("Row ID").alias("Number of orders")).show()

# 4. Identifier les 10 produits (`Product Name`) les plus vendus en quantité
print("10 best-selling products:")
df_enriched_3.sort(F.col("Sales").desc()).limit(10).select(F.col("Product Name")).show()

# 5. Identifier les 5 états (`State`) avec le plus de CA
print("5 state with best CA:")
df_enriched_3.groupBy("State").agg(F.sum("Sales").alias("CA")).sort(
    F.col("CA").desc()
).limit(5).show()

# ===
# Partie 6 : Broadcast Variable - Codes région
# ===

# 1. Créer une Map qui associe chaque région à un code :
regionCodes = {"East": "EST", "West": "WST", "Central": "CTR", "South": "STH"}

# 2. Broadcaster cette Map avec `spark.sparkContext.broadcast()`
regionCodesBroadcast = sc.broadcast(regionCodes)


# 3. Créer une UDF qui utilise cette broadcast variable pour créer une colonne `Region Code`
def get_region_code(region: str) -> str:
    return (
        regionCodesBroadcast.value[region]
        if region in regionCodesBroadcast.value.keys()
        else None
    )


getRegionCode = F.udf(get_region_code, StringType())

df_enriched_4 = df_enriched_3.withColumn("Region Code", getRegionCode(F.col("Region")))

# 4. Afficher quelques lignes avec le code région
print("Enriched with Region Code:")
df_enriched_4.show(5)

# ===
# Partie 7 : Broadcast Variable - Coefficients de priorité
# ===

# 1. Créer une Map de coefficients par catégorie :
categoryPriority = {"Technology": 1.5, "Furniture": 1.2, "Office Supplies": 1.0}

# 2. Broadcaster cette Map
categoryPriorityBroadcast = sc.broadcast(categoryPriority)


# 3. Créer une UDF qui multiplie le `Profit` par le coefficient de sa catégorie pour créer une colonne `Weighted Profit`
def compute_weighted_profit(category: str, profit: float) -> float:
    weight = (
        categoryPriorityBroadcast.value[category]
        if category in categoryPriorityBroadcast.value.keys()
        else 1
    )
    return weight * profit


computeWeightedProfit = F.udf(compute_weighted_profit, DoubleType())

df_enriched_5 = df_enriched_4.withColumn(
    "Weighted Profit", computeWeightedProfit(F.col("Category"), F.col("Profit"))
)

# 4. Calculer le weighted profit total par catégorie
print("Enriched with Weight Profit")
df_enriched_5.show(5)
