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

- A Compléter

---

## Partie 1 : Exploration du Site Cible 

### 1.1 Découverte de la structure

Avant de coder, explorez manuellement le site : https://webscraper.io/test-sites/e-commerce/allinone

**Questions à résoudre :**

1. Quelles sont les catégories de produits disponibles ?
2. Comment fonctionne la pagination ?
3. Quelles informations sont disponibles sur la page liste vs page détail ?
4. Où se trouvent les images des produits ?

### 1.2 Analyse de la structure HTML



### 1.3 Exercice préparatoire

Complétez le tableau suivant en inspectant le HTML :

| Donnée | Sélecteur CSS | Exemple de valeur |
|--------|---------------|-------------------|
| Titre du produit |  | |
| Prix | | |
| Description | | |
| Rating (étoiles) | | |
| URL de l'image | | |
| Lien vers détails | | |

---

## Partie 2 : Infrastructure Docker 

### 2.1 Structure du projet

Créez l'arborescence du projet.


### 2.2 Docker Compose

Créez le fichier `docker-compose.yml` pour le projet.



### 2.3 Dépendances Python

Créez le fichier `requirements.txt`.



### 2.4 Configuration

Créez les fichiers de configuration.


---

## Partie 3 : Clients de Stockage

### 3.1 Client MinIO

### 3.2 Client MongoDB



---

## Partie 4 : Scraper E-Commerce 

### 4.1 Scraper principal


---

## Partie 5 : Pipeline Intégré

### 5.1 Pipeline principal



---

## Partie 6 

### Exercice 1 : Validation de l'infrastructure 

**Questions à répondre :**

1. Combien de produits ont été scrapés ?
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

