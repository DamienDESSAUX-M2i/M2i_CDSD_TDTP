# Exercice 1 : Votre premier Dockerfile

## Objectif

Créer un Dockerfile pour conteneuriser un script Python qui analyse des données.

Vous devez créer un projet qui analyse des données de ventes et génère un rapport.

### Fichiers fournis

**data.csv** (à créer) :

```csv
date,produit,quantite,prix_unitaire
2024-01-01,Laptop,2,1200
2024-01-02,Souris,5,25
2024-01-03,Clavier,3,75
2024-01-04,Laptop,1,1200
2024-01-05,Écran,2,300
```

**analyse.py** (à créer) :

```python
import pandas as pd

# Charger les données
df = pd.read_csv('data.csv')

# Calculer le montant total
df['montant_total'] = df['quantite'] * df['prix_unitaire']

# Afficher les statistiques
print(f"Nombre total de transactions: {len(df)}")
print(f"Chiffre d'affaires total: {df['montant_total'].sum()}€")
print(f"Produit le plus vendu:")
print(df.groupby('produit')['quantite'].sum().sort_values(ascending=False).head(1))
print(f"Produit le plus rentable:")
print(df.groupby('produit')['montant_total'].sum().sort_values(ascending=False).head(1))
```

## Tâches à réaliser

### Niveau 1 : Basique

1. **Créer la structure du projet** :

```
exercice1/
├── Dockerfile
├── requirements.txt
├── data.csv
└── analyse.py
```

2. **Créer le fichier `requirements.txt`**

3. **Créer le Dockerfile**

4. **Construire et exécuter**

### Niveau 2 : Intermédiaire

Améliorez votre Dockerfile pour :

1. **Ajouter des métadonnées** :

```dockerfile
LABEL maintainer="votre.email@example.com"
LABEL version="1.0"
LABEL description="Analyse des ventes"
```

2. **Utiliser un utilisateur non-root** :

```dockerfile
RUN useradd -m appuser
USER appuser
```

3. **Créer un fichier `.dockerignore`** pour exclure :
   - `__pycache__/`
   - `*.pyc`
   - `.git/`

### Niveau 3 : Avancé (Bonus)

1. **Rendre le script paramétrable** :

Modifier `analyse.py` pour accepter le nom du fichier en argument :

```python
import pandas as pd
import sys

# Récupérer le fichier depuis les arguments ou utiliser data.csv par défaut
fichier = sys.argv[1] if len(sys.argv) > 1 else 'data.csv'

df = pd.read_csv(fichier)
# ... reste du code
```

Adapter le Dockerfile

2. **Tester avec des données différentes**
