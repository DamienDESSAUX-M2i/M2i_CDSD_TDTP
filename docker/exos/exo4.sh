# Partie 1
docker search 2048
docher pull oats87/2048
docker images # oats87/2048 est bien présent
docker run -d -p 8080:80 --name jeu-damien oats87/2048
docker ps # le conteneur jeu-damien est bien lancé
docker run -d -p 8181:80 --name jeu-dessaux oats87/2048
docker ps # les deux conteneurs sont lancés
docker stop jeu-damien jeu-dessaux # les 2 jeux fonctionnent toujours mais si j'actualise la page ils saissent de fonctionner
docker restart jeu-damien jeu-dessaux # les 2 jeux fonctionnent normalement
docker stop jeu-damien jeu-dessaux
docker rm jeu-damien jeu-dessaux
docker ps -a # les conteneurs jeu-damien et jeu-dessaux sont bien supprimés
docker rmi oats87/2048
docker images # l'image oats87/2048 est bien supprimée

# Partie 2
docker pull nginx
docker images # l'image nginx est bien présente
docker run -d -p 8080:80 --name nginx-web nginx
docker ps # le conteneur nginx_web est bien lancé
# http://localhost:8080/ -> Welcome to nginx!
docker exec -it nginx-web bash
apt update
apt upgrade
apt install vim
vim ./usr/share/nginx/html/index.html
docker stop nginx-web
docker restart nginx-web
# http://localhost:8080/ -> Welcome to nginx Damien DESSAUX!
docker pull httpd # apache
docker run -d -p 8181:80 --name apache-web httpd
docker exec -it apache-web bash
apt update
apt upgrade
apt install vim
vim ./htdocs/index.html
# http://localhost:8181/ -> Je suis heureux

# Partie 3
docker run -d -p 8383:80 --name nginx-web3 nginx
docker run -d -p 8484:80 --name nginx-web4 nginx
docker run -d -p 8585:80 --name nginx-web5 nginx
docker cp C:\Users\Administrateur\Downloads\html5up-editorial-m2i\. nginx-web3:./usr/share/nginx/html/
docker cp C:\Users\Administrateur\Downloads\html5up-massively\. nginx-web4:./usr/share/nginx/html/
docker cp C:\Users\Administrateur\Downloads\html5up-paradigm-shift\. nginx-web5:./usr/share/nginx/html/
docker stop nginx-web3 nginx-web4 nginx-web5