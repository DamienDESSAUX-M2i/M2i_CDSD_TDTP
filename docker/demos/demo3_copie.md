# Copier un fichier ou un dossier entre un conteneur et le systeme local.

## Copier un fichier du systeme local vers un conteneur

```bash
docker cp [chemin_du_fichier_local] [nom_du_conteneur]:[chemin_dans_le_conteneur]
```

Exemple : 

```bash
docker cp ./index.html my-nginx:/usr/share/nginx/html
```

## Copier un fichier du conteneur vers le systeme

```bash
docker cp [nom_du_conteneur]:[chemin_dans_le_conteneur] [chemin_du_fichier_local] 
```

Exemple : 

```bash
docker cp my-nginx:/usr/share/nginx/html/index.html . # Copie la ou se trouve le terminal docker
```

Pour les dossiers c'est la même chose, hormis que l'on précise le dossier complet plutot qu'un fichier.

