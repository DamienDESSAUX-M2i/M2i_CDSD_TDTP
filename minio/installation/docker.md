# MinIO

## Construction d'un conteneur sur docker

- `docker run` -> création d'un conteneur
- `-d` -> tâche de fond
- `--name minio` -> nom du conteneur
- `-p` -> 1 port terminal + 1 port interface
- `-e` -> varialbes d'environnement
- `-v` -> montage d'un volume
- `quay.io/minio/minio` -> image
- `server /data --console-address ":9001"` -> serveur

```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -v C:/Users/Administrateur/Documents/M2i_CDSD_TDTP/minio/intallation/minio-data/minio-data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

```powershell
docker run -d `
  --name minio `
  -p 9000:9000 `
  -p 9001:9001 `
  -e "MINIO_ROOT_USER=minioadmin" `
  -e "MINIO_ROOT_PASSWORD=minioadmin" `
  -v "C:\Users\Administrateur\Documents\M2i_CDSD_TDTP\minio\intallation\minio-data:/data" `
  quay.io/minio/minio server /data --console-address ":9001"
```