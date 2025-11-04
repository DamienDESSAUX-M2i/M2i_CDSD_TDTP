# Commandes pour les volumes

## Créer un volume docker

```bash
docker volume create <volume_name>
```

## Lister les volumes docker 

```bash
docker volume ls
```

## Inspect un volume docker

```bash
docker volume inspect <volume_name>
```

## Supprimer un volume

```bash
docker volume rm <volume_name>
```

## Supprimer tout les volumes non-utilisé

```bash
docker volume prune
```

## Lancer un conteneur avec un volume

```bash
docker run --name <container_name> -v <volume_name>:/path/to/volume -d <image_name>
```

## Supprimer un conteneur avec son volume associé

```bash
docker rm -v <container_name>
```
