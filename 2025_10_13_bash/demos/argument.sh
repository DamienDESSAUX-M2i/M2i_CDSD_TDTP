#!/bin/bash

# variable pré-peuplée fournies par le Shell
echo "Le dossier actuel est : $PWD" # Répertoire du script
echo "L'utilisateur actuel est : $USER" # Nom d'utilisateur
echo "Le dossier personnel est : $HOME" # Emplacement du dosier personnel utilisateur actuel
echo "La commande d'entrée du script est : $0"
echo "Le premier argument du script est : $1" # $n pour le n-ieme
echo "Arguments d'entrée du script : $*" # ensemble des arguments sous forme d'une chaine de caractère
echo "Arguments d'entrée du script : $@" # ensemble des arguments
echo "Nombres arguments d'entrée du script : $#"
echo "Code de sortie de la dernière commande : $?"
echo "PID dernier processus effectué en arrière plan : $!"