# TP : Pipeline de Données E-Commerce

## Scraping, Stockage Hybride MinIO & MongoDB

### Cursus Data & IA - Module Data Engineering

---

## Contexte du Projet

Vous êtes Data Engineer dans une startup de veille concurrentielle. Votre mission est de construire un pipeline automatisé pour collecter et analyser les données produits d'un site e-commerce de démonstration.

**Site cible** : https://webscraper.io/test-sites/e-commerce/allinone

---

## Objectifs Pédagogiques

À l'issue de ce TP, vous serez capable de :

- Concevoir un scraper robuste avec gestion de la pagination
- Implémenter une architecture de stockage hybride adaptée aux données
- Exploiter MongoDB pour des requêtes analytiques complexes
- Utiliser MinIO pour le stockage d'assets binaires
- Préparer des données pour des cas d'usage Machine Learning

---

## Architecture Cible

```
┌────────────────────┐
│   webscraper.io    │
│   (E-commerce)     │
└─────────┬──────────┘
          │ Scraping
          ▼
┌────────────────────┐
│      Scraper       │
│      Python        │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌────────┐  ┌────────┐
│ MinIO  │  │MongoDB │
│        │  │        │
│ Images │  │Produits│
│ Exports│  │ Stats  │
│ Backups│  │ Logs   │
└────────┘  └────────┘
    │           │
    └─────┬─────┘
          ▼
┌────────────────────┐
│   Analytics &      │
│   ML Datasets      │
└────────────────────┘
```

### Justification de l'Architecture Hybride

- MongoDB propose un stockage orienté document au format BSON. Il sera adapté aux données qui peuvent être mises sous forme d'un fichier JSON. De plus, il propose une indexation qui accélère la lecture des données.
- MinIO propose quand à lui un stockage objet. Il propose l'ajout de métadonnées.

---

## Partie 1 : Exploration du Site Cible 

### 1.1 Découverte de la structure

Avant de coder, explorez manuellement le site : https://webscraper.io/test-sites/e-commerce/allinone

**Questions à résoudre :**

1. Quelles sont les catégories de produits disponibles ?

-> Les catégories de produits disponibles sont `Computer` et `Phone`.

2. Comment fonctionne la pagination ?

-> Un lien permet de passer à la page suivant. Son sélecteur CSS est `a.page-link.next`.

3. Quelles informations sont disponibles sur la page liste vs page détail ?

-> Les informations principales de la page liste sont : Le nom de la catégorie et les articles vendus. Chaque article contient les informations suivantes : image, nom, prix, description, note, et nombre d'avis.

Les informations principales de la page détaillées sont :
- Pour les laptops : image, nom, prix, description, note, nombre d'avis et une sélection HDD.
- Pour les tablets : image, nom, prix, not, nombre d'avis, une sélection couleur et une sélection HDD
- Pour les Touch : image, prix, description, note, nombre d'avis et une sélection couleur.

4. Où se trouvent les images des produits ?

-> Tous les produits ont la même image accessible par le lien : https://webscraper.io/images/test-sites/e-commerce/items/cart2.png.

### 1.2 Analyse de la structure HTML



### 1.3 Exercice préparatoire

Complétez le tableau suivant en inspectant le HTML :

Je me place sur une page produit.

| Donnée | Sélecteur CSS | Exemple de valeur |
|--------|---------------|-------------------|
| Titre du produit | h4 a::attr(title) | Asus VivoBook X441NA-GA190 |
| Prix | h4 span::text | $295.99 |
| Description | p.description::text | Asus VivoBook X441NA-GA190 Chocolate Black, 14", Celeron N3450, 4GB, 128GB SSD, Endless OS, ENG kbd |
| Rating (étoiles) | p.review-count + p::attr(data-rating) | 2 |
| URL de l'image | img.img-fluid::attr(src) | /images/test-sites/e-commerce/items/cart2.png |
| Lien vers détails | h4 a::attr(src) | /test-sites/e-commerce/static/product/31 |

---

## Partie 2 : Infrastructure Docker 

### 2.1 Structure du projet

Créez l'arborescence du projet.

```
│   docker-compose.yml
│   main.py
│   requirements.txt
│   
├───config
│       __init__.py
│       settings.py
│       
└───src
    │   pipeline.py
    │   scrapper.py
    │   __init__.py
    │   
    └───storage
            minio_client.py
            mongo_client.py
            __init__.py
```

### 2.2 Docker Compose

Créez le fichier `docker-compose.yml` pour le projet.

```yaml
name: s3_mino

services:
  minio:
    image: minio/minio:latest
    container_name: workshop-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  mongodb:
    image: mongo:7.0
    container_name: workshop-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
      MONGO_INITDB_DATABASE: scraping_db
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 30s
      timeout: 10s
      retries: 3

  mongo-express:
    image: mongo-express:latest
    container_name: workshop-mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin123
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin123@mongodb:27017/
      ME_CONFIG_BASICAUTH: false
    depends_on:
      - mongodb

volumes:
  minio_data:
  mongo_data:
```

### 2.3 Dépendances Python

Créez le fichier `requirements.txt`.

```
# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.3
# lxml==5.1.0
fake-useragent==1.4.0

# Stockage
minio==7.2.3
pymongo==4.6.1

# Utilitaires
python-dotenv==1.0.1
structlog==24.1.0
tenacity==8.2.3
tqdm==4.66.1

# Traitement de données
pandas==2.2.0
numpy==1.26.4
```


### 2.4 Configuration

Créez les fichiers de configuration.

Création des classes `MinIOConfig`, `MongoDBConfig` et `ScraperConfig`.
Le fichier `config.__init__.py` permet d'importer une instance des classes précédentes : `minio_config`, `mongo_config` et `scraper_config`.

---

## Partie 3 : Clients de Stockage

### 3.1 Client MinIO

Création de la classe `MinIOStorage` dans le fichier `src/storage/minio_client.py` :
- J'ai copié le fichier de la démo.

### 3.2 Client MongoDB

Création de la classe `MongoStorage` dans le fichier `src/storage/mongo_client.py` :
- Modification du fichier de la démo :
  - modification du nom des collections : produits, stats, logs
  - modification des méthodes associées

---

## Partie 4 : Scraper E-Commerce 

### 4.1 Scraper principal

Définition du modèle `Product` :
- title: str
- price: float
- description: str
- rating: int
- image_url: str
- details_url: str

Création de la classe `ProductsScraper`. J'ai modifié le fichié démo.

---

## Partie 5 : Pipeline Intégré

### 5.1 Pipeline principal

Création de la classe `ProductsPipeline`. Modification de la démo.

---

## Partie 6 

### Exercice 1 : Validation de l'infrastructure 

**Questions à répondre :**

1. Combien de produits ont été scrapés ?

-> Pour les 

2. Quelle est la structure d'un document produit dans MongoDB ?
3. Comment sont organisées les images dans MinIO ?

---

### Exercice 2 : Requêtes MongoDB 

**Objectif** : Maîtriser les requêtes et agrégations.

Créez le fichier `exercises/ex2_mongo_queries.py` :

```python
"""
Exercice 2 : Requêtes MongoDB

Complétez les fonctions TODO.
"""

from src.storage import MongoDBStorage


def exercise_2():
    mongo = MongoDBStorage()
    
    # 2.1 Trouvez tous les laptops avec un prix < 500$
    # TODO
    cheap_laptops = None
    
    # 2.2 Trouvez le produit le plus cher de chaque catégorie
    # Indice: utilisez $group avec $max et $first
    # TODO
    most_expensive_by_cat = None
    
    # 2.3 Calculez le prix moyen des produits avec rating >= 4
    # TODO
    avg_price_good_rating = None
    
    # 2.4 Trouvez les produits dont le titre contient "Samsung" ou "Apple"
    # Indice: utilisez $regex ou $in
    # TODO
    brand_products = None
    
    # 2.5 Créez un classement des produits par rapport qualité/prix
    # Score = rating / (price / 100)
    # Retournez le top 10
    # TODO
    value_ranking = None
    
    # 2.6 Groupez les produits par tranche de prix (0-200, 200-500, 500-1000, 1000+)
    # et comptez le nombre de produits par tranche
    # TODO
    price_ranges = None
    
    # 2.7 Trouvez les produits qui ont le même prix (doublons de prix)
    # Indice: $group puis $match sur count > 1
    # TODO
    same_price_products = None
    
    mongo.close()
    
    return {
        "cheap_laptops": cheap_laptops,
        "most_expensive_by_cat": most_expensive_by_cat,
        "avg_price_good_rating": avg_price_good_rating,
        "brand_products": brand_products,
        "value_ranking": value_ranking,
        "price_ranges": price_ranges,
        "same_price_products": same_price_products
    }


if __name__ == "__main__":
    results = exercise_2()
    
    for name, result in results.items():
        print(f"\n{'='*50}")
        print(f"{name}:")
        print(f"{'='*50}")
        
        if isinstance(result, list):
            for item in result[:5]:  # Limiter l'affichage
                print(item)
            if len(result) > 5:
                print(f"... et {len(result) - 5} autres")
        else:
            print(result)
```

---

### Exercice 3 : Opérations MinIO

**Objectif** : Manipuler le stockage objet.

Créez le fichier `exercises/ex3_minio_operations.py` :

```python
"""
Exercice 3 : Opérations MinIO

Complétez les fonctions TODO.
"""

from PIL import Image
import io
from src.storage import MinIOStorage, MongoDBStorage


def exercise_3():
    minio = MinIOStorage()
    mongo = MongoDBStorage()
    
    # 3.1 Listez toutes les images et calculez la taille totale
    # TODO
    total_images = 0
    total_size_kb = 0
    
    # 3.2 Créez des thumbnails (100x100) pour toutes les images
    # Stockez-les dans le même bucket avec préfixe "thumbnails/"
    # Indice: Utilisez PIL (Pillow)
    # TODO
    thumbnails_created = 0
    
    # 3.3 Générez une URL présignée (24h) pour l'image du produit le plus cher
    # TODO
    presigned_url = None
    
    # 3.4 Créez un rapport JSON avec les stats de chaque catégorie d'images
    # et uploadez-le dans le bucket exports
    # Format: {"laptops": {"count": X, "size_kb": Y}, ...}
    # TODO
    stats_report = {}
    
    # 3.5 Implémentez une fonction qui copie toutes les images
    # vers un nouveau bucket "backup-YYYYMMDD"
    # TODO
    backup_created = False
    
    mongo.close()
    
    return {
        "total_images": total_images,
        "total_size_kb": total_size_kb,
        "thumbnails_created": thumbnails_created,
        "presigned_url": presigned_url,
        "stats_report": stats_report,
        "backup_created": backup_created
    }


if __name__ == "__main__":
    results = exercise_3()
    
    for name, result in results.items():
        print(f"{name}: {result}")
```

---

