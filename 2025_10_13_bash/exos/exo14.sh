#!/bin/bash


# $RANDOM => nombre random entre 0 et 32767
borne_inf=-10
borne_sup=10
nombre_mystere=$(( borne_inf + RANDOM % ( borne_sup - borne_inf ) ))

read -p "Donner un entier relatif entre $borne_inf et $borne_sup : " nombre_donne


# if [[ $nombre_donne -lt $nombre_mystere ]] ; then
#     echo "Le nombre mystère est plus grand que $nombre_donne."
# elif [[ $nombre_donne -gt $nombre_mystere ]] ; then
#     echo "Le nombre mystère est plus petit que $nombre_donne"
# else
#     echo "Vous avez trouvé le nombre mystère !"
# fi


while [[ $nombre_donne -ne $nombre_mystere ]] ; do
    if (( $nombre_donne < $nombre_mystere )) ; then
        echo "Le nombre mystère est plus grand que $nombre_donne."
    else
        echo "Le nombre mystère est plus petit que $nombre_donne."
    fi
    read -p "Donner un entier relatif entre $borne_inf et $borne_sup : " nombre_donne
done

echo "Vous avez trouvé le nombre mystère !"