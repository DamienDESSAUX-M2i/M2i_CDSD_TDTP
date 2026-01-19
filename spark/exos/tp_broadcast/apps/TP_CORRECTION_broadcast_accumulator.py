"""
================================================================================
TP SPARK - BROADCAST & ACCUMULATOR - CORRECTION
================================================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, sum as spark_sum, avg, count, when, lit
from pyspark.sql.types import StringType, FloatType, StructType, StructField, IntegerType
from pyspark.accumulators import AccumulatorParam
import time

# =============================================================
# INITIALISATION SPARK
# =============================================================

spark = SparkSession.builder \
    .appName("TP_Broadcast_Accumulator_Correction") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext

print("=" * 70)
print("TP SPARK - BROADCAST & ACCUMULATOR - CORRECTION")
print("=" * 70)

# =============================================================
# EXERCICE 1 : CHARGEMENT DES DONNÉES
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 1 : CHARGEMENT DES DONNÉES")
print("=" * 70)

# 1.1 Charger les fichiers CSV
df_clients = spark.read.csv("/data/clients.csv", header=True, inferSchema=True)
df_achats = spark.read.csv("/data/achats.csv", header=True, inferSchema=False)
# inferSchema=False pour achats car on veut gérer les erreurs nous-mêmes

# 1.2 Afficher le schéma
print("\n Schéma clients :")
df_clients.printSchema()

print("\n Schéma achats :")
df_achats.printSchema()

# 1.3 Compter les lignes
print(f"\n Nombre de clients : {df_clients.count()}")
print(f" Nombre d'achats : {df_achats.count()}")

# Aperçu des données
print("\n Aperçu clients :")
df_clients.select("client_id", "nom", "prenom", "country", "segment").show(5)

print("\n Aperçu achats :")
df_achats.show(5)


# =============================================================
# EXERCICE 2 : BROADCAST - TABLE TVA
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 2 : BROADCAST - TABLE TVA")
print("=" * 70)

# 2.1 Créer le dictionnaire des taux de TVA
taux_tva = {
    "France": 20.0,
    "Belgique": 21.0,
    "Suisse": 7.7,
    "Luxembourg": 17.0,
    "Canada": 5.0,
    "Maroc": 20.0
}
print(f"\n Table des taux de TVA : {taux_tva}")

# 2.2 Broadcaster le dictionnaire
broadcast_tva = sc.broadcast(taux_tva)
# broadcast() : envoie la variable à tous les workers une seule fois
# Les workers y accèdent via broadcast_tva.value

print(f" Dictionnaire TVA broadcasté vers les workers")

# 2.3 Créer une UDF qui utilise la broadcast variable
def get_taux_tva(pays):
    """
    Récupère le taux de TVA depuis la broadcast variable.
    Retourne 0 si le pays n'est pas trouvé.
    """
    return broadcast_tva.value.get(pays, 0.0)

# Enregistrer l'UDF
get_taux_tva_udf = udf(get_taux_tva, FloatType())

# 2.4 Ajouter la colonne taux_tva
df_clients_tva = df_clients.withColumn("taux_tva", get_taux_tva_udf(col("country")))

# 2.5 Afficher les résultats
print("\n Clients avec taux de TVA :")
df_clients_tva.select("client_id", "nom", "prenom", "country", "taux_tva").show(10)

# Vérifier la répartition par pays
print("\n Répartition par pays et taux TVA :")
df_clients_tva.groupBy("country", "taux_tva").count().orderBy("country").show()


# =============================================================
# EXERCICE 3 : BROADCAST - JOINTURE OPTIMISÉE
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 3 : BROADCAST - JOINTURE OPTIMISÉE")
print("=" * 70)

# 3.1 Créer le dictionnaire clients
# ATTENTION : Correspondance entre "C001" (achats) et 1 (clients)

# Collecter les données clients dans un dictionnaire
clients_data = df_clients.select("client_id", "nom", "prenom", "segment").collect()

# Créer le dictionnaire avec la clé au format "C001", "C002", etc.
dict_clients = {}
for row in clients_data:
    # Convertir 1 → "C001", 2 → "C002", etc.
    key = f"C{row['client_id']:03d}"
    dict_clients[key] = (row['nom'], row['prenom'], row['segment'])

print(f"\n Exemple de mapping :")
for i, (k, v) in enumerate(list(dict_clients.items())[:5]):
    print(f"   {k} → {v}")

# 3.2 Broadcaster le dictionnaire
broadcast_clients = sc.broadcast(dict_clients)
print(f"\n Dictionnaire clients broadcasté ({len(dict_clients)} entrées)")

# 3.3 Enrichir les achats avec broadcast
def enrichir_achat_nom(id_client):
    """Récupère le nom du client"""
    info = broadcast_clients.value.get(id_client)
    return info[0] if info else "INCONNU"

def enrichir_achat_prenom(id_client):
    """Récupère le prénom du client"""
    info = broadcast_clients.value.get(id_client)
    return info[1] if info else "INCONNU"

def enrichir_achat_segment(id_client):
    """Récupère le segment du client"""
    info = broadcast_clients.value.get(id_client)
    return info[2] if info else "INCONNU"

# Enregistrer les UDFs
udf_nom = udf(enrichir_achat_nom, StringType())
udf_prenom = udf(enrichir_achat_prenom, StringType())
udf_segment = udf(enrichir_achat_segment, StringType())

# Enrichir le DataFrame
df_achats_enrichi = df_achats \
    .withColumn("nom", udf_nom(col("id_client"))) \
    .withColumn("prenom", udf_prenom(col("id_client"))) \
    .withColumn("segment", udf_segment(col("id_client")))

print("\n Achats enrichis avec broadcast :")
df_achats_enrichi.show(10)

# 3.4 Comparer avec jointure classique
print("\n  Comparaison des performances :")

# Préparer les données pour la jointure classique
df_achats_prep = df_achats.withColumn(
    "client_id_int",
    when(col("id_client").rlike("^C[0-9]+$"),
         col("id_client").substr(2, 3).cast(IntegerType()))
    .otherwise(None)
)

# Méthode 1 : Jointure classique
start = time.time()
df_join_classique = df_achats_prep.join(
    df_clients.select("client_id", "nom", "prenom", "segment"),
    df_achats_prep["client_id_int"] == df_clients["client_id"],
    "left"
)
_ = df_join_classique.count()
temps_classique = time.time() - start
print(f"   Jointure classique : {temps_classique:.3f}s")

# Méthode 2 : Broadcast (déjà fait, on re-mesure)
start = time.time()
df_broadcast = df_achats \
    .withColumn("nom", udf_nom(col("id_client"))) \
    .withColumn("segment", udf_segment(col("id_client")))
_ = df_broadcast.count()
temps_broadcast = time.time() - start
print(f"   Avec broadcast     : {temps_broadcast:.3f}s")


# =============================================================
# EXERCICE 4 : ACCUMULATOR - COMPTAGE D'ERREURS
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 4 : ACCUMULATOR - COMPTAGE D'ERREURS")
print("=" * 70)

# 4.1 Créer les accumulators
montants_valides = sc.accumulator(0)
montants_invalides = sc.accumulator(0)
montants_negatifs = sc.accumulator(0)
montants_vides = sc.accumulator(0)
clients_inconnus = sc.accumulator(0)

print("\n Accumulators créés :")
print("   - montants_valides")
print("   - montants_invalides")
print("   - montants_negatifs")
print("   - montants_vides")
print("   - clients_inconnus")

# 4.2 Fonction de parsing avec accumulators
def parser_achat(id_client, id_article, montant_str):
    """
    Parse une ligne d'achat et incrémente les accumulators.
    Retourne (id_client, id_article, montant, nom, prenom, segment) ou None si invalide.
    """
    # Vérifier si le client existe
    client_info = broadcast_clients.value.get(id_client)
    if client_info is None:
        clients_inconnus.add(1)
        return None
    
    # Vérifier le montant
    if montant_str is None or montant_str.strip() == "":
        montants_vides.add(1)
        return None
    
    try:
        montant = float(montant_str)
        if montant < 0:
            montants_negatifs.add(1)
            return None
        montants_valides.add(1)
        return (id_client, id_article, montant, client_info[0], client_info[1], client_info[2])
    except ValueError:
        montants_invalides.add(1)
        return None

# 4.3 Appliquer la fonction avec RDD
print("\n Traitement des achats...")

# Convertir en RDD pour utiliser les accumulators facilement
rdd_achats = df_achats.rdd

# Appliquer le parsing (sauter l'en-tête si présent)
rdd_parsed = rdd_achats.map(lambda row: parser_achat(row['id_client'], row['id_article'], row['montant']))

# Filtrer les None et collecter
rdd_valides = rdd_parsed.filter(lambda x: x is not None)
achats_valides = rdd_valides.collect()

# Afficher les statistiques
print("\n STATISTIQUES DE QUALITÉ DES DONNÉES :")
print(f"    Montants valides   : {montants_valides.value}")
print(f"    Montants invalides : {montants_invalides.value}")
print(f"    Montants négatifs  : {montants_negatifs.value}")
print(f"    Montants vides     : {montants_vides.value}")
print(f"    Clients inconnus   : {clients_inconnus.value}")

total_erreurs = montants_invalides.value + montants_negatifs.value + montants_vides.value + clients_inconnus.value
total_lignes = montants_valides.value + total_erreurs
taux_erreur = (total_erreurs / total_lignes * 100) if total_lignes > 0 else 0

print(f"\n    Total lignes      : {total_lignes}")
print(f"    Taux d'erreur     : {taux_erreur:.1f}%")


# =============================================================
# EXERCICE 5 : ACCUMULATOR PERSONNALISÉ
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 5 : ACCUMULATOR PERSONNALISÉ")
print("=" * 70)

# 5.1 Créer un AccumulatorParam pour les listes
class ListAccumulatorParam(AccumulatorParam):
    """
    Accumulator personnalisé qui collecte des éléments dans une liste.
    """
    def zero(self, initialValue):
        """Valeur initiale : liste vide"""
        return []
    
    def addInPlace(self, v1, v2):
        """Fusionner deux listes (sans doublons)"""
        return list(set(v1 + v2))

# 5.2 Créer les accumulators de collecte
acc_clients_inconnus = sc.accumulator([], ListAccumulatorParam())
acc_montants_invalides = sc.accumulator([], ListAccumulatorParam())

print("\n Accumulators personnalisés créés")

# Réinitialiser les compteurs pour ce test
compteur_test = sc.accumulator(0)

def parser_avec_collecte(id_client, id_article, montant_str):
    """
    Parse et collecte les erreurs pour le rapport.
    """
    compteur_test.add(1)
    
    # Vérifier si le client existe
    client_info = broadcast_clients.value.get(id_client)
    if client_info is None:
        acc_clients_inconnus.add([id_client])
        return None
    
    # Vérifier le montant
    if montant_str is None or montant_str.strip() == "":
        acc_montants_invalides.add([f"VIDE (client {id_client})"])
        return None
    
    try:
        montant = float(montant_str)
        if montant < 0:
            acc_montants_invalides.add([f"{montant_str} (négatif, client {id_client})"])
            return None
        return (id_client, id_article, montant, client_info[2])
    except ValueError:
        acc_montants_invalides.add([f"'{montant_str}' (client {id_client})"])
        return None

# Appliquer
rdd_achats2 = df_achats.rdd
rdd_result = rdd_achats2.map(lambda row: parser_avec_collecte(row['id_client'], row['id_article'], row['montant']))
_ = rdd_result.filter(lambda x: x is not None).count()

# 5.3 Afficher le rapport d'erreurs
print("\n" + "=" * 50)
print(" RAPPORT D'ERREURS DÉTAILLÉ")
print("=" * 50)

print(f"\n🔍 Clients inconnus ({len(acc_clients_inconnus.value)}) :")
for client in sorted(acc_clients_inconnus.value):
    print(f"   - {client}")

print(f"\n🔍 Montants invalides ({len(acc_montants_invalides.value)}) :")
for montant in acc_montants_invalides.value:
    print(f"   - {montant}")


# =============================================================
# EXERCICE 6 : ANALYSE COMPLÈTE
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 6 : ANALYSE COMPLÈTE")
print("=" * 70)

# Réinitialiser les accumulators
acc_total_traite = sc.accumulator(0)
acc_total_valide = sc.accumulator(0)
acc_somme_ventes = sc.accumulator(0.0)
acc_erreurs = sc.accumulator(0)

def analyser_vente(id_client, id_article, montant_str):
    """
    Analyse complète avec métriques.
    """
    acc_total_traite.add(1)
    
    # Vérifier client
    client_info = broadcast_clients.value.get(id_client)
    if client_info is None:
        acc_erreurs.add(1)
        return None
    
    # Vérifier montant
    if montant_str is None or montant_str.strip() == "":
        acc_erreurs.add(1)
        return None
    
    try:
        montant = float(montant_str)
        if montant < 0:
            acc_erreurs.add(1)
            return None
        
        acc_total_valide.add(1)
        acc_somme_ventes.add(montant)
        return (client_info[2], montant)  # (segment, montant)
        
    except ValueError:
        acc_erreurs.add(1)
        return None

# 6.1 Calculer par segment
print("\n Analyse par segment de client...")

rdd_analyse = df_achats.rdd \
    .map(lambda row: analyser_vente(row['id_client'], row['id_article'], row['montant'])) \
    .filter(lambda x: x is not None)

# Agréger par segment
resultats_segment = rdd_analyse \
    .map(lambda x: (x[0], (x[1], 1))) \
    .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
    .collect()

# 6.2 & 6.3 Afficher les résultats
print("\n" + "=" * 50)
print(" RÉSULTATS PAR SEGMENT")
print("=" * 50)
print(f"{'Segment':<15} {'Nb Trans':<12} {'Total €':<15} {'Moyenne €':<12}")
print("-" * 50)

for segment, (total, nb) in sorted(resultats_segment):
    moyenne = total / nb if nb > 0 else 0
    print(f"{segment:<15} {nb:<12} {total:<15.2f} {moyenne:<12.2f}")

print("\n" + "=" * 50)
print(" MÉTRIQUES GLOBALES (via Accumulators)")
print("=" * 50)
print(f"   Transactions traitées : {acc_total_traite.value}")
print(f"   Transactions valides  : {acc_total_valide.value}")
print(f"   Transactions en erreur: {acc_erreurs.value}")
print(f"   Taux d'erreur         : {acc_erreurs.value / acc_total_traite.value * 100:.1f}%")
print(f"   Montant total ventes  : {acc_somme_ventes.value:.2f} €")
print(f"   Panier moyen          : {acc_somme_ventes.value / acc_total_valide.value:.2f} €")


# =============================================================
# EXERCICE 7 : COMPARAISON DE PERFORMANCE
# =============================================================
print("\n" + "=" * 70)
print("EXERCICE 7 : COMPARAISON DE PERFORMANCE")
print("=" * 70)

# Générer plus de données pour un test significatif
print("\n Génération de données volumineuses pour le test...")

# Multiplier les achats pour avoir plus de volume
achats_multiplies = []
for i in range(1000):
    for row in df_achats.collect():
        achats_multiplies.append((row['id_client'], row['id_article'], row['montant']))

rdd_gros = sc.parallelize(achats_multiplies)
print(f"   Nombre de lignes : {rdd_gros.count():,}")

# 7.1 SANS optimisation
print("\n SANS optimisation :")

start = time.time()

# Simuler plusieurs passes
# Pass 1 : Filtrer les montants valides
valides_1 = rdd_gros.filter(lambda x: x[2] is not None and x[2] != "")
count_1 = valides_1.count()

# Pass 2 : Filtrer les montants numériques
def is_numeric(x):
    try:
        float(x[2])
        return True
    except:
        return False

valides_2 = rdd_gros.filter(is_numeric)
count_2 = valides_2.count()

# Pass 3 : Compter les erreurs
erreurs = rdd_gros.filter(lambda x: not is_numeric(x)).count()

temps_sans_opti = time.time() - start
print(f"   Temps (3 passes) : {temps_sans_opti:.2f}s")
print(f"   Valides: {count_2}, Erreurs: {erreurs}")

# 7.2 AVEC optimisation
print("\n AVEC optimisation (Broadcast + Accumulator) :")

acc_v = sc.accumulator(0)
acc_e = sc.accumulator(0)

def traiter_optimise(row):
    id_client, id_article, montant_str = row
    
    if montant_str is None or montant_str.strip() == "":
        acc_e.add(1)
        return None
    
    try:
        montant = float(montant_str)
        if montant < 0:
            acc_e.add(1)
            return None
        
        client_info = broadcast_clients.value.get(id_client)
        if client_info is None:
            acc_e.add(1)
            return None
        
        acc_v.add(1)
        return (id_client, montant, client_info[2])
    except:
        acc_e.add(1)
        return None

start = time.time()

# 1 seule passe !
resultat = rdd_gros.map(traiter_optimise).filter(lambda x: x is not None).count()

temps_avec_opti = time.time() - start
print(f"   Temps (1 passe)  : {temps_avec_opti:.2f}s")
print(f"   Valides: {acc_v.value}, Erreurs: {acc_e.value}")

# 7.3 Comparaison
print("\n" + "=" * 50)
print(" COMPARAISON")
print("=" * 50)
print(f"   Sans optimisation : {temps_sans_opti:.2f}s")
print(f"   Avec optimisation : {temps_avec_opti:.2f}s")
if temps_sans_opti > temps_avec_opti:
    gain = (1 - temps_avec_opti / temps_sans_opti) * 100
    print(f"    Gain           : {gain:.1f}%")


# =============================================================
# BONUS : RÉPONSES AUX QUESTIONS
# =============================================================
print("\n" + "=" * 70)
print("BONUS : RÉPONSES AUX QUESTIONS")
print("=" * 70)

print("""
B.1 QUAND NE PAS UTILISER BROADCAST ?
    - Quand la donnée est trop volumineuse (> quelques centaines de Mo)
    - Quand la donnée change fréquemment
    - Quand les deux tables à joindre sont volumineuses
    → Dans ces cas, utiliser une jointure classique avec partitionnement

B.2 POURQUOI LES ACCUMULATORS NE SONT PAS FIABLES POUR LA LOGIQUE MÉTIER ?
    - En cas de re-exécution de tâches (échec puis retry), les valeurs
      peuvent être incrémentées plusieurs fois
    - Les accumulators sont mis à jour de manière asynchrone
    → Utiliser uniquement pour des métriques approximatives, debugging

B.3 DIFFÉRENCE ENTRE CACHE() ET BROADCAST() ?
    - cache() : stocke un RDD/DataFrame réparti sur les workers
                pour éviter de recalculer les transformations
    - broadcast() : envoie une variable ENTIÈRE à tous les workers
                    pour éviter de la transférer à chaque tâche
    → cache = optimiser les calculs répétés
    → broadcast = optimiser les jointures avec petites tables

B.4 ACCUMULATOR POUR OPÉRATIONS NON COMMUTATIVES ?
    - Par défaut, l'ordre d'agrégation n'est pas garanti
    - Pour des opérations ordonnées, collecter les données avec
      un identifiant/timestamp et trier après
    - Ou utiliser un accumulator de liste puis trier sur le driver
""")


# =============================================================
# NETTOYAGE
# =============================================================

# Libérer les broadcast variables
broadcast_tva.unpersist()
broadcast_clients.unpersist()

spark.stop()
print("\n TP terminé avec succès !")
