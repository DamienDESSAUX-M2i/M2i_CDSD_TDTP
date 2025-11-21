-- Question 1
-- La notion 'ESPRIT LIBERTÉ MATIÈRE RAISON' est abordé 3 fois.
SELECT COUNT(notions)
FROM sujets
WHERE notions ILIKE '%esprit%'
AND notions ILIKE '%libert_%'
AND notions ILIKE '%mati_re%'
AND notions ILIKE '%raison%';

-- Question 2
-- Le premier sujet abordé pour la série S en métropole est : La science nous livre-t-elle le réel tel qu'il est ?
SELECT *
FROM (
    -- Ensemble des sujets année=MIN(annee), série='S', lieu='métropole'
    SELECT *
    FROM sujets AS s1
    WHERE annee = (
        SELECT MIN(s2.annee)
        FROM sujets AS s2
    )
    AND s1.serie = 'S'
    AND s1.lieu ILIKE '%m_tropole%'
)
WHERE rang = (
    -- Le plus petit rang parmis l'ensemble des sujets année=MIN(annee), série='S', lieu='métropole'
    SELECT MIN(rang)
    FROM (
        SELECT *
        FROM sujets AS s1
        WHERE annee = (
            SELECT MIN(s2.annee)
            FROM sujets AS s2
        )
        AND s1.serie = 'S'
        AND s1.lieu ILIKE '%m_tropole%'
    )
);

-- Question 3
-- Les types de session sont 'REMPLACEMENT', 'SECOURS' et 'NORMALE'
SELECT DISTINCT session
FROM sujets;

-- Question 4
-- L'auteur le plus représenté dans les sujets est ROUSSEAU.
SELECT auteur, nb_occurrences
FROM (
    -- Table présentant les auteurs et le nombre d'occurrences de ces auteurs dans les sujets
    SELECT auteur, COUNT(auteur) AS nb_occurrences
    FROM sujets
    GROUP BY auteur
)
WHERE nb_occurrences = (
    -- Nombre maximal d'occurrences des auteurs dans les sujets
    SELECT MAX(nb_occurrences)
    FROM (
        SELECT auteur, COUNT(auteur) AS nb_occurrences
        FROM sujets
        GROUP BY auteur
    )
);

-- Question 5
-- Le lieu ayant eu le plus long sujet est 'métropole'.
SELECT lieu, LENGTH(sujet) AS nb_charactères
FROM sujets
WHERE LENGTH(sujet) = (
    -- Longueur maximale des sujets
    SELECT MAX(LENGTH(sujet))
    FROM sujets
);

-- Le sujet le plus court est 'Qui est artiste ?'.
SELECT sujet, LENGTH(sujet) AS nb_charactères
FROM sujets
WHERE LENGTH(sujet) = (
    -- Longueur minimale des sujets
    SELECT MIN(LENGTH(sujet))
    FROM sujets
);

-- Question 6
-- Taille moyenne des sujets par série :
-- S        481
-- STI AA   577
-- ES       484
-- STHR     1154
-- TECHN    572
-- L        502
-- TMD      594
SELECT serie, ROUND(AVG(LENGTH(sujet)))
FROM sujets
GROUP BY serie;

-- Question 7
-- 79 sujets ont un nombre d'occurrences supérieure à 1.
SELECT sujet
FROM (
    SELECT sujet, COUNT(sujet) AS nb_occurrences_sujet
    FROM sujets
    GROUP BY sujet
)
WHERE nb_occurrences_sujet > 1;

-- Question 8
SELECT lieu, annee, rang, session
FROM sujets
WHERE lieu ILIKE '%japon%'
ORDER BY annee, rang, session;

-- Question 9
-- Les 3 notions les plus abordées pour la série 'ES' entre 2000 et 2005 sont : 'art', 'liberté' et 'vérité'.
SELECT notions, COUNT(notions) AS nb_occurrences
FROM sujets
WHERE serie = 'ES'
AND annee BETWEEN 2000 AND 2005
GROUP BY notions
ORDER BY nb_occurrences DESC
LIMIT 3;

-- Question 10
SELECT
    CASE
        WHEN LENGTH(sujet) > 50 THEN CONCAT(SUBSTR(sujet, 1, 50), '[...]')
        ELSE sujet
    END AS sujet_tronque
FROM sujets;
