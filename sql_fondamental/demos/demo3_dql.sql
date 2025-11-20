SET search_path TO 'demo_dql', '$user', 'public';

-- Sélectionner toutes les colonnes
SELECT * FROM services;

-- Sélectionner des colonnes spécifiques dans le SELECT
SELECT
	libelle,
	date_creation
FROM services; 

-- Alias pour les colonnes
SELECT
	libelle AS nom_service,
	date_creation AS creation
FROM
	services;

-- Alias sur les tables
SELECT
	s.libelle,
	s.date_creation
FROM
	services AS s;

INSERT INTO services (libelle)
VALUES ('RD'), ('Managment');

INSERT INTO employes (prenom, nom, age, salaire, service_id)
VALUES
	('Jean', 'Dupont', 30, 1400, 1), 
	('Michelle', 'Dufour', 29, 2800, 2), 
	('Geralt', 'De rive', 24, 1500, 4), 
	('Jasquier', 'Dandelion', 41, 2100, 5), 
	('John', 'Doe', 52, 2000, 1), 
	('Jane', 'Does', 44, 3000, 2), 
	('Joe', 'Dalton', 25, 2040, 4), 
	('Avrel', 'Dalton', 20, 1700, 5);

-- Récupére l'ensemble des employés.
SELECT * FROM employes; 

-- Lectures sur plusieurs
-- A éviter à tout pris, et préférer l'utilisation des joitures.
SELECT *
FROM employes, services;

-- La clause Where permet de filtrer les résultats de la requête.
SELECT prenom, nom
FROM employes
WHERE service_id = 1;

-- LENGTH permet de récuperer le nombre de caractere
SELECT prenom, nom
FROM employes
WHERE service_id = 1 AND LENGTH(nom) > 4;

SELECT prenom, nom, age, salaire
FROM employes
WHERE salaire > 2000 OR (age < 30 AND service_id <> 1); 

-- LIKE permet d'effectuer une recherche sur une partie d'une chaine de caractere
SELECT *
FROM employes
WHERE prenom LIKE 'J%';

SELECT *
FROM employes
WHERE prenom ILIKE 'J___';

SELECT *
FROM employes
WHERE prenom ILIKE '%g%';

-- Il est possible d'afficher des champs calculer directement dans le SELECT (Le AS va donner le nom de la colonne)
SELECT prenom, salaire, salaire * 1.10 AS salaire_augmente
FROM employes;

-- BETWEEN permet de faire une recherche sur une plage de valeur
SELECT prenom, nom, salaire
FROM employes
WHERE salaire BETWEEN 2000 AND 3000;

-- IN permet d'effectuer une recherche parmis plusieurs réponse possible
SELECT prenom, nom, service_id
FROM employes
WHERE service_id IN (1, 2);

-- ORDER BY
-- Permet d'ordonner le jeu de résultat par rapport à une ou plusieurs colonnes
-- de manière croissante (ASC) ou décroissante (DESC)
-- Par défaut: ASC, pas besoin de le préciser
SELECT *
FROM employes
ORDER BY prenom;
 
SELECT prenom, salaire
FROM employes
ORDER BY salaire DESC;

-- LIMIT
-- Permet de limiter le nombre de résultats obtenus
SELECT prenom, salaire
FROM employes
ORDER BY salaire DESC
LIMIT 3;

-- OFFSET permet de décaler le jeu d'enregistrement que l'on récupère
SELECT DISTINCT service_id
FROM employes
LIMIT 2
OFFSET 2;

INSERT INTO
 employes
 (prenom, nom, salaire, "age", service_id)
VALUES
 ('Jean', 'Dupontax', 1500, 38, 2);
 
-- DISTINCT
-- Permet de supprimer les doublons d'un jeu de resultats
SELECT DISTINCT prenom
FROM employes;

-- GROUP BY et Fonctions d'agrégations

-- Salaire max parmis les salariés
SELECT MAX(salaire) AS salaire_max
FROM employes;

-- Salaire moyen par service
SELECT ROUND(AVG(salaire)) AS salaire_moyen, service_id
FROM employes
GROUP BY service_id
ORDER BY salaire_moyen DESC;

-- On sélectionne les salaires moyen par service supérieur à 2000€
SELECT ROUND(AVG(salaire)) AS salaire_moyen, service_id
FROM employes
GROUP BY service_id
HAVING AVG(salaire) >= 1900
ORDER BY salaire_moyen DESC;
 
SELECT service_id, COUNT(*) AS nombre_salarie_par_service
FROM employes
GROUP BY service_id
ORDER BY nombre_salarie_par_service DESC, service_id;

SELECT EXTRACT(YEAR FROM date_creation) AS year, EXTRACT(MONTH FROM date_creation) AS month
FROM services 
GROUP BY year, month
ORDER BY year, month; 

