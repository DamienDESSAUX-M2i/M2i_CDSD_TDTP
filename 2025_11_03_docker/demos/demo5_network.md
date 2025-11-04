1. Création d'un réseau personnalisé

```bash
docker network create mon_reseau
```

2. Création de deux conteneurs sur un même réseau

```bash
docker run -d --name container1 --network mon_reseau nginx
docker run -d --name container2 --network mon_reseau nginx
```

3. Se connecter à container1

```bash
docker exec -it container1 bash
apt update
apt upgrade
apt install -y iputils-ping

ping container2
```

4. Liste des réseaux

```bash
docker network ls
```

5. Pour connecter un conteneur à un réseau

```bash
docker network connect mon_reseau container1
```

6. Pour connaitre l'adresse IP interne 

```bash
docker network inspect mon_reseau
```

7. Pour déconnecter un conteneur d'un réseau


```bash
docker network disconnect mon_reseau container1
```

8. Supprimer un reseau

```bash
docker network rm mon_reseau
```