import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, IntegerType, StringType

# Session
builder: SparkSession.Builder = SparkSession.builder
spark = builder.master("local").appName("exo5").getOrCreate()

# Data
ventesData = [
    (
        "CMD001",
        "Alice Martin",
        "2024-03-15",
        "Électronique",
        1299.99,
        1,
        "Premium",
        "alice.martin@email.com",
    ),
    (
        "CMD002",
        "Bob Durand",
        "2024-03-16",
        "Vêtements",
        89.50,
        3,
        "Standard",
        "bob.durand@email.com",
    ),
    (
        "CMD003",
        "Claire Dubois",
        "2024-03-17",
        "Maison",
        45.00,
        2,
        "Premium",
        "claire.dubois@email.com",
    ),
    (
        "CMD004",
        "David Moreau",
        "2024-03-18",
        "Sport",
        199.99,
        1,
        "Standard",
        "david.moreau@email.com",
    ),
    (
        "CMD005",
        "Emma Petit",
        "2024-03-19",
        "Électronique",
        799.00,
        2,
        "VIP",
        "emma.petit@email.com",
    ),
    (
        "CMD006",
        "Frank Lambert",
        "2024-03-20",
        "Livres",
        29.99,
        5,
        "Standard",
        "frank.lambert@email.com",
    ),
    (
        "CMD007",
        "Grace Bernard",
        "2024-03-21",
        "Beauté",
        156.75,
        1,
        "Premium",
        "grace.bernard@email.com",
    ),
    (
        "CMD008",
        "Henri Rousseau",
        "2024-03-22",
        "Électronique",
        2199.00,
        1,
        "VIP",
        "henri.rousseau@email.com",
    ),
]

# DataFrame
df = spark.createDataFrame(
    ventesData,
    [
        "id_commande",
        "nom_client",
        "date_commande",
        "categorie",
        "prix_unitaire",
        "quantite",
        "statut_client",
        "email",
    ],
)

# Exercice 1 : Classification des ventes**

# Créez une UDF `classifierVente` qui :

# - Prend en paramètre le prix unitaire (Double)
# - Retourne une String avec les catégories :
#   - "Vente faible" si prix < 50€
#   - "Vente moyenne" si 50€ ≤ prix < 200€
#   - "Vente élevée" si 200€ ≤ prix < 1000€
#   - "Vente premium" si prix ≥ 1000€


def classifier_vente(prix_unitaire: float) -> str:
    if prix_unitaire >= 1000:
        return "Vente premium"
    if prix_unitaire >= 200:
        return "Vente élevée"
    if prix_unitaire >= 50:
        return "Vente moyenne"
    return "Vente faible"


classifierVente = F.udf(f=classifier_vente, returnType=StringType())

# ### **Exercice 2 : Calcul du montant total**

# Créez une UDF `calculerMontantTotal` qui :

# - Prend en paramètres le prix unitaire (Double) et la quantité (Int)
# - Applique une remise selon le statut client :
#   - Standard : aucune remise
#   - Premium : 5% de remise
#   - VIP : 10% de remise
# - Retourne le montant total après remise (Double)

REMISE_MAP = {"Standard": 0, "Premium": 0.05, "VIP": 0.1}


def calculer_montant_total(
    prix_unitaire: float, quantite: int, statut_client: str
) -> str:
    return round(
        quantite
        * prix_unitaire
        * (
            1 - (REMISE_MAP[statut_client] if statut_client in REMISE_MAP.keys() else 0)
        ),
        2,
    )


calculerMontantTotal = F.udf(f=calculer_montant_total, returnType=DoubleType())

# ### **Exercice 3 : Score de fidélité client**

# Créez une UDF `calculerScoreFidelite` qui :

# - Prend en paramètres : statut_client (String), montant_total (Double), categorie (String)
# - Calcule un score selon les règles :
#   - Score de base selon statut : Standard=1, Premium=2, VIP=3
#   - Bonus catégorie : Électronique=+2, Sport=+1, autres=+0
#   - Bonus montant : +1 point par tranche de 100€
# - Retourne le score total (Int)

BASE_SCORE_MAP = {"Standard": 1, "Premium": 2, "VIP": 3}
BONUS_MONTANT = 1
BONUS_CATEGORIE = {"Électronique": 2, "Sport": 1}


def calculer_score_fidelite(
    montant_total: float, categorie: str, statut_client: str
) -> int:
    return (
        (BASE_SCORE_MAP[statut_client] if statut_client in BASE_SCORE_MAP.keys() else 0)
        + int(montant_total // 100) * BONUS_MONTANT
        + (BONUS_CATEGORIE[categorie] if categorie in BONUS_CATEGORIE.keys() else 0)
    )


calculerScoreFidelite = F.udf(f=calculer_score_fidelite, returnType=IntegerType())

# DataFrame with UDF
dfWithUdf = (
    df.withColumn(
        colName="classification_vente", col=classifierVente(F.col("prix_unitaire"))
    )
    .withColumn(
        colName="montant_total",
        col=calculerMontantTotal(
            F.col("prix_unitaire"), F.col("quantite"), F.col("statut_client")
        ),
    )
    .withColumn(
        colName="score_fidélité",
        col=calculerScoreFidelite(
            F.col("montant_total"), F.col("categorie"), F.col("statut_client")
        ),
    )
)

dfWithUdf.show()
