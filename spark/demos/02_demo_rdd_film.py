from pyspark.sql import SparkSession

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("demo-rdd-film").getOrCreate()

# Récupérer le SparkContext
sc = spark.sparkContext

# Lecture du fichier film.data
rddFilm = sc.textFile(
    "C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/film.data"
)

# Récupération de la première ligne
firstline = rddFilm.first()

# Extraction de la valeur qui nous intéresse (3éme colonne)
rddNotes = rddFilm.map(lambda line: line.split("\t")[2])

# compte le nombre d'éléments par valeur
result = rddNotes.countByValue()

# Affichage du résultat
for key, value in result.items():
    print(f"{key} = {value}")
