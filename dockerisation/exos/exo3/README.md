## Build image

```bash
docker build --no-cache -t exo3 .
```

## Execute container

```bash
docker run --rm -v ${pwd}/data:/app/data -v ${pwd}/logs:/app/logs -v ${pwd}/models:/app/models exo3
```
