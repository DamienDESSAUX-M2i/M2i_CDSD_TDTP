# Créer image
docker build -t app_python1:1.0 .
# Créer conteneur
docker run -it --name app_python1 app_python1:1.0