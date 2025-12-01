-- ================================================================
-- DEMO JOINS - Université
-- Pré-requis : exécuter d'abord demo_universite_schema.sql
--
-- Objectifs pédagogiques :
--  - Comprendre ce qu'est un JOIN et pourquoi on en a besoin
--  - Voir les différents types de JOIN :
--      * INNER JOIN
--      * LEFT JOIN
--      * RIGHT JOIN
--      * FULL OUTER JOIN
--      * CROSS JOIN
--      * SELF JOIN
--  - Apprendre à lire une requête avec plusieurs JOIN
-- ================================================================


-- ================================================================
-- Étape 0 - Rappel : SELECT sans JOIN
-- Objectif :
--   Montrer les limites d'une seule table.
--   Ici : on voit les étudiants, mais aucun cours ni note.
-- ================================================================
SELECT
    student_id,
    full_name,
    program,
    city
FROM students
ORDER BY student_id;

-- ================================================================
-- Étape 1 - INNER JOIN (2 tables)
-- Objectif :
--   Relier deux tables par une clé étrangère.
--   Ici :
--     enrollments.student_id -> students.student_id
--   On obtient : inscriptions + nom de l'étudiant.
--   Remarque :
--     INNER JOIN = ne garde que les lignes qui ont une correspondance
--     dans les deux tables.
-- ================================================================
SELECT
    e.enrollment_id,
    s.full_name      AS student_name,
    s.program,
    e.course_id,
    e.grade
FROM enrollments AS e
INNER JOIN students AS s
    ON s.student_id = e.student_id
ORDER BY e.enrollment_id;


-- ================================================================
-- Étape 2 - INNER JOIN (3 tables)
-- Objectif :
--   Ajouter une 3e table au JOIN :
--     enrollments -> courses pour récupérer le titre du cours.
--   On obtient : étudiant + cours + note.
-- ================================================================
SELECT
    s.full_name      AS student_name,
    s.program,
    c.title          AS course_title,
    e.grade
FROM enrollments AS e
INNER JOIN students AS s
    ON s.student_id = e.student_id
INNER JOIN courses AS c
    ON c.course_id = e.course_id
ORDER BY s.full_name, c.title;

-- ================================================================
-- Étape 3 - INNER JOIN (4 tables)
-- Objectif :
--   Ajouter encore une table :
--     courses.teacher_id -> teachers.teacher_id
--   On obtient : étudiant + cours + enseignant + note.
--   Intérêt pédagogique :
--     Montrer qu'on peut "enchaîner" les JOIN autant que nécessaire.
-- ================================================================
SELECT
    s.full_name      AS student_name,
    c.title          AS course_title,
    t.full_name      AS teacher_name,
    t.department,
    e.grade
FROM enrollments AS e
INNER JOIN students AS s
    ON s.student_id = e.student_id
INNER JOIN courses AS c
    ON c.course_id = e.course_id
INNER JOIN teachers AS t
    ON t.teacher_id = c.teacher_id
ORDER BY t.department, t.full_name, s.full_name, c.title;

-- ================================================================
-- Étape 4 - LEFT JOIN
-- Objectif :
--   Voir la différence avec INNER JOIN.
--   LEFT JOIN = on garde TOUTES les lignes de la table de gauche,
--   même si aucune correspondance à droite.
--
--   Exemple :
--     Liste des cours, y compris ceux sans inscription.
-- ================================================================
SELECT
    c.course_id,
    c.title,
    COUNT(e.enrollment_id) AS nb_inscriptions
FROM courses AS c
LEFT JOIN enrollments AS e
    ON e.course_id = c.course_id
GROUP BY c.course_id, c.title
ORDER BY c.course_id;



-- ================================================================
-- Étape 5 - RIGHT JOIN
-- Objectif :
--   Montrer RIGHT JOIN, qui est l'inverse du LEFT JOIN :
--   on garde toutes les lignes de la table de droite.
--
--   Exemple pédagogique :
--     C'est rarement indispensable si on sait permuter les tables,
--     mais utile pour comprendre la symétrie avec LEFT JOIN.
-- ================================================================
SELECT
    c.course_id,
    c.title,
    COUNT(e.enrollment_id) AS nb_inscriptions
FROM enrollments AS e
RIGHT JOIN courses AS c
    ON e.course_id = c.course_id
GROUP BY c.course_id, c.title
ORDER BY c.course_id;

-- ================================================================
-- Étape 6 - FULL OUTER JOIN
-- Objectif :
--   FULL OUTER JOIN = garde toutes les lignes des deux côtés,
--   même s'il n'y a pas de correspondance.
--
--   Exemple (purement démonstratif) :
--     Mettre en face les cours et les inscriptions, même si
--     un côté n'a pas de correspondance.
--   Intérêt :
--     Montrer que certaines colonnes seront NULL d'un côté ou de l'autre.
-- ================================================================
SELECT
    c.course_id,
    c.title,
    e.enrollment_id,
    e.student_id,
    e.grade
FROM courses AS c
FULL OUTER JOIN enrollments AS e
    ON e.course_id = c.course_id
ORDER BY c.course_id, e.enrollment_id;

-- ================================================================
-- Étape 7 - CROSS JOIN
-- Objectif :
--   CROSS JOIN = produit cartésien entre deux tables.
--   => toutes les combinaisons possibles des lignes.
--
--   Exemple :
--     On veut générer toutes les combinaisons (programme, département)
--     pour illustrer le concept (à ne pas faire sur de très grandes tables).
-- ================================================================
SELECT
    s.program,
    t.department
FROM students AS s
CROSS JOIN teachers AS t
ORDER BY s.program, t.department;

-- ================================================================
-- Étape 8 - SELF JOIN
-- Objectif :
--   SELF JOIN = une table jointe avec elle-même.
--
--   Exemple :
--     Mettre en relation deux enseignants du même département.
--     On crée deux alias de la table teachers.
-- ================================================================
SELECT
    t1.full_name AS teacher_1,
    t2.full_name AS teacher_2,
    t1.department
FROM teachers AS t1
INNER JOIN teachers AS t2
    ON t1.department = t2.department
   AND t1.teacher_id < t2.teacher_id
ORDER BY t1.department, teacher_1, teacher_2;