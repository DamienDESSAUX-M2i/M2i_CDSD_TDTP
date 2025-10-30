#!/bin/bash

nom=dessaux
nom=${nom^}
prenom=damien
prenom=${prenom^}

echo "Mes initales sont ${nom:0:1}.${prenom:0:1}"