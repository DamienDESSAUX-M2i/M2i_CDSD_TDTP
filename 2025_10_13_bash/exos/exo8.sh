#!/bin/bash


NOM_FICHIER="$HOME/animal.txt"

cat > $NOM_FICHIER << EOF
Rufus Lapin 3
Rex Chien 4
Fido Chien 5
Ponpon Lapin 2
Nemo Poisson 1
Furax Furet 3
Hector Castor 5
Dragor Dragon 120
EOF

echo "=== Toutes les lignes contenant 'Chien' ==="
grep 'Chien' $NOM_FICHIER

echo
echo "=== Toutes les lignes contenant 5 avec numéro de ligne ==="
grep -n '5' $NOM_FICHIER

echo
echo "=== Toutes les lignes qui ne contiennent pas 'Nemo' ==="
grep -v 'Nemo' $NOM_FICHIER

echo
echo "=== Toutes les lignes contenant la lettre 'L' ==="
grep -i 'l' $NOM_FICHIER

echo
echo "=== Toutes les lignes qui contiennent soit 'Lapin' soit 'Furet' ==="
grep -E 'Lapin|Furet' $NOM_FICHIER

echo
echo "=== Toutes les lignes qui contiennent un mot commançant par 'Dr' et finissant par 'on' ==="
grep -E '.*(Dr[[:alnum:]]*on).*' $NOM_FICHIER

rm $NOM_FICHIER
