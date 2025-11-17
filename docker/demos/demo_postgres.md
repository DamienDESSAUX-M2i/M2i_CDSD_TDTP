## Pour se connecter à postgres 

```bash
docker run --name myps -e POSTGRES_PASSWORD=postgres

psql -U postgres
```

## Créer une BDD

```bash
CREATE DATABASE testdb; 
```

## Lister les BDD

```bash
\l
```

## Se connecter à une BDD 

```bash
\c testdb 
```

## Créer une table

```sql
CREATE TABLE person(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
); 
```

## Insérer une donnée dans la table

```sql
INSERT INTO person (name, age) VALUES ("Toto", 25) 
```

## Vérifier que les données ont été insérés 

```sql
SELECT * FROM person; 
```
