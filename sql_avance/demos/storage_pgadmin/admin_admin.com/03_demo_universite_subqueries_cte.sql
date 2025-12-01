-- ================================================================
-- MODULE 4 : SOUS-REQUÊTES & CTE (WITH)
-- Pré-requis : exécuter d'abord demo_universite_schema.sql
--
-- Objectifs pédagogiques :
--   - Comprendre ce qu'est une sous-requête (subquery)
--   - Voir les principaux types de sous-requêtes :
--        * sous-requête scalaire (renvoie une valeur)
--        * sous-requête avec IN
--        * sous-requête avec EXISTS
--        * sous-requête dans FROM (table dérivée)
--   - Comprendre ce qu'est un CTE (WITH) et pourquoi l'utiliser
--   - Réécrire certaines sous-requêtes avec WITH pour gagner en lisibilité
-- ================================================================


-- ================================================================
-- Étape 1 - Sous-requête scalaire dans SELECT
-- Objectif :
--   Ajouter une information "globale" à chaque ligne.
--   Ici : afficher, pour chaque étudiant, sa moyenne générale,
--   à côté de la moyenne générale de TOUTES les notes.
--
--   Question fréquente :
--     "Pourquoi utiliser une sous-requête plutôt qu'une jointure ici ?"
--   Réponse :
--     - La sous-requête scalaire est pratique pour calculer
--       une valeur globale (un seul résultat) et la répéter
--       sur chaque ligne du résultat principal.
-- ================================================================
SELECT
    s.student_id,
    s.full_name                          AS student_name,
    -- Sous-requête scalaire : moyenne globale de toutes les notes
    (
        SELECT ROUND(AVG(grade), 2)
        FROM enrollments
        WHERE grade IS NOT NULL
    )                                    AS global_avg_grade
FROM students AS s
ORDER BY s.student_id;


-- ================================================================
-- Étape 2 - Sous-requête scalaire corrélée : moyenne par étudiant
-- Objectif :
--   Faire dépendre la sous-requête de la ligne courante (correlation).
--   Ici : calculer la moyenne des notes de CHAQUE étudiant.
--
--   Remarque :
--     - La sous-requête référence s.student_id (corrélation).
--     - Fonctionnellement, ceci revient à un GROUP BY,
--       mais ici on illustre la notion de sous-requête corrélée.
-- ================================================================
SELECT
    s.student_id,
    s.full_name                          AS student_name,
    (
        SELECT ROUND(AVG(e.grade), 2)
        FROM enrollments AS e
        WHERE e.student_id = s.student_id
          AND e.grade IS NOT NULL
    )                                    AS avg_grade_for_student
FROM students AS s
ORDER BY student_name;



-- ================================================================
-- - Sous-requête dans FROM : table dérivée (subquery FROM)
-- Objectif :
--   Construire une "vue temporaire" dans la requête.
--   Exemple :
--     1) Dans la sous-requête : calculer des stats par cours
--     2) Dans la requête externe : filtrer / trier ces résultats
--
--   Question fréquente :
--     "En quoi est-ce différent d'une vue ?"
--   Réponse :
--     - Table dérivée : définie dans une seule requête, ponctuellement
--     - Vue : définie une fois pour toutes dans le schéma
-- ================================================================
SELECT
    cs.course_title,
    cs.nb_notes,
    cs.avg_grade
FROM (
    SELECT
        c.course_id,
        c.title                       AS course_title,
        COUNT(e.grade)                AS nb_notes,
        ROUND(AVG(e.grade), 2)        AS avg_grade
    FROM courses     AS c
    JOIN enrollments AS e ON e.course_id = c.course_id
    WHERE e.grade IS NOT NULL
    GROUP BY c.course_id, c.title
) AS cs
WHERE cs.nb_notes >= 3
ORDER BY cs.avg_grade DESC;


-- ================================================================
--  - Introduction aux CTE (WITH)
-- Objectif :
--   Réécrire l'exemple précédent avec WITH pour améliorer la lisibilité.
--
--   Définition :
--     Un CTE (Common Table Expression) est une sous-requête nommée
--     déclarée en tête de requête avec WITH.
--
--   Intérêt :
--     - Lisibilité (on évite d'imbriquer des sous-requêtes complexes)
--     - Réutilisation dans la même requête (dans certains cas)
-- ================================================================
WITH course_stats AS (
    SELECT
        c.course_id,
        c.title                       AS course_title,
        COUNT(e.grade)                AS nb_notes,
        ROUND(AVG(e.grade), 2)        AS avg_grade
    FROM courses     AS c
    JOIN enrollments AS e ON e.course_id = c.course_id
    WHERE e.grade IS NOT NULL
    GROUP BY c.course_id, c.title
)
SELECT
    course_title,
    nb_notes,
    avg_grade
FROM course_stats
WHERE nb_notes >= 3
ORDER BY avg_grade DESC;

-- ================================================================
-- - CTE multiples
-- Objectif :
--   Définir plusieurs CTE dans un même WITH.
--   Exemple :
--     1) cte_student_avg  : moyenne par étudiant
--     2) cte_global_avg   : moyenne globale
--     3) Requête finale   : comparer chaque étudiant à la moyenne globale
--
--   Syntaxe :
--     WITH cte1 AS (...),
--          cte2 AS (...)
--     SELECT ...
-- ================================================================
WITH cte_student_avg AS (
    SELECT
        s.student_id,
        s.full_name           AS student_name,
        s.program,
        ROUND(AVG(e.grade), 2) AS avg_grade
    FROM students    AS s
    JOIN enrollments AS e ON e.student_id = s.student_id
    WHERE e.grade IS NOT NULL
    GROUP BY s.student_id, s.full_name, s.program
),
cte_global_avg AS (
    SELECT ROUND(AVG(grade), 2) AS global_avg
    FROM enrollments
    WHERE grade IS NOT NULL
)
SELECT
    a.student_id,
    a.student_name,
    a.program,
    a.avg_grade,
    g.global_avg,
    (a.avg_grade - g.global_avg) AS diff_with_global
FROM cte_student_avg AS a
CROSS JOIN cte_global_avg AS g
ORDER BY diff_with_global DESC;