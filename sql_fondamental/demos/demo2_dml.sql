----------- INSERTION -----------

-- Pour insérer une valeur dans un table, nous utilisons la commande INSERT INTO
INSERT INTO demo_dml.services (libelle)
VALUES ('comptabilité');

-- Pour insérer plusieurs valeurs d'un coup
INSERT INTO demo_dml.services (libelle, date_creation)
VALUES 
	('RH', '2025-11-19'), 
	('Informatique', '2025-01-01');

-- Format timestamp (date-heure) : AAAA-MM-JJ HH:mm:SS

----------- MISE A JOUR -----------
-- Pour mettre à jour une ou plusieurs lignes de notre table, nous utiliserons le mot-clé UPDATE suivie de SET.
UPDATE
	demo_dml.services
SET 
	libelle = 'Comptabilite'
WHERE
	service_id = 1; 

-- Pour mettre plusieurs attribut à jour en même, il suffit de les préciser dans le SET séparé par des ","
UPDATE
	demo_dml.services
SET 
	libelle = 'Ressources humaines',
	date_creation = '1990-10-10'
WHERE
	service_id = 2; 

-- Si l'on souhaite récupérer la/les lignes qui ont été modifiées nous pouvons ajouter le mot-clé RETURNING.
UPDATE
	demo_dml.services
SET 
	libelle = 'Recherche et Developement'
WHERE
	service_id = 4
RETURNING *; 

----------- SUPPRESSION -----------
-- Supprimer un élément par son id
DELETE FROM
	demo_dml.services
WHERE
	service_id = 2;

-- Nous pouvons récupérer les enregistrements avant qu'ils ne soient supprimés.
DELETE FROM
	demo_dml.services
WHERE
	date_creation < '2024-01-01'
RETURNING *;

-- Supprimer tous les enregistrements
DELETE FROM
	demo_dml.services;

-- Réinitialise la table en supprimant tous les enregistrements
-- Méthode plus optimisé que DELETE mais aucun retour en arrière possible.
TRUNCATE 
	demo_dml.services RESTART IDENTITY CASCADE;
