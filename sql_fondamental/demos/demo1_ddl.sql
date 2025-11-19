-- DDL : DATA DEFENITION LANGAGE
-- Pour faire un commentaire, on utilise deux "-" suivi d'un espace

-- Création d'une base de donnée
-- La création d'une base de donnée dans postgreSQL implique de créer une 
-- seconde connexion pour y accéder.
CREATE DATABASE demo1;

-- Suppression d'une base de donnée
DROP DATABASE demo1;

-- Ajout d'une commentaire sur une base de donnée
COMMENT ON DATABASE postgres IS 'base de données par défaut'

-- Créer un schéma (ensemble groupé de table)
CREATE SCHEMA demo;

-- Ne pas levé d'erreur si l'objet existe déjà
CREATE SCHEMA IF NOT EXISTS demo; 

-- Suppression du schéma
DROP SCHEMA demo;

---------------- CREATE TABLE ----------------

-- Pour créer une table, on utilise l'instruction CREATE TABLE
-- On peut vérifier que la table n'existe pas avant de la créer
-- Pour être sur de créer la table au bon endroit, on peut préfixer du schéma
CREATE TABLE IF NOT EXISTS demo.services (
	service_id SERIAL PRIMARY KEY,
	libelle VARCHAR(100) NOT NULL
);

-- Suppression d'une table si elle existe
DROP TABLE IF EXISTS demo.services; 

-- Créer un enum sql
CREATE TYPE secteur_enum AS ENUM ('INFO', 'GESTION', 'RD');

-- Créer une table avec des contraintes 
CREATE TABLE IF NOT EXISTS salarie (
	-- Fait la même chose que SERIAL, cad il utilise le méchanisme de séquence
	-- Respecte au mieux la convention SQL
    -- Mais il est nécessaire d'ajouter le contrainte de clé primaire.
	salarie_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
	-- On précise NOT NULL pour empécher l'absence de valeur
	prenom VARCHAR(50) NOT NULL,
	nom VARCHAR(50) NOT NULL,
	-- LA contrainte CHECK permet d'ajouter un mécanisme de vérification
	-- Les mots réservé du langage peuvent être noté entre guillemets
	"age" INT NOT NULL CHECK ("age" > 18 AND "age" < 70),
	status VARCHAR(50) NOT NULL CHECK (status IN ('STAGIAIRE', 'INTERIMAIRE', 'CDD', 'CDI')),
	secteur secteur_enum NOT NULL, 

	-- La contrainte DEFAULT qui permet de définir une valeur par défaut en cas d'absence de valeur renseignée.
	salaire DECIMAL(6, 2) DEFAULT 1500,
	service_id INT NOT NULL, 
	CONSTRAINT fk_service_id FOREIGN KEY (service_id) 
	REFERENCES services(service_id)
);

-- Modification d'une table
ALTER TABLE salarie
	RENAME TO salaries;

-- Suppression d'une contrainte
ALTER TABLE salaries
	DROP CONSTRAINT fk_service_id;

-- Ajouter une contrainte
ALTER TABLE salaries
	ADD CONSTRAINT fk_service_id
	FOREIGN KEY (service_id) REFERENCES services(service_id);

-- Ajout d'une colonne
ALTER TABLE salaries
	ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP; 

-- Modification d'un type de colonne
ALTER TABLE salaries
	ALTER COLUMN prenom TYPE VARCHAR(100);
