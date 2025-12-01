-- ================================================================
-- DEMO VUES MATERIALISEES - Université
-- Pré-requis : demo_universite_schema.sql
--
-- Objectifs pédagogiques :
--  - Comprendre la différence entre :
--      * VIEW          : requête enregistrée, résultat recalculé à chaque SELECT
--      * MATERIALIZED VIEW : résultat stocké physiquement, à rafraîchir
--  - Créer des vues matérialisées basées sur des requêtes avec JOIN et agrégats
--  - Voir comment rafraîchir une vue matérialisée (REFRESH MATERIALIZED VIEW)
--  - Montrer l'intérêt : lecture plus rapide au prix d'une donnée pas toujours à jour
-- ================================================================


-- ================================================================
-- Rappel conceptuel (en commentaire)
-- ================================================================
-- VIEW classique :
--   - Syntaxe : CREATE [OR REPLACE] VIEW nom_vue AS SELECT ...
--   - La vue NE stocke PAS les données.
--   - À chaque SELECT sur la vue, PostgreSQL ré-exécute la requête sous-jacente.
--   - Avantage : toujours à jour.
--   - Inconvénient : peut être lent si la requête est complexe / volumineuse.
--
-- MATERIALIZED VIEW :
--   - Syntaxe : CREATE MATERIALIZED VIEW nom_vue AS SELECT ...
--   - La vue matérialisée STOCKE physiquement le résultat du SELECT
--     (comme une “table” générée).
--   - Un SELECT sur la vue matérialisée lit les données stockées (plus rapide).
--   - MAIS : le contenu ne se met PAS à jour tout seul.
--       -> Il faut utiliser : REFRESH MATERIALIZED VIEW nom_vue;
--   - Avantage : lecture rapide, surtout pour des grosses requêtes (JOIN, agrégats).
--   - Inconvénient : données potentiellement “périmées” entre deux REFRESH,
--                    prend de la place disque, nécessite une gestion explicite.


-- ================================================================
-- Nettoyage préalable : on supprime d'éventuelles anciennes vues matérialisées
-- ================================================================
DROP MATERIALIZED VIEW IF EXISTS mv_course_stats CASCADE;
DROP MATERIALIZED VIEW IF EXISTS mv_student_avg_grade CASCADE;

-- ================================================================
-- Étape 1 - Créer une vue matérialisée de statistiques par cours
--
-- Objectif :
--   Reprendre l'idée de v_course_stats (vue classique)
--   et en faire une version matérialisée.
--
-- Cas d'usage typique :
--   - Beaucoup de rapports / tableaux de bord lisent les mêmes stats.
--   - On préfère calculer ces agrégats une bonne fois (REFRESH) puis les lire rapidement.
-- ================================================================


CREATE MATERIALIZED VIEW mv_course_stats AS
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

-- Utilisation : on lit la vue matérialisée comme une table
SELECT *
FROM mv_course_stats
ORDER BY course_title;

-- ================================================================
-- Étape 2 - Ajouter un index sur une vue matérialisée
--
-- Objectif :
--   Montrer qu'une vue matérialisée se comporte comme une table :
--   on peut lui ajouter des index pour accélérer les requêtes.
-- ================================================================


-- Exemple : on ajoute un index sur avg_grade
-- (utile si on filtre / trie souvent sur la moyenne de cours)
CREATE INDEX idx_mv_course_stats_avg_grade
    ON mv_course_stats (avg_grade);

    -- Utilisation : chercher les cours avec moyenne >= 15
SELECT *
FROM mv_course_stats
WHERE avg_grade IS NOT NULL
  AND avg_grade >= 15
ORDER BY avg_grade DESC;

-- ================================================================
-- Étape 3 - Vue matérialisée de moyenne générale par étudiant
--
-- Objectif :
--   Créer une vue matérialisée qui résume la performance de chaque étudiant.
--   Même logique que v_student_avg_grade (vue classique),
--   mais matérialisée pour des lectures fréquentes (classements, rapports).
-- ================================================================

CREATE MATERIALIZED VIEW mv_student_avg_grade AS
SELECT
    s.student_id,
    s.full_name            AS student_name,
    s.program,
    ROUND(AVG(e.grade), 2) AS avg_grade,
    COUNT(e.grade)         AS nb_notes
FROM students    AS s
JOIN enrollments AS e
    ON e.student_id = s.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.student_id, s.full_name, s.program;

-- Utilisation : classement des étudiants par moyenne
SELECT *
FROM mv_student_avg_grade
ORDER BY avg_grade DESC;

-- Autre utilisation : filtrer les étudiants avec au moins 3 notes
SELECT *
FROM mv_student_avg_grade
WHERE nb_notes >= 3
ORDER BY avg_grade DESC;

-- ================================================================
-- Étape 4 - Démontrer la différence “à jour / pas à jour”
--
-- Objectif :
--   Montrer concrètement que la vue classique est à jour,
--   tandis que la vue matérialisée ne se met pas à jour automatiquement.
--
-- Scénario :
--   1) On insère une nouvelle note dans enrollments.
--   2) On compare :
--        - v_student_avg_grade (vue classique, si tu l'as créée avant)
--        - mv_student_avg_grade (vue matérialisée)
--   3) On fait un REFRESH MATERIALIZED VIEW, puis on recompare.
-- ================================================================


-- 4.1) Vérifier l'état initial pour un étudiant donné, par exemple Gina (id=7)
SELECT *
FROM mv_student_avg_grade
WHERE student_id = 7;

-- 4.2) On insère une nouvelle note pour Gina sur un cours existant
INSERT INTO enrollments (enrollment_id, student_id, course_id, grade)
VALUES (25, 7, 2, 19.5); 

-- Vue matérialisée (PAS encore rafraîchie)
SELECT *
FROM mv_student_avg_grade
WHERE student_id = 7;

-- À ce stade :
--   - v_student_avg_grade (vue classique) tient compte de la nouvelle note (si elle existe).
--   - mv_student_avg_grade (vue matérialisée) n'a PAS encore été mise à jour,
--     donc la moyenne de Gina n'a pas changé ici.

-- 4.4) Rafraîchir la vue matérialisée
REFRESH MATERIALIZED VIEW mv_student_avg_grade;

-- 4.5) Relecture de la vue matérialisée après refresh
SELECT *
FROM mv_student_avg_grade
WHERE student_id = 7;

-- Maintenant, la vue matérialisée reflète la nouvelle moyenne,
-- car on a recalculé toutes les données avec REFRESH MATERIALIZED VIEW.