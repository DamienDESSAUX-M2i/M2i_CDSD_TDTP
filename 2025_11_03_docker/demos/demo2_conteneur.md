# Commande docker pour les conteneurs

## Lancer un conteneur : 

```bash
docker run [options] nom_image [command] [arg...]
```

Exemple : 

```bash
# Lance un conteneur nginx en arrière plan avec un port interne (docker) de 80 et un port externe (machine) de 80
docker run -d -p 80:80 nginx 
```

- Les options utiles : 
    - -it : terminal interactif
    - -p : port externe/interne
    - -e : variable d'environnement
    - -d : lancé en arrière plan
    - --name : Nommer le conteneur

## Lister les conteneurs : 

```bash
docker ps [options]
```

Exemple : 

```bash
# Affiche tous les conteneurs, y compris ceux qui sont arrêtés.
docker ps -a 
```

## Arrêter un conteneur

```bash
docker stop <nom_conteneur>
```

Exemple : 

```bash
docker stop nginx
```

## Redémarrer un conteneur

```bash
docker restart <nom_conteneur>
```

Exemple : 

```bash
docker restart nginx
```

## Supprimer un conteneur

```bash
docker rm <nom_conteneur>
```

Exemple : 

```bash
# Supprime le conteneur après l'avoir arrêté
docker rm nginx 
```

## Logs du conteneurs

Les logs sont les informations que nous avions dans notre terminal lors du démarrage d'une API, d'une application ou d'une BDD. 

```bash
docker logs <nom_conteneur>
```

Exemple : 

```bash
docker logs mysql 
```

## Executer une commande dans un conteneur actif

```bash
docker exec [options] <nom_conteneur> commande [args...]
```

Exemple : 

```bash
# Ouvrir une session bash dans le conteneur
docker exec -it nom_conteneur bash
```

## Inspecter un conteneur

```bash
docker inspect <nom_conteneur>
```

Exemple : 

```bash
# Fournit les détails sur le conteneur
docker inspect conteneur-mysql 
```

## Afficher les statistiques de l'utilisation des ressources par les conteneurs

```bash
docker stats
```
