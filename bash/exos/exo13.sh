#!/bin/bash

# Méthode 1 peu explicite
# echo "$1" >> $2

# Méthode 2 plus explicite
mot=$1
fichier=$2
echo "$mot" >> $fichier