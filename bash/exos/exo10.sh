#!/bin/bash

read -p "Entrer un nombre: " a
read -p "Entrer un nombre: " b
# a=5
# b=10

echo "a = $a et b = $b"

c=$a
a=$b
b=$c

echo
echo "Swap a et b"
echo "a = $a et b = $b"

a=$((a-b))
b=$((b+a))
a=$((b-a))

echo
echo "2e Swap a et b"
echo "a = $a et b = $b"