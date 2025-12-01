-- ================================================================
-- DEMO AGRÉGATS - Université
-- Pré-requis : demo_universite_schema.sql
--
-- Objectifs pédagogiques :
--  - Comprendre le rôle d'une fonction d'agrégat
--  - Voir les fonctions d'agrégat de base :
--      * COUNT
--      * SUM
--      * AVG
--      * MIN
--      * MAX
--  - Comprendre GROUP BY et HAVING
--  - Combiner agrégats + JOIN
-- ================================================================


-- ================================================================
-- Étape 1 - COUNT(*) : compter des lignes
-- Objectif :
--   Compter le nombre total d'étudiants.
--   COUNT(*) compte toutes les lignes, même si certaines colonnes sont NULL.
-- ================================================================
SELECT
    COUNT(*) AS nb_etudiants
FROM students;

-- ================================================================
-- Étape 2 - COUNT(colonne) : compter les valeurs non NULL
-- Objectif :
--   Count sur une colonne ignore les NULL.
--   Ici : compter le nombre de notes déjà attribuées.
-- ================================================================
SELECT
    COUNT(grade) AS nb_notes_attribuees
FROM enrollments;


-- ================================================================
-- Étape 3 - MIN / MAX : valeurs extrêmes
-- Objectif :
--   Trouver la plus petite et la plus grande note attribuée.
-- ================================================================
SELECT
    MIN(grade) AS note_min,
    MAX(grade) AS note_max
FROM enrollments
WHERE grade IS NOT NULL;

-- ================================================================
-- Étape 4 - AVG : moyenne
-- Objectif :
--   Calculer la moyenne de toutes les notes.
--   Remarque : AVG ignore les NULL, donc pas besoin de les filtrer,
--   mais on peut le faire pour être explicite.
-- ================================================================
SELECT
    AVG(grade)       AS moyenne_brute,
    ROUND(AVG(grade), 2) AS moyenne_arrondie
FROM enrollments
WHERE grade IS NOT NULL;

-- ================================================================
-- Étape 5 - SUM : somme
-- Objectif :
--   Exemple simple : total de tous les ECTS des cours.
--   SUM additionne les valeurs numériques.
-- ================================================================
SELECT
    SUM(ects) AS total_ects
FROM courses;

-- ================================================================
-- Étape 6 - DISTINCT + agrégats
-- Objectif :
--   Combiner DISTINCT avec COUNT pour compter les valeurs distinctes.
--   Exemple :
--     - nombre de programmes différents
--     - nombre de villes différentes
-- ================================================================
SELECT
    COUNT(DISTINCT program) AS nb_programmes_distincts,
    COUNT(DISTINCT city)    AS nb_villes_distinctes
FROM students;

-- ================================================================
-- Étape 7 - GROUP BY : agrégats par groupe
-- Objectif :
--   Compter le nombre d'étudiants par ville.
--   GROUP BY crée un groupe par valeur de city,
--   puis on applique les fonctions d'agrégat par groupe.
-- ================================================================
SELECT
    city,
    COUNT(*) AS nb_etudiants
FROM students
GROUP BY city
ORDER BY nb_etudiants DESC, city;

-- ================================================================
-- Étape 8 - Plusieurs agrégats sur un même groupe
-- Objectif :
--   Exemple : statistiques de notes par cours :
--     - nombre de notes
--     - note min, max
--     - moyenne
-- ================================================================
SELECT
    c.title                        AS course_title,
    COUNT(e.grade)                 AS nb_notes,
    MIN(e.grade)                   AS note_min,
    MAX(e.grade)                   AS note_max,
    ROUND(AVG(e.grade), 2)         AS note_moy
FROM courses     AS c
JOIN enrollments AS e
    ON e.course_id = c.course_id
WHERE e.grade IS NOT NULL
GROUP BY c.title
ORDER BY note_moy DESC;

-- ================================================================
-- Étape 9 - SUM + GROUP BY : total ECTS par enseignant
-- Objectif :
--   Monter un exemple de SUM groupé :
--   somme des crédits (ECTS) des cours d'un enseignant.
-- ================================================================
SELECT
    t.full_name AS teacher_name,
    SUM(c.ects) AS total_ects
FROM teachers AS t
JOIN courses  AS c
    ON c.teacher_id = t.teacher_id
GROUP BY t.full_name
ORDER BY total_ects DESC, teacher_name;

-- ================================================================
-- Étape 10 - HAVING : filtrer sur les agrégats
-- Objectif :
--   Différence entre WHERE et HAVING :
--     - WHERE filtre les lignes avant l'agrégat
--     - HAVING filtre les groupes après l'agrégat
--
--   Exemple :
--     Afficher seulement les cours dont la moyenne >= 15.
-- ================================================================
SELECT
    c.title                AS course_title,
    ROUND(AVG(e.grade), 2) AS note_moy
FROM courses     AS c
JOIN enrollments AS e
    ON e.course_id = c.course_id
WHERE e.grade IS NOT NULL
GROUP BY c.title
HAVING AVG(e.grade) >= 15
ORDER BY note_moy DESC;


-- ================================================================
-- Étape 11 - Agrégats par étudiant : moyenne individuelle
-- Objectif :
--   Calculer la moyenne de chaque étudiant.
--   Intérêt pédagogique :
--     Combiner JOIN + GROUP BY + plusieurs agrégats.
-- ================================================================
SELECT
    s.full_name           AS student_name,
    s.program,
    COUNT(e.grade)        AS nb_notes,
    ROUND(AVG(e.grade), 2) AS moyenne
FROM students    AS s
JOIN enrollments AS e
    ON e.student_id = s.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.full_name, s.program
ORDER BY moyenne DESC;