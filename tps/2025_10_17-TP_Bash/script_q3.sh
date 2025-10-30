#!/bin/bash

# Répertoire
rep=$1

# Récupération de la date
## l'argument '+%F_%T' affiche la date et l'heure de la manière suivante : 2025-10-17_10:45:35
today=$(date '+%F_%T')
## remplace le caractère ':' par '-'
today="${today//:/-}"
# Création du backup
tar czf "./backups/backup_${today}.gz" "${rep}"

# On parcours les fichier du repertoire 'rep'
for file in $(ls $rep)
do
    # Archivage des fichiers invalides
    ## On récupère l'extension du fichier 'file'
    file_extension=${file##*.}
    ## On archive les fichier dont l'extension n'est pas 'csv'
    if [[ "$file_extension" != "csv" ]] ; then
        mv "${rep}/${file}" ./data/archives/

    # Traitement des données
    else
        # chemin fichier csv de départ
        data_raw=$(realpath file)
        # On récupére le nom du fichier 'file' pour créer le nom du fichier arpès traitement
        file_name=${file%%.*}
        # chemin fichier csv aprés traitement
        data_processed="./data/processed/${file_name}_processed.csv"
        # chemin du rapport
        rapport="./logs/${file_name}_rapport_${today}.txt"

        # Supprimer les lignes vides
        grep -vE "^[[:space:]]*$" $data_raw > $data_processed

        # Nombre de lignes dans data_raw.csv
        nb_raw_lines=$(wc -l $data_raw)
        nb_raw_lines=${nb_raw_lines%%[[:space:]]*}
        # Nombre de lignes dans data_processed.csv
        nb_processed_lines=$(wc -l $data_processed)
        nb_processed_lines=${nb_processed_lines%%[[:space:]]*}
        # Nombre de lignes vides
        nb_blank_lines=$(( nb_raw_lines - nb_processed_lines ))

        # Fichier temporaire pour éviter de lire et d'écrire en même temps
        tmp="data/processed/tmp.csv"
        cat $data_processed > $tmp
        # Supprimer les doublons
        sort -u $tmp > $data_processed

        # Nombre de lignes dans data_processed.csv
        nb_processed_lines=$(wc -l $data_processed)
        nb_processed_lines=${nb_processed_lines%%[[:space:]]*}
        # Nombre de lignes vides
        nb_doubloon_lines=$(( nb_raw_lines - nb_blank_lines - nb_processed_lines ))

        # Expression régulière pour valider le format de nos données
        ## '^[A-Za-z]+,' : la première colonne est constitué de caractère alphabétiques
        ## '[A-Za-z]+,' : la deuxième colonne est constituée de caractères alphabétiques
        ## '[0-9]+[\r\n|\r|\n]$' : la troisième colonne est constituée de caractères numériques et se termine par un retour chariot
        validator="^[A-Za-z]+,[A-Za-z]+,[0-9]+[\r\n|\r|\n]$"
        # Pour éviter de lire et écrire dans le même fichier, on utilise le fichier tmp.csv
        cat $data_processed > $tmp
        # On supprime les lignes mal formatées
        grep -E $validator $tmp > $data_processed

        # Nombre de lignes dans data_processed.csv
        nb_processed_lines=$(wc -l $data_processed)
        nb_processed_lines=${nb_processed_lines%%[[:space:]]*}
        # Nombre de lignes mal formatées
        nb_odd_lines=$(( nb_raw_lines - nb_blank_lines - nb_doubloon_lines - nb_processed_lines ))

        # Ecriture du rapport
        echo "=== Rapport ===" > $rapport
        echo "" >> $rapport
        echo "Nombre de lignes dans le fichier $data_raw : $nb_raw_lines." >> $rapport
        echo "Nombre de lignes dans le fichier $data_processed : $nb_processed_lines." >> $rapport
        echo "Nombre de lignes vides : $nb_blank_lines." >> $rapport
        echo "Nombre de lignes en doublons : $nb_doubloon_lines." >> $rapport
        echo "Nombre de lignes mal formatées : $nb_odd_lines." >> $rapport

        # Suppression du fichier temporaire
        rm $tmp

        # Permissions des fichiers 'data_raw', 'data_processed' et 'rapport'
        chmod 660 $data_raw
        chmod 660 $data_processed
        chmod 770 $rapport
    fi
done