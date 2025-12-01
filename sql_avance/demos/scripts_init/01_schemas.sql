
-- Nettoyage pour rejouer le script
DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- ===========================
-- Table des étudiants
-- ===========================
CREATE TABLE students (
    student_id      INTEGER PRIMARY KEY,
    full_name       TEXT        NOT NULL,
    program         TEXT        NOT NULL,   -- ex : "L3 Informatique", "M1 Data Science"
    city            TEXT        NOT NULL
);

INSERT INTO students (student_id, full_name, program, city) VALUES
    (1, 'Alice Martin',   'L3 Informatique',    'Lille'),
    (2, 'Bruno Dubois',   'L3 Informatique',    'Lille'),
    (3, 'Chloé Petit',    'M1 Data Science',    'Paris'),
    (4, 'David Leroy',    'M1 Data Science',    'Lyon'),
    (5, 'Emma Renault',   'L2 Mathématiques',   'Lille'),
    (6, 'Farid Benali',   'L2 Mathématiques',   'Marseille'),
    (7, 'Gina Rossi',     'M2 Intelligence Artificielle', 'Paris');

-- ===========================
-- Table des enseignants
-- ===========================
CREATE TABLE teachers (
    teacher_id      INTEGER PRIMARY KEY,
    full_name       TEXT        NOT NULL,
    department      TEXT        NOT NULL     -- ex : "Informatique", "Mathématiques", ...
);

INSERT INTO teachers (teacher_id, full_name, department) VALUES
    (1, 'Prof. Sophie Durant',  'Informatique'),
    (2, 'Prof. Marc Olivier',   'Mathématiques'),
    (3, 'Dr. Nora Karim',       'Data Science'),
    (4, 'Dr. Paul André',       'Statistiques'),
    (5, 'Prof. Laura Cohen',    'Informatique');

-- ===========================
-- Table des cours
-- ===========================
CREATE TABLE courses (
    course_id       INTEGER PRIMARY KEY,
    title           TEXT        NOT NULL,
    ects            INTEGER     NOT NULL,    -- crédits ECTS
    teacher_id      INTEGER     NOT NULL REFERENCES teachers(teacher_id)
);

INSERT INTO courses (course_id, title, ects, teacher_id) VALUES
    (1, 'Bases de données',                    6, 1),
    (2, 'Algèbre linéaire',                    6, 2),
    (3, 'Probabilités',                        4, 4),
    (4, 'Apprentissage automatique',           6, 3),
    (5, 'Programmation avancée',               5, 5),
    (6, 'Introduction au Big Data',            4, 3),
    (7, 'Analyse de données avec Python',      5, 3),
    (8, 'Logique mathématique',                4, 2);

-- ===========================
-- Table des inscriptions aux cours
-- ===========================
CREATE TABLE enrollments (
    enrollment_id   INTEGER PRIMARY KEY,
    student_id      INTEGER NOT NULL REFERENCES students(student_id),
    course_id       INTEGER NOT NULL REFERENCES courses(course_id),
    grade           NUMERIC(4,1)  -- note sur 20, peut être NULL si pas encore noté
);

INSERT INTO enrollments (enrollment_id, student_id, course_id, grade) VALUES
    -- Alice (id=1)
    ( 1, 1, 1, 14.5),
    ( 2, 1, 5, 15.0),
    ( 3, 1, 3, 12.0),
    ( 4, 1, 7, NULL),

    -- Bruno (id=2)
    ( 5, 2, 1, 11.0),
    ( 6, 2, 5, 13.5),
    ( 7, 2, 2, 10.0),

    -- Chloé (id=3)
    ( 8, 3, 1, 16.0),
    ( 9, 3, 4, 17.5),
    (10, 3, 6, 14.0),
    (11, 3, 7, 18.0),

    -- David (id=4)
    (12, 4, 4, 12.5),
    (13, 4, 6, NULL),
    (14, 4, 3, 13.0),

    -- Emma (id=5)
    (15, 5, 2,  9.5),
    (16, 5, 3, 11.0),
    (17, 5, 8, NULL),

    -- Farid (id=6)
    (18, 6, 2, 12.5),
    (19, 6, 8, 13.0),
    (20, 6, 3, NULL),

    -- Gina (id=7)
    (21, 7, 4, 18.5),
    (22, 7, 6, 17.0),
    (23, 7, 7, 19.0),
    (24, 7, 1, 16.5);