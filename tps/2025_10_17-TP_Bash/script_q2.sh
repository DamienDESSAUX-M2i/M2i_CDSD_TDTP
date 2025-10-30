#!/bin/bash

data_raw=./data/raw/data_raw.csv
data_processed=./data/processed/data_processed.csv
rapport=./data/processed/rapport.txt

# Supprimer les lignes vides
grep -vE "^[[:space:]]*$" $data_raw > $data_processed

echo
echo "=== Supprimer les lignes vides ==="
cat $data_processed

# Nombre de lignes dans data_raw.csv
nb_raw_lines=$(wc -l $data_raw)
nb_raw_lines=${nb_raw_lines%%[[:space:]]*}
# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}
# Nombre de lignes vides
nb_blank_lines=$(( nb_raw_lines - nb_processed_lines ))

# Supprimer les doublons
tmp="data/processed/tmp.csv"
cat $data_processed > $tmp

sort -u $tmp > $data_processed

echo
echo "=== Supprimer les doublons ==="
cat $data_processed

# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}
# Nombre de lignes vides
nb_doubloon_lines=$(( nb_raw_lines - nb_blank_lines - nb_processed_lines ))

# Expression régulière pour valider le format de nos données
validator="^[A-Za-z]+,[A-Za-z]+,[0-9]+"

# Pour éviter de lire et écrire dans le même fichier, on utilise le fichier tmp.csv
cat $data_processed > $tmp

# On supprime les lignes mal formatées
grep -E $validator $tmp > $data_processed

echo
echo "=== Supprimer les données mal formatées ==="
cat $data_processed

# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}

# Nombre de lignes mal formatées
nb_odd_lines=$(( nb_raw_lines - nb_blank_lines - nb_doubloon_lines - nb_processed_lines ))

# Ecriture du rapport
cat > $rapport << EOF
Nombre de lignes dans le fichier $data_raw : $nb_raw_lines.
Nombre de lignes dans le fichier $data_processed : $nb_processed_lines.
Nombre de lignes vides : $nb_blank_lines.
Nombre de lignes en doublons : $nb_doubloon_lines
Nombre de lignes mal formatées : $nb_odd_lines
EOF