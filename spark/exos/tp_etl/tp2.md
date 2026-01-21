# EXERCICE PYSPARK - Nettoyage de Logs avec Regex

## Données fournies

Vous disposez de 5 lignes de logs au format suivant :

```
2024-01-15 10:23:45 [INFO] User: jean.dupont@company.fr logged in from IP: 192.168.1.100
2024-01-15 11:45:12 [ERROR] User: marie_martin@gmail.com failed login from IP: 10.0.0.25
2024-01-15 14:30:00 [INFO] User: pierre.durant@yahoo.fr logged in from IP: 172.16.0.5
2024-01-15 15:22:33 [WARNING] User: sophie@invalid-email logged in from IP: 192.168.2.200
2024-01-15 16:10:05 [INFO] User: luc.moreau@outlook.com logged in from IP: 8.8.8.8
```

## Tâches à réaliser

### EXERCICE 1 : Extraction de la date et heure

Extraire le timestamp au format `YYYY-MM-DD HH:MM:SS`

- **Colonne à créer** : `timestamp`
- **Exemple résultat** : `2024-01-15 10:23:45`

### EXERCICE 2 : Extraction du niveau de log

Extraire le niveau entre crochets (INFO, ERROR, WARNING)

- **Colonne à créer** : `niveau`
- **Exemple résultat** : `INFO`

### EXERCICE 3 : Extraction de l'email complet

Extraire l'adresse email complète après "User: "

- **Colonne à créer** : `email`
- **Exemple résultat** : `jean.dupont@company.fr`

### EXERCICE 4 : Extraction du nom d'utilisateur

Extraire uniquement la partie avant le @ de l'email

- **Colonne à créer** : `username`
- **Exemple résultat** : `jean.dupont`

### EXERCICE 5 : Extraction du domaine

Extraire uniquement la partie après le @ de l'email

- **Colonne à créer** : `domaine`
- **Exemple résultat** : `company.fr`

### EXERCICE 6 : Extraction de l'adresse IP

Extraire l'adresse IP après "IP: "

- **Colonne à créer** : `ip_address`
- **Exemple résultat** : `192.168.1.100`

### EXERCICE 7 : Extraction de l'action

Extraire le type d'action (logged in ou failed login)

- **Colonne à créer** : `action`
- **Exemple résultat** : `logged in`

### EXERCICE 8 : Validation de l'email

Vérifier si l'email est valide (format correct)

- **Colonne à créer** : `email_valide`
- **Résultat** : `OUI` ou `NON`

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract, when
from pyspark.sql.types import StructType, StructField, StringType

spark = SparkSession.builder \
    .appName("Exercice_Regex_Logs") \
    .master("local[*]") \
    .getOrCreate()

# Données de logs
logs_data = [
    ("2024-01-15 10:23:45 [INFO] User: jean.dupont@company.fr logged in from IP: 192.168.1.100"),
    ("2024-01-15 11:45:12 [ERROR] User: marie_martin@gmail.com failed login from IP: 10.0.0.25"),
    ("2024-01-15 14:30:00 [INFO] User: pierre.durant@yahoo.fr logged in from IP: 172.16.0.5"),
    ("2024-01-15 15:22:33 [WARNING] User: sophie@invalid-email logged in from IP: 192.168.2.200"),
    ("2024-01-15 16:10:05 [INFO] User: luc.moreau@outlook.com logged in from IP: 8.8.8.8"),
]

schema = StructType([StructField("log_message", StringType(), True)])
df_logs = spark.createDataFrame([(log,) for log in logs_data], schema)



# Afficher le résultat
df.show(truncate=False)

spark.stop()
```
