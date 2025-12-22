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

- MongoDB propose un stockage orienté document au format BSON. Il sera adapté aux données qui peuvent être mises sous forme d'un fichier JSON comme les produits. De plus, il propose une indexation qui accélère la lecture des données.
- MinIO propose quant à lui un stockage orienté objet. Il permet l'ajout de métadonnées qui enrichie les fichiers binaires comme les images.

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

-> Les informations principales de la page liste sont :
- le nom de la catégorie
- le nom de la sous-catégorie
- le lien de l'image, le nom, le lien de la page détaillée, le prix, la description partielle, la note, et le nombre d'avis d'au plus 10 articles.

-> Les informations principales de la page détaillées sont :
- Pour les laptops :
  - le lien de l'image
  - le nom
  - le prix
  - la description complète
  - la note
  - le nombre d'avis
  - une sélection HDD
- Pour les tablets :
  - le lien de l'image
  - le nom
  - le prix
  - la note
  - le nombre d'avis
  - une sélection couleur
  - une sélection HDD
- Pour les Touch :
  - le lien de l'image
  - le prix
  - la description
  - la note
  - le nombre d'avis
  - une sélection couleur

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
│   exo2_mongo_queries.py
│   exo3_minio_operations.py
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

-> Le fichier `docker-compose.yml` comprend trois service : `minio`, `mongo` et `mongo-express`.

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

Création de la classe `MinIOStorage` dans le fichier `src/storage/minio_client.py`.

### 3.2 Client MongoDB

Création de la classe `MongoStorage` dans le fichier `src/storage/mongo_client.py`.

---

## Partie 4 : Scraper E-Commerce 

### 4.1 Scraper principal

Création des classes `Product` et `ProductsScraper` dans le fichier `src/scrapper.py`.

Définition du modèle `Product` :
- id_product: uuid
- category: str
- ub_category: str
- title: str
- price: float
- description: str
- rating: int
- image_url: str
- details_url: str

---

## Partie 5 : Pipeline Intégré

### 5.1 Pipeline principal

Création de la classe `ProductsPipeline` dans le fichier `src/pipeline.py`.

---

## Partie 6 

### Exercice 1 : Validation de l'infrastructure 

**Questions à répondre :**

1. Combien de produits ont été scrapés ?

-> Au total 147 produits ont été scrappés.

Affichage concole :

====================================
Total products: 147
    Total computers: 138
        Total computers/laptops: 117
        Total computers/tablets: 21
    Total phones: 9
        Total phones/touch: 9
====================================

2. Quelle est la structure d'un document produit dans MongoDB ?

-> Dans MondoDB un document produit a la structure suivante :
- _id: ObjectId
- id_product: str
- category: str
- sub_category: str
- title: str
- price: float | int
- description: str
- rating: int
- image_url: str
- details_url: str

3. Comment sont organisées les images dans MinIO ?

Dans MinIO, le filename des images suis la structure suivante `products_images/category/subcategor/id_produit.jpeg`.

---

### Exercice 2 : Requêtes MongoDB 

**Objectif** : Maîtriser les requêtes et agrégations.

Créez le fichier `exercises/ex2_mongo_queries.py` :

-> J'ai placé le fichier `ex2_mongo_queries.py` à la racine du projet en raison des imports.

```python
"""
Exercice 2 : Requêtes MongoDB

Complétez les fonctions TODO.
"""

from src.storage import MongoDBStorage


def exercise_2():
    mongo = MongoDBStorage()
    
    # 2.1 Trouvez tous les laptops avec un prix < 500$
    cheap_laptops = mongo.get_cheap_laptops()

    # 2.2 Trouvez le produit le plus cher de chaque catégorie
    # Indice: utilisez $group avec $max et $first
    most_expensive_by_cat = mongo.get_most_expensive_by_cat()

    # 2.3 Calculez le prix moyen des produits avec rating >= 4
    avg_price_good_rating = mongo.get_avg_price_good_rating(rating=4)

    # 2.4 Trouvez les produits dont le titre contient "Samsung" ou "Apple"
    # Indice: utilisez $regex ou $in
    brand_products = mongo.get_brand_products(text_inside=["Samsung", "Apple"])

    # 2.5 Créez un classement des produits par rapport qualité/prix
    # Score = rating / (price / 100)
    # Retournez le top 10
    value_ranking = mongo.get_value_ranking()

    # 2.6 Groupez les produits par tranche de prix (0-200, 200-500, 500-1000, 1000+)
    # et comptez le nombre de produits par tranche
    price_ranges = mongo.get_price_ranges()

    # 2.7 Trouvez les produits qui ont le même prix (doublons de prix)
    # Indice: $group puis $match sur count > 1
    same_price_products = mongo.get_same_price_products()

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

-> Ajout de méthodes dans le fichier `src/storage/mongo_client.py` pour l'exercice 2.

```python
    def get_cheap_laptops(self) -> list[dict]:
        """Trouve les laptops inférieurs à 500€"""
        return self.find_products(
            {"sub_category": "laptops", "price": {"$lt": 500}},
            {"_id": 0, "title": 1, "price": 1},
            [("price", pymongo.DESCENDING)],
        )

    def get_most_expensive_by_cat(self) -> list[dict]:
        """Trouve les produits les plus cher par catégorie"""
        pipeline = [
            {
                "$group": {
                    "_id": {"category": "$category"},
                    "max_price": {"$max": "$price"},
                }
            },
            {"$project": {"_id": 0, "category": "$_id.category", "max_price": 1}},
        ]
        return list(self.products.aggregate(pipeline))

    def get_avg_price_good_rating(self, rating: int) -> float:
        """Calcule la moyenne des prix des produits dont le note est supérieur ou égale à rating"""
        pipeline = [
            {"$match": {"rating": {"$gte": rating}}},
            {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}},
        ]
        result = list(self.products.aggregate(pipeline))
        return result[0]["avg_price"] if result else 0

    def get_brand_products(self, text_inside: list[str]) -> list[dict]:
        """Trouve les produit dont le nom contient un des item de la list text_inside"""
        regex = "|".join(text_inside)
        return self.find_products(
            {"title": {"$regex": regex, "$options": "i"}}, {"_id": 0, "title": 1}
        )

    def get_value_ranking(self) -> list[dict]:
        """Trouve les 10 produits ayant le meilleur score où score=rating/(price/100)"""
        pipeline = [
            {
                "$addFields": {
                    "score": {"$divide": ["$rating", {"$divide": ["$price", 100]}]}
                }
            },
            {"$sort": {"score": -1}},
            {"$limit": 10},
            {"$project": {"_id": 0, "title": 1, "score": 1}},
        ]
        return list(self.products.aggregate(pipeline))

    def get_price_ranges(self) -> list[dict]:
        """Groupe les produits par interval de prix et compte le nombre produits par groupe"""
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$price",
                    "boundaries": [0, 200, 500, 1000, float("inf")],
                    "default": "out_of_range",
                    "output": {
                        "number_of_products": {"$sum": 1},
                    },
                }
            }
        ]
        return list(self.products.aggregate(pipeline))

    def get_same_price_products(self) -> list[dict]:
        """Trouve les produits ayant le même prix"""
        pipeline = [
            {"$group": {"_id": {"price": "$price"}, "nb_occurrences": {"$sum": 1}}},
            {"$match": {"nb_occurrences": {"$gt": 1}}},
        ]
        return list(self.products.aggregate(pipeline))

```

-> Affichage console :

==================================================
cheap_laptops:
==================================================
{'price': 498.23, 'title': 'Lenovo V510 Black'}
{'price': 497.17, 'title': 'Dell Vostro 15 (3568) Red'}
{'price': 494.71, 'title': 'Acer Aspire 3 A315-51 Black'}
{'price': 488.78, 'title': 'Dell Vostro 15'}
{'price': 488.64, 'title': 'Acer Swift 1 SF113-31 Silver'}
... et 33 autres

==================================================
most_expensive_by_cat:
==================================================
{'max_price': 1799.0, 'category': 'computers'}
{'max_price': 899.99, 'category': 'phones'}

==================================================
avg_price_good_rating:
==================================================
673.7970370370371

==================================================
brand_products:
==================================================
{'title': 'Apple MacBook Air 13"'}
{'title': 'Apple MacBook Pro 13" Space Gray'}
{'title': 'Apple MacBook Air 13"'}
{'title': 'Apple iPad Air'}
{'title': 'Samsung Galaxy'}

==================================================
value_ranking:
==================================================
{'title': 'Nokia 123', 'score': 12.004801920768308}
{'title': 'LG Optimus', 'score': 5.173305742369374}
{'title': 'IdeaTab A3500L', 'score': 4.494887065962468}
{'title': 'Lenovo IdeaTab', 'score': 4.286326618088299}
{'title': 'Asus MeMO Pad', 'score': 3.883872220603942}
... et 5 autres

==================================================
price_ranges:
==================================================
{'_id': 0, 'number_of_products': 18}
{'_id': 200, 'number_of_products': 44}
{'_id': 500, 'number_of_products': 20}
{'_id': 1000, 'number_of_products': 65}

==================================================
same_price_products:
==================================================
{'_id': {'price': 899.99}, 'nb_occurrences': 3}
{'_id': {'price': 1199.0}, 'nb_occurrences': 2}
{'_id': {'price': 436.29}, 'nb_occurrences': 2}
{'_id': {'price': 1769.0}, 'nb_occurrences': 2}
{'_id': {'price': 399.99}, 'nb_occurrences': 2}
... et 6 autres

---

### Exercice 3 : Opérations MinIO

**Objectif** : Manipuler le stockage objet.

Créez le fichier `exercises/ex3_minio_operations.py` :

-> J'ai placé le fichier `ex3_minio_operations.py` à la racine du porjet en raison des imports.

```python
"""
Exercice 3 : Opérations MinIO

Complétez les fonctions TODO.
"""

import io
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from config import minio_config
from PIL import Image
from src.storage import MinIOStorage, MongoDBStorage

DIR_PATH = Path(__file__).parent.resolve()


def create_thumbnails(minio: MinIOStorage, list_filenames: dict) -> int:
    """Crée un thumbnail pour chaque image de produit"""
    thumbnails_created = 0
    for filename in list_filenames:
        image_byte = minio.get_object(
            bucket=minio_config.bucket_images, filename=filename
        )

        # Load byte object
        pil_image = Image.open(io.BytesIO(image_byte))
        pil_image.thumbnail((100, 100))

        # Pillow Image object to byte
        thumbnail_byte = io.BytesIO()
        pil_image.save(thumbnail_byte, format="PNG")
        thumbnail_byte = thumbnail_byte.getvalue()

        # Upload thumbnail image
        thumbnail_filename = "thumbnail/" + filename
        minio.upload_image(image_data=thumbnail_byte, filename=thumbnail_filename)

        thumbnails_created += 1
    return thumbnails_created


def exercise_3():
    minio = MinIOStorage()
    mongo = MongoDBStorage()

    # 3.1 Listez toutes les images et calculez la taille totale
    list_objects = minio.list_objects(bucket=minio_config.bucket_images)
    total_images = len(list_objects)
    total_size_kb = sum([object_info["size"] for object_info in list_objects])

    # 3.2 Créez des thumbnails (100x100) pour toutes les images
    # Stockez-les dans le même bucket avec préfixe "thumbnails/"
    # Indice: Utilisez PIL (Pillow)
    thumbnails_created = 0
    # list_filenames = [object_info["name"] for object_info in list_objects]
    # thumbnails_created = create_thumbnails(minio=minio, list_filenames=list_filenames)

    # 3.3 Générez une URL présignée (24h) pour l'image du produit le plus cher
    pipeline = [{"$sort": {"price": -1}}, {"$limit": 1}]
    product_most_expensive = list(mongo.products.aggregate(pipeline))[0]
    filename_product_most_expensive = "/".join(
        [
            product_most_expensive["category"],
            product_most_expensive["sub_category"],
            product_most_expensive["id_product"],
            ".jpeg",
        ]
    )
    presigned_url = minio.get_presigned_url(
        bucket=minio_config.bucket_images,
        filename=filename_product_most_expensive,
        expires_hours=24,
    )

    # 3.4 Créez un rapport JSON avec les stats de chaque catégorie d'images
    # et uploadez-le dans le bucket exports
    # Format: {"laptops": {"count": X, "size_kb": Y}, ...}
    objects_infos = deepcopy(list_objects)

    # Ajout d'information à partir du filename: thumbnail image, category et sub_category
    sub_categories = []
    for k in range(len(objects_infos)):
        filename = objects_infos[k]["name"]
        filename_split = filename.split("/")
        if "thumbnail" in filename_split:
            objects_infos[k]["thumbnail"] = True
            objects_infos[k]["category"] = filename_split[1]
            objects_infos[k]["sub_category"] = filename_split[2]
        else:
            objects_infos[k]["thumbnail"] = False
            objects_infos[k]["category"] = filename_split[0]
            objects_infos[k]["sub_category"] = filename_split[1]
        sub_categories.append(objects_infos[k]["sub_category"])

    # Liste des sub_categories
    dictincts_sub_categories = list(set(sub_categories))

    # Images originales
    original_objects_infos = [
        object_info for object_info in objects_infos if object_info["thumbnail"]
    ]

    stats_report = {}
    for sub_category in dictincts_sub_categories:
        sub_category_objects_infos = [
            object_info
            for object_info in original_objects_infos
            if object_info["sub_category"] == sub_category
        ]
        stats_report.update(
            {
                sub_category: {
                    "count": len(sub_category_objects_infos),
                    "size": sum(
                        [
                            sub_category_object_info["size"]
                            for sub_category_object_info in sub_category_objects_infos
                        ]
                    ),
                }
            }
        )

        # Upload bucket export
        stats_report_byte = json.dumps(stats_report, indent=4).encode("utf-8")
        filename_report = (
            "stats_report_" + datetime.now().strftime("%Y%m%dT%H%M%S") + ".json"
        )
        minio.upload_export(data=stats_report_byte, filename=filename_report)

    # 3.5 Implémentez une fonction qui copie toutes les images
    # vers un nouveau bucket "backup-YYYYMMDD"
    for object_info in list_objects:
        filename: str = object_info["name"]
        image_byte = minio.get_object(
            bucket=minio_config.bucket_images, filename=filename
        )
        minio.create_backup(data=image_byte, prefix=filename.replace(".jpeg", ""))
    backup_created = True

    mongo.close()

    return {
        "total_images": total_images,
        "total_size_kb": total_size_kb,
        "thumbnails_created": thumbnails_created,
        "presigned_url": presigned_url,
        "stats_report": stats_report,
        "backup_created": backup_created,
    }


if __name__ == "__main__":
    results = exercise_3()

    for name, result in results.items():
        print(f"{name}: {result}")
```

-> Affichage console :

===========================
total_images: 147
total_size_kb: 1848819
thumbnails_created: 147
presigned_url: [None](http://localhost:9000/products-images/computers/laptops/3957b46edf0c11f0901a908d6e62deca/.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20251222%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251222T094027Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=884a29a5b8e2f2b068c00799d095da5e4a99648b8718747f656e4301a2dd234a)
stats_report: {'tablets': {'count': 21, 'size': 187278}, 'touch': {'count': 9, 'size': 80262}, 'laptops': {'count': 117, 'size': 1043406}}
backup_created: False
===========================

---

