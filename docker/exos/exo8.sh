# Créez un network (network1)
docker network create network1

# Affichez-en la liste
docker network ls

# Run un conteneur rattaché à votre network "network1"
docker run -d --name container1 --network network1 nginx

# Run un autre conteneur, puis dans un 2e temps rattachez-le à "network1"
docker run -d --name container2 nginx
docker network connect network1 container2

# Récupérez l'adresse ip d'un conteneur
docker network inspect network1
# container1 -> "IPv4Address": "172.18.0.2/16"
# container2 -> "IPv4Address": "172.18.0.3/16"

# Essayez de ping les conteneurs entre eux (par leur nom et par leur ip)
docker exec -it container1 bash
    apt update
    apt upgrade
    apt install -y iputils-ping
    ping container2
    ping 172.18.0.3

# Affichez les conteneurs reliés au "network1"
docker network inspect network1
# "Name": "container1"
# "Name": "container2"

# Déconnectez les conteneurs du network
docker network disconnect network1 container1
docker network disconnect network1 container2

# Supprimez le network créé
docker network rm network1