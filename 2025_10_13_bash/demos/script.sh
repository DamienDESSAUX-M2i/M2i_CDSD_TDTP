#!/bin/bash

# variable
firstname="john"
lastname="doe"
nb_a=12
nb_b=7

# expension de variable (syntaxe $var)
echo "Bonjour $firstname $lastname"
fullname="$firstname $lastname"

# Peupler une varible d'un retour de commande on utilise la substitution de commande ( $(commande) )
date=$(date '+%d-%m-%Y %H:%M')
echo "$date"

# Calcul nombres entiers relatifs
add=$((nb_a + nb_b))
echo "$nb_a + $nb_b = $add"

# Calcul nombre décimaux avec une partie décimale non nulle
# substitution + pipeline vers la commande bc
div=$(echo "scale=3; 5 / 2" | bc)
echo "5 / 2 = $div"

# Manipulation string
# ${text,} => Première lettre en minuscule
# ${text^} => Première lettre en majuscule
# ${text,,} => Tout en minuscule
# ${text^^} => Tout lettre en minuscule
firstname=${firstname^}
lastname=${lastname^^}
echo "Bonjour $firstname $lastname"

# Slice chaine de caractères
text="Une longue phrase."
echo "5 première lettres du texte : ${text:0:5}"
echo "3 lettres du texte à partir de la 2e lettre : ${text:1:3}"
echo "Toutes les lettres du texte à partir de la 5e lettre : ${text:4}"
echo "Les 5 dernières lettres du texte : ${text: -5: -2}"
echo "Longueur du texte : ${#text}"

# Remplacement
chaine1="toto toto toto"
chaine2="tata titi toto"
echo "${chaine1/toto/titi}" # remplacement 1er occurence
echo "${chaine1//toto/titi}" # remplacement toutes occurences
echo "${chaine1/#toto/titi}" # remplacement premier élément
echo "${chaine1/%toto/titi}" # remplacement dernier élément

adn="aattaca"
echo "${adn#*t}" # partant de gauche, dès la 1er occurence, tronque et retourne la partie à droite
echo "${adn##*t}" # partant de gauche, à la dernière occurence, tronque et retourne la partie à droite
echo "${adn%t*}" # partant de droite, dès la 1er occurence, tronque et retourne la partie à gauche
echo "${adn%%t*}" # partant de droite, à la dernière occurence, tronque et retourne la partie à gauche

path="/home/user/text.txt"
echo "Le nom du fichier est ${path##*/}"
echo "L'extension est ${path##*.}"
echo "le chemin du répertoire est ${path%/*}"

# Condition
# if then elif then else fi
read -p "veuilliez entrer une valeur : " ma_variable
if [[ ma_variable -gt 5 ]] ; then
    echo "$ma_variable est supérieure à 5"
elif [[ ma_variable -lt 5 ]] ; then
    echo "$ma_variable est inférieure à 5"
else
    echo "$ma_variable est égale à 5"
fi

if (( $ma_variable % 2 == 0 )) ; then
    echo "$ma_variable est un multiple de 2"
else
    echo "$ma_varible n'est pas un multiple de 2"
fi

# Switch case pour éviter l'accumulation de elif
case $ma_variable in
    1)
        echo "vous avec entré un 1"
        ;;
    2|3)
        echo "Vous avec entré un 2 ou un 3"
        ;;
    [4-9])
        echo "vous avez entré un nombre entre 4 et 9"
        ;;
    *)
        echo "Vous avez entré un nombre supérieur à 9"
        ;;
esac