#!/bin/bash

# Création des répertoires
mkdir data/
mkdir logs/
mkdir backups/
mkdir data/raw/
mkdir data/processed/
mkdir data/archives/
# Affichage de l'arborescence
tree

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