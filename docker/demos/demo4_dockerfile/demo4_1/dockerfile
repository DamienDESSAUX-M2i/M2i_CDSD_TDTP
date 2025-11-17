# image sur laquelle on se base
FROM nginx:latest
# répertoire de travail dans le conteneur
WORKDIR /usr/share/nginx/html
# commandes effectuées dans le conteneur
RUN rm -f ./*
RUN apt update
RUN apt upgrade
RUN apt install vim
# copie du répertoire dans lequel se trouve le Dockerfile
# vers le répertoire de travail du conteneur
COPY . .
# port interne du conteneur
EXPOSE 80
# commande effectuées à la construction du conteneur
CMD ["nginx", "-g", "deamon off;"]