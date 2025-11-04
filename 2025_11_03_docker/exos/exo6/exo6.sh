# Créer image
docker build -t web_nginx1:1.0 .
# Créer conteneur
docker run -d -p 8080:80 --name web_nginx1 web_nginx1:1.0