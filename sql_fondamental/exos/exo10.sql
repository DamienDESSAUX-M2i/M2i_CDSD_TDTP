-- Question 1
-- Les 10 villes les plus peuplées en 2012 sont :
-- "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"
SELECT ville_nom_reel, ville_population_2012
FROM villes_france_free
ORDER BY ville_population_2012 DESC
LIMIT 10;

-- Question 2
SELECT ville_nom_reel, ville_surface
FROM villes_france_free
ORDER BY ville_surface ASC
LIMIT 50;

-- Question 3
SELECT ville_nom_reel
FROM villes_france_free
WHERE ville_departement LIKE '97%';

-- Question 4
SELECT v.ville_departement, d.departement_nom, v.ville_nom_reel, v.ville_population_2012
FROM villes_france_free AS v
LEFT JOIN departement AS d
ON v.ville_departement = d.departement_code
ORDER BY ville_population_2012 DESC

-- Question 5
SELECT d.departement_code, d.departement_nom, COUNT(v.ville_nom) AS nb_villes
FROM departement AS d
LEFT JOIN villes_france_free AS v
ON v.ville_departement = d.departement_code
GROUP BY d.departement_code, d.departement_nom
ORDER BY COUNT(v.ville_nom) DESC;

-- Question 6
SELECT d.departement_nom, SUM(v.ville_surface) AS sum_villes_surfaces
FROM departement AS d
LEFT JOIN villes_france_free AS v
ON d.departement_code = v.ville_departement
GROUP BY d.departement_nom
HAVING SUM(v.ville_surface) IS NOT NULL
ORDER BY SUM(v.ville_surface) DESC
LIMIT 10;

-- Question 7
SELECT COUNT(ville_nom) AS nb_villes_saint
FROM villes_france_free
WHERE ville_nom ILIKE 'saint%';

-- Question 8
-- SAINTE-COLOMBE est le nom de commune le plus fréquent.
SELECT ville_nom, COUNT(ville_nom) AS nb_occurrences
FROM villes_france_free
GROUP BY ville_nom
HAVING COUNT(ville_nom) > 1
ORDER BY COUNT(ville_nom) DESC
LIMIT 1;

-- Question 9
SELECT ville_nom, ville_surface
FROM villes_france_free
WHERE ville_surface > (
    SELECT AVG(ville_surface)
    FROM villes_france_free
);

-- Question 10
-- Les départements ayant plus de 2M d'habitants sont Paris et Nord
SELECT d.departement_nom, SUM(v.ville_population_2012) AS population_total
FROM departement AS d
LEFT JOIN villes_france_free AS v
ON d.departement_code = v.ville_departement
GROUP BY d.departement_nom
HAVING SUM(v.ville_population_2012) > 2000000;

-- Question 11
UPDATE villes_france_free
SET ville_nom = REPLACE(ville_nom, '-', ' ');