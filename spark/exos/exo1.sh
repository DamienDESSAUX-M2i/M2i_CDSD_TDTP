# Créer un dossier logs à l’intérieur du système de fichier Hadoop.
hdfs dfs -mkdir /logs

# Afficher le contenu du dossier logs.
hdfs dfs -ls /logs

# Envoyer le dossier /logs dans le dossier logs du HDFS.
## powershell
docker cp C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/spark/data/access_log.txt 1375af43bddcb3c0c3b038ec9e9f04eb060a1c839bfce65b33a25a4602192fd8:/
hdfs dfs -put /access_log.txt /logs

# Afficher le contenu du ficher access_log.txt (Les 50 premières lignes).
head -n 50 acces_log.txt
hdfs dfs -cat /logs/access_log.txt | head -n 50

# Supprimer le ficher access_log.txt.
hdfs dfs -rm /logs/access_log.txt
rm /logs/access_log.txt