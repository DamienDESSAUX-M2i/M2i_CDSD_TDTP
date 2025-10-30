#!/bin/bash

casse=$1
mot=${2,,}

case $casse in
    -maj)
        echo "${mot^^}"
        ;;
    -min)
        echo "$mot"
        ;;
    -cap)
        echo "${mot^}"
        ;;
    *)
        echo "Erreur, les options disponibles sont [-maj,-min,-cap]"
        ;;
esac