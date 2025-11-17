#!/bin/bash

age=0
read -p "Quelle âge avez-vous ? " age

if [[ $age -lt 0 ]] ; then
    echo "Votre âge doit être supérieur ou égal à 0"
elif [[ $age -lt 18 ]] ; then
    echo "Vous êtes mineur(e)"
else
    echo "Vous êtes majeur(e)"
fi