# Data Quality Streaming Dashboard

Projet Docker Compose avec 4 conteneurs :

1. `kafka` : Redpanda compatible Kafka
2. `data-generator` : génération de données aléatoires
3. `data-analyzer` : calcul des métriques qualité
4. `data-dashboard` : dashboard Streamlit avec graphiques

## Lancer

```bash
docker compose down -v
docker compose up --build
```

## Dashboard

```txt
http://localhost:8501
```

## Métriques affichées

- Taux de complétude
- Taux de doublons
- Taux d'erreurs
- Volume de lignes
- Répartition lignes valides / invalides / doublons
- Évolution temps réel
- Types d'erreurs détectées
