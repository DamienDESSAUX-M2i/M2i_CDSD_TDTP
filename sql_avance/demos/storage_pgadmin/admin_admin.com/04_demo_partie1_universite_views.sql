-- ================================================================
-- DEMO VUES - Université
-- Pré-requis : demo_universite_schema.sql
--
-- Objectifs pédagogiques :
--  - Comprendre ce qu'est une vue :
--      * une requête SELECT enregistrée sous un nom
--  - Créer différents types de vues :
--      * vue simple (projection / filtre)
--      * vue basée sur des JOIN
--      * vue avec agrégats
--  - Montrer comment réutiliser une vue dans d'autres requêtes
-- ================================================================


-- ================================================================
-- Étape 1 - Vue simple de projection
-- Objectif :
--   Créer une vue qui expose seulement une partie des colonnes.
--   Exemple : liste des étudiants avec un alias “propre”.
-- ================================================================
CREATE OR REPLACE VIEW v_students_basic AS
SELECT
    student_id,
    full_name      AS student_name,
    program,
    city
FROM students;

-- Utilisation : on interroge la vue comme une table.
SELECT *
FROM v_students_basic
ORDER BY student_id;

-- ================================================================
-- Étape 2 - Vue avec filtre
-- Objectif :
--   Enregistrer une sélection filtrée dans une vue.
--   Exemple :
--     On veut souvent consulter uniquement les étudiants de Master (M1/M2).
-- ================================================================
CREATE OR REPLACE VIEW v_master_students AS
SELECT
    student_id,
    full_name      AS student_name,
    program,
    city
FROM students
WHERE program LIKE 'M%';

-- Utilisation : afficher tous les étudiants en Master
SELECT *
FROM v_master_students
ORDER BY program, student_name;

-- ================================================================
-- Étape 3 - Vue basée sur des JOIN (vue “résultats étudiants”)
-- Objectif :
--   Encapsuler un JOIN complexe dans une vue réutilisable.
--   On y met :
--     - étudiant
--     - cours
--     - enseignant
--     - note
-- ================================================================
CREATE OR REPLACE VIEW v_student_results AS
SELECT
    e.enrollment_id,
    s.student_id,
    s.full_name      AS student_name,
    s.program,
    c.course_id,
    c.title          AS course_title,
    t.teacher_id,
    t.full_name      AS teacher_name,
    t.department,
    e.grade
FROM enrollments AS e
JOIN students    AS s
    ON s.student_id = e.student_id
JOIN courses     AS c
    ON c.course_id = e.course_id
JOIN teachers    AS t
    ON t.teacher_id = c.teacher_id;

    -- Utilisation : lire les résultats comme si c'était une table "flattened"
SELECT *
FROM v_student_results
ORDER BY student_name, course_title;


-- ================================================================
-- Étape 4 - Vue d'agrégats par cours
-- Objectif :
--   Créer une vue “table de statistiques” par cours :
--     - nombre d'inscriptions
--     - nombre de notes
--     - moyenne
-- ================================================================
CREATE OR REPLACE VIEW v_course_stats AS
SELECT
    c.course_id,
    c.title          AS course_title,
    t.full_name      AS teacher_name,
    t.department,
    COUNT(e.enrollment_id) AS nb_inscriptions,
    COUNT(e.grade)         AS nb_notes,
    ROUND(AVG(e.grade), 2) AS avg_grade
FROM courses     AS c
LEFT JOIN enrollments AS e
    ON e.course_id = c.course_id
JOIN teachers    AS t
    ON t.teacher_id = c.teacher_id
GROUP BY c.course_id, c.title, t.full_name, t.department;

-- Utilisation 1 : voir toutes les stats de cours
SELECT *
FROM v_course_stats
ORDER BY course_title;

-- Utilisation 2 : ne voir que les cours avec moyenne >= 15
SELECT *
FROM v_course_stats
WHERE avg_grade IS NOT NULL
  AND avg_grade >= 15
ORDER BY avg_grade DESC;


-- ================================================================
-- Étape 5 - Vue d'agrégats par étudiant (moyenne générale)
-- Objectif :
--   Résumer la performance de chaque étudiant dans une vue.
--   On pourra ensuite réutiliser cette vue dans d'autres requêtes.
-- ================================================================
CREATE OR REPLACE VIEW v_student_avg_grade AS
SELECT
    s.student_id,
    s.full_name           AS student_name,
    s.program,
    ROUND(AVG(e.grade), 2) AS avg_grade,
    COUNT(e.grade)         AS nb_notes
FROM students    AS s
JOIN enrollments AS e
    ON e.student_id = s.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.student_id, s.full_name, s.program;

-- Utilisation 1 : classement des étudiants
SELECT *
FROM v_student_avg_grade
ORDER BY avg_grade DESC;

-- Utilisation 2 : filtrer les étudiants avec au moins 3 notes
SELECT *
FROM v_student_avg_grade
WHERE nb_notes >= 3
ORDER BY avg_grade DESC;


-- ================================================================
-- Étape 6 - Réutiliser une vue dans une autre requête
-- Objectif :
--   Montrer qu'une vue est une "brique" qu'on peut composer.
--   Exemple :
--     moyenne des étudiants par ville,
--     en s'appuyant sur v_student_avg_grade.
-- ================================================================
SELECT
    s.city,
    ROUND(AVG(v.avg_grade), 2) AS avg_grade_par_ville,
    COUNT(*)                   AS nb_etudiants
FROM v_student_avg_grade AS v
JOIN students            AS s
    ON s.student_id = v.student_id
GROUP BY s.city
ORDER BY avg_grade_par_ville DESC;