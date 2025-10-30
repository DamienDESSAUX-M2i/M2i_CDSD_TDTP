# TP1

Dans la suite, je supose être administrateur. Sinon je dois utiliser la commande `sudo` et entrer le mot de passe pour obtenir les droit administrateur.

## Question 1

Pour créer un répertoire, on utilise la commande `mkdir`.
On crée les répertoires `\data`, `\logs` et `\backups`.
Dans le répertoire `\data`, on crée les répertoires `\raw`, `\processed` et `\archives`.
Pour visualiser l'arborescence on peut utiliser la commande `tree`.

```bash
# Création des répertoires
mkdir data/
mkdir logs/
mkdir backups/
mkdir data/raw/
mkdir data/processed/
mkdir data/archives/
# Affichage de l'arborescence
tree
```

La commande `chmod` permet de modifier les permissions. On utilise la commande `groupadd` pour créer des groupes et la commande `chgrp` pour changer le groupe propriétaire d'un fichier ou répertoire. Pour créer un utilisateur, on utilise la commande `useradd` puis pour ajouter un utilisateur à un groupe, on utilise la commande `usermod`. On peut afficher la liste des groupes d'un utilisateur avec la commande `groups`. La commande `chown` permet de modifier le propriétaire d'un groupe.
 
```bash
# On crée un groupe admin
groupadd admin
# On ajoute l'utilisateur 'damiendessaux' au groupe 'admin'
usermod -aG admin damiendessaux
# On change le groupe propriétaire des répertoires 'backups/' et 'logs'
chgrp -R admin ./backups
chgrp -R admin ./logs
# On change les permissions des répertoires '/backups/' et 'logs/' afin que seul l'administrateur puisse lire, écrire et exécuter
chmod -R 770 ./backups
chmod -R 770 ./logs
# Pour vérifier, on afficher les groupes de l'utilisateur 'damiendessaux' et les informations des répertoires 'logs/' et 'backups/'.
groups damiendessaux
ll
 
# On crée les groupes 'data_users' et 'data_viewers'
groupadd data_users
groupadd data_viewers
# On change le groupe propriétaire de data/
chgrp -R data_users ./data
# On change les permissions du groupe 'data_users'
## les membre de ce groupe pourront lire et écrire
## les autres groupes ne pourront que lire
chmod -R 660 ./data
# On crée deux utilisateurs 'data_user' et 'data_viewer' qu'on ajoute aux groupes 'data_users' et 'data_viewers' respectivement
useradd data_user --groups data_users
useradd data_viewer --groups data_viewers
# Pour vérifier, on affiche les groupes de 'data_users' et 'data_viewers' et les informations du répertoire 'data/'.
groups data_user
groups data_viewer
ll
```

## Question 2

On crée un fichier `data_raw.csv` avec quelques données dans un bloc de texte.

```bash
# Chemin du fichier data_raw.csv
data_raw="./data/raw/data_raw.csv"
cat > $data_raw << EOF
nom,groupe,prix
lampe,objet,30

bureau,meuble,120
lampe,objet,50

bureau,meuble,120
chaise,meuble,cinquante
ord1n@teur,multimedia,600

ordinateur,05561,600
EOF
```

Pour supprimer les lignes vides on peut utiliser la commande `grep`.

```bash
# Cemin du fichier data_processed.csv
data_processed="./data/processed/data_processed.csv"
# On supprime les lignes vides ou ne contenant que des espaces
grep -vE "^[[:space:]]*$" $data_raw > $data_processed

echo
echo "=== Supprimer les lignes vides ==="
cat $data_processed
```

Pour l'écriture de notre rapport nous auront besoin du nombre de ligne vide. On compte le nombre de ligne dans les fichiers `data_raw.csv` et `data_processed.csv` et on les soustrait.

```bash
# Nombre de lignes dans data_raw.csv
nb_raw_lines=$(wc -l $data_raw)
nb_raw_lines=${nb_raw_lines%%[[:space:]]*}

# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}

# Nombre de lignes vides
nb_blank_lines=$(( nb_raw_lines - nb_processed_lines ))
```

Pour supprimer les doublons, on peut utiliser la commande `sort` avec l'argument `-u`.

```bash
# Pour éviter de lire et écrire dans le même fichier, on crée un fichier tmp contenant les données du fichier data_processed
tmp="./data/processed/tmp.csv"
cat $data_processed > $tmp

# On supprime les lignes vides ou ne contenant que des espaces
sort -u $tmp > $data_processed

echo
echo "=== Supprimer les doublons ==="
cat $data_processed
```

Pour l'écriture de notre rapport nous auront besoin du nombre de ligne en boublon. On compte le nombre de ligne dans le fichier `data_processed.csv` et on calcule le nombre de ligne en doublon.

```bash
# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}

# Nombre de lignes vides
nb_doubloon_lines=$(( nb_raw_lines - nb_blank_lines - nb_processed_lines ))
```

Pour supprimer les lignes n'ayant pas le bon formation, on peut utiliser la commande `grep` avec une expression régulière donnant le format de chaque ligne.

```bash
# Expression régulière pour valider le format de nos données
validator="^[A-Za-z]+,[A-Za-z]+,[0-9]+"

# Pour éviter de lire et écrire dans le même fichier, on utilise le fichier tmp.csv
cat $data_processed > $tmp

# On supprime les lignes mal formatées
grep -E "$validator" $tmp > $data_processed

echo
echo "=== Supprimer les données mal formatées ==="
cat $data_processed
```

Pour l'écriture de notre rapport nous auront besoin du nombre de ligne mal formattées. On compte le nombre de ligne dans le fichier `data_processed.csv` et on calcule le nombre de ligne mal formattées.

```bash
# Nombre de lignes dans data_processed.csv
nb_processed_lines=$(wc -l $data_processed)
nb_processed_lines=${nb_processed_lines%%[[:space:]]*}

# Nombre de lignes mal formatées
nb_odd_lines=$(( nb_raw_lines - nb_blank_lines - nb_doubloon - nb_processed_lines ))
```

On écrit le rapport dans un fichier rapport.txt.

```bash
# Ecriture du rapport
rapport=./data/processed/rapport.txt

cat > $rapport << EOF
Nombre de lignes dans le fichier $data_raw : $nb_raw_lines.
Nombre de lignes dans le fichier $data_processed : $nb_processed_lines.
Nombre de lignes vides : $nb_blank_lines.
Nombre de lignes en doublons : $nb_doubloon_lines.
Nombre de lignes mal formatées : $nb_odd_lines.
EOF
```

## Question 3

Script réalisant les traitements demandés :

```bash
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
```