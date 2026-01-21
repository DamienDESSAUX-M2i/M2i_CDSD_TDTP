from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, broadcast, col, count, desc, sum

# Créer la session Spark
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("exercise-broadcast-join").getOrCreate()

# Données des ventes
salesDF = spark.createDataFrame(
    [
        (1, "2025-01-15", 101, 1, 2, 99.99),
        (2, "2025-01-15", 102, 2, 1, 149.50),
        (3, "2025-01-16", 103, 1, 3, 29.99),
        (4, "2025-01-16", 101, 3, 1, 199.00),
        (5, "2025-01-17", 104, 2, 2, 79.99),
        (6, "2025-01-17", 102, 4, 1, 299.00),
        (7, "2025-01-18", 105, 1, 4, 49.99),
        (8, "2025-01-18", 103, 3, 2, 89.50),
    ],
    ["sale_id", "sale_date", "customer_id", "product_id", "quantity", "unit_price"],
)

# Table de référence des produits
productsDF = spark.createDataFrame(
    [
        (1, "Laptop Dell XPS", "Electronics", "US"),
        (2, "iPhone 15", "Electronics", "US"),
        (3, "Chaise Bureau", "Furniture", "FR"),
        (4, "Table Bois", "Furniture", "DE"),
    ],
    ["product_id", "product_name", "category", "origin_country"],
)

# Table de référence des clients
customersDF = spark.createDataFrame(
    [
        (101, "Alice Martin", "FR", "Premium"),
        (102, "Bob Smith", "US", "Standard"),
        (103, "Charlie Dubois", "FR", "Premium"),
        (104, "Diana Wagner", "DE", "Standard"),
        (105, "Erik Larsen", "NO", "Premium"),
    ],
    ["customer_id", "customer_name", "country", "membership"],
)

# Table de taux de conversion
exchangeRatesDF = spark.createDataFrame(
    [("US", 1.0), ("FR", 0.92), ("DE", 0.92), ("NO", 0.10)], ["country", "usd_rate"]
)

print("=== DONNÉES INITIALES ===\n")
print("Ventes :")
salesDF.show()
print("Produits :")
productsDF.show()
print("Clients :")
customersDF.show()
print("Taux de change :")
exchangeRatesDF.show()

# ========================================
# VOTRE CODE ICI
# ========================================

# TODO 1: Joindre les ventes avec les produits (utilisez broadcast!)
# Colonnes attendues : toutes les colonnes de sales + product_name, category, origin_country
productsDF_broadcast = broadcast(productsDF)

salesProductsDF = salesDF.join(
    other=productsDF_broadcast,
    on="product_id",
    how="inner",
)

# TODO 2: Ajouter les informations clients (utilisez broadcast!)
# Colonnes attendues : colonnes précédentes + customer_name, country (du client), membership
customersDF_broadcast = broadcast(customersDF)

salesProductsCustomersDF = salesProductsDF.join(
    other=customersDF_broadcast,
    on="customer_id",
    how="inner",
)

# TODO 3: Calculer le montant total de chaque vente (quantity * unit_price)
# Nouvelle colonne : total_amount
salesProductsCustomersDF = salesProductsCustomersDF.withColumn(
    colName="total_amount",
    col=col("quantity") * col("unit_price"),
)

# TODO 4: Convertir les montants en USD selon le pays du client
# Utilisez les taux de change avec broadcast
# Nouvelle colonne : total_amount_usd
exchangeRatesDF_broadcast = broadcast(exchangeRatesDF)

salesProductsCustomersExchangeRatesDF = salesProductsCustomersDF.join(
    other=exchangeRatesDF_broadcast,
    on="country",
    how="inner",
)

salesProductsCustomersExchangeRatesDF = (
    salesProductsCustomersExchangeRatesDF.withColumn(
        colName="total_amount_usd",
        col=col("total_amount") * col("usd_rate"),
    )
)

# TODO 5: Calculer des statistiques par catégorie de produit
# Afficher : category, nombre de ventes, montant total USD, montant moyen USD
salesProductsCustomersExchangeRatesDF.groupBy("category").agg(
    count("sale_id").alias("count_sales"),
    sum("total_amount_usd").alias("usd_total"),
    avg("total_amount_usd").alias("avg_total_amount_usd"),
).show()

# TODO 6: Identifier les clients Premium qui ont acheté des Electronics
# Afficher : customer_name, product_name, total_amount_usd
salesProductsCustomersExchangeRatesDF.filter(
    (col("category") == "Electronics") & (col("membership") == "Premium")
).select(["customer_name", "product_name", "total_amount_usd"]).orderBy(
    col("total_amount_usd").desc()
).show()
