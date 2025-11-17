# Question 2
docker search nginx # nginx -> Oficial
# Question 3
docker pull nginx
# Question 4
docker run -d -p 8080:80 --name my_nginx nginx
# Question 5
docker ps # my_nginx est en cours d'exécution
# http://localhost:8080 -> Welcome to nginx!
# Question 6
docker exec -it my_nginx bash
find . -name index.html # Le fichier index.html est dans le répertoire ./usr/share/nginx/html/
apt upgrade
apt update
apt install vim
vim ./usr/share/nginx/html/index.html
# http://localhost:8080 -> Welcome to nginx Damien DESSAUX!
# Question 7
docker stop my_nginx
docker rm my_nginx