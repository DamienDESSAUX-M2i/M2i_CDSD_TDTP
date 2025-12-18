# Projet Data Analyst

## Démarrage

### Étape 1 : Lancer les bases de données

```bash
docker-compose up -d mongodb postgres
```

Attendre 15 secondes.

### Étape 2 : Générer les données Bronze

```bash
docker-compose up bronze_generator
```

Cela génère **20 000 documents** dans MongoDB :
- 5000 clients
- 15000 transactions  
- 200 campagnes marketing

### Étape 3 : Vérifier les données

```bash
mongosh mongodb://admin:admin123@localhost:27017

use bronze_db
db.customers.countDocuments()      // 5000
db.transactions.countDocuments()   // 15000
db.campaigns.countDocuments()      // 200
```

---

## Votre Mission

Consultez **SUJET.md** pour les instructions complètes.

**Vous devez créer :**
1. **Silver** : Script Python pour nettoyer et anonymiser les données
2. **Gold** : Script Python pour agréger et exporter vers PostgreSQL

---

## Connexions

**MongoDB**  
`mongodb://admin:admin123@localhost:27017`

**PostgreSQL**  
`postgresql://analyst:analyst123@localhost:5432/gold_db`

---

## Arrêter l'environnement

```bash
docker-compose down
```
