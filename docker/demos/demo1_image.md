# Commandes Docker pour les images 

## Rechercher une image 

```bash
docker search <nom_image>
```

Exemple :

```bash
docker search mysql
```

## Télécharger une image

Pour télécharger une image depuis Docker Hub:

```bash
docker pull <nom_image>[:tag]
```

Exemple 

```bash
docker pull mysql:latest
```

## Lister les images locales

Pour voir toutes les images qui ont été téléchargés localement :

```bash
docker images
```

## Inspecter une image 

Pour obtenir les détails sur une image :

```bash
docker inspect <nom_image>[:tag]
```

Exemple : 

```bash
docker inspect mysql
```

## Supprimer une image 

Pour supprimer une image en local : 

```bash
docker rmi <nom_image>[:tag]
```

Exemple : 

```bash
docker rmi mysql
```

Si l'image est utilisé par un conteneur (même arrêté), nous pouvons forcer la suppression avec `-f`

```bash
docker rmi -f <nom_image>[:tag]
```

## Tagger une image 

Pour ajouter un tag : 

```bash
docker tag <nom_image_existante>[:tag_existant] <nouveau_nom_image>[:nouveau_tag]
```

Exemple : 

```bash
docker tag mysql:latest mysql:v1.0
```

## Pousser une image vers un registre

Pour pousser une image local vers DockerHub ou un autre registre Docker :

```bash
docker push <nom_image>[:tag]
```

Exemple : 

```bash
docker push myrepo/myimage:latest
```

## Sauvegarder une image 

Pour sauvegarder une image dans un fichier tar :

```bash
docker save -o <chemin_de_sortie> <image_name>:<tag> 
```

Exemple : 

```bash
docker save -o ubuntu_latest.tar ubuntu:latest 
```

## Charger une image

Pour charger une image à partir d'un fichier tar :

```bash
docker load -i <chemin_dentree> 
```

Exemple : 

```bash
docker load -i ubuntu_latest.tar
```

## Historique d'une image 

Pour voir l'historique des couches d'une images : 

```bash
docker history <nom_image>[:tag]
```

Exemple :

```bash
docker history ubuntu:latest
```

## Supprimer les images Dangling

Si l'on créer plusieurs fois la même images (via docker build), nous obtiendrons des images solitaires.

Pour supprimer les images intermédiaires non-utilisé (dangling)

```bash
docker image prune
```

## Supprimer toutes les images

Pour supprimer toutes les images localement :

```bash
docker rmi -f $(docker images -q)
```

