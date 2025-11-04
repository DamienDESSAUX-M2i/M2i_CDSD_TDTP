# Commande dockerfile

## FROM 

- Usage : FROM <image>[:<tag>] [AS <name>]
- Description : Spécifie l'image de base à partir de laquelle construire l'image Docker. 

## LABEL

- Usage : LABEL <key>=<value> 
- Description : Ajout des métadonnée à l'image
- Exemple : LABEL maintainer="loick@utopios.solutions"

## ENV

- Usage : ENV <key>=<value>
- Description : Définir les variables d'environnements
- Exemple : ENV MYSQL_ROOT_PASSWORD=secret

## RUN

- Usage : RUN <command>
- Description : Execute une commande intermédiaire pendans la construction de l'image. 
- Exemple : RUN apt update && apt upgrade && apt install nano

## COPY

- Usage : COPY <src> <dest> (le chemin de la source est basé sur l'emplacement du Dockerfile)
- Description : Copie un fichier/dossier du syseme hote dans le conteneur
- Exemple : COPY . /usr/share/nginx/html 

## ADD

- Usage : ADD <src> <dest>
- Description : Similaire à COPY, mais peut aussi extraire des fichiers compressé.

## CMD 

- Usage : CMD ["commande", "arg1", "arg2"]
- Description : Permet d'executer une commande dès le lancement du conteneur.
- Exemple : CMD ["python", "main.py"]

## ENTRYPOINT

- Usage : ENTRYPOINT ["commande", "arg1", "arg2"]
- Description : Configure une commande qui sera toujours executé dans le conteneur.
- Exemple : ENTRYPOINT ["nginx", "-g", "daemon off;"]