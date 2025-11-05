# Créez un volume nommé pgdata_exercice
docker volume create pgdata_exercice
docker volume ls # local pgdata_exercice

# Lancez un conteneur PostgreSQL en utilisant le volume pgdata_exercice
docker search postgres # postgres 6> Official
docker pull postgres
docker inspect postgres # chemin volume : /var/lib/postgresql
docker run -d -v pgdata_exercice:/var/lib/postgresql --name pgsql1 -e POSTGRES_PASSWORD=admin postgres

# Entrer dans le conteneur :
docker exec -it pgsql1 bash

# Accéder à PostgreSQL :
psql -U postgres

# Créer une base de données school :
CREATE DATABASE school;

# Se connecter à la base de données school : (\c [nom_bdd])
\c school

# Créer une table students :
CREATE TABLE students(
    id SERIAL PRIMERY KEY,
    name VARCHAR(255),
    age INT
);

# Insérer des données dans la table students :
## id auto-généré
INSERT INTO students(name, age) VALUES("Damien", 32);

# Vérifier que les données ont été insérées :
SELECT * FROM students;

# Sortir de PostgreSQL et du conteneur :
\q # quitter terminal postgres
exit # quitter terminal bash
# CTRL+Z quitter conteneur

# Arrêter le conteneur :
docker stop pgsql1

# Supprimer le conteneur
docker rm pgsql

# Recréer un nouveau conteneur avec le volume pgdata_exercice :
docker run -d -v pgdata_exercice:/var/lib/postgresql --name pgsql2 -e POSTGRES_PASSWORD=admin postgres

# Entrer dans le conteneur :
docker exec -it pgsql2 bash

# Accéder à PostgreSQL :
psql -U postgres

# Se connecter à la base de données school :
\c school

# Vérifier que les données sont toujours présentes :
SELECT * FROM students;