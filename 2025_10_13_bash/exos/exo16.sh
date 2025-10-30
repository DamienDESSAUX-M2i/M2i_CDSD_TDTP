#!/bin/bash

caractere=""
read -p "Donner un caractere : " caractere

case $caractere in
    [[:alpha:]])
        case $caractere in
            [aeiouAEIOU])
                echo "C'est un voyelle"
                ;;
            *)
                echo "C'est une consonne"
                ;;
        esac
        ;;
    *)
        echo "Ce n'est pas un caractère alphanumérique"
        ;;
esac
