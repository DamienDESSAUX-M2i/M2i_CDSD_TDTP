# Créer image
docker build -t angular1:1.0 .
# Créer conteneur
docker run -d -p 4201:4200 --name angular1 angular1:1.0