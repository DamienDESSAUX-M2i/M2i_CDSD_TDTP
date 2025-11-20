-- Question 1
CREATE TABLE services (
    id_service uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    libelle TEXT NOT NULL,
    date_creation DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE employees (
    id_employee uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT,
    id_service uuid NOT NULL,
    CONSTRAINT fk_id_service FOREIGN KEY (id_service) REFERENCES services(id_service)
);

-- Question 2a
INSERT INTO services (libelle)
VALUES
    ('Informatique'),
    ('Marketing');

INSERT INTO services (libelle, date_creation)
VALUES ('Ressources Humaines', '2024-01-01');

-- Question 2b
UPDATE services
SET libelle='IT'
WHERE libelle='Informatique';

UPDATE services
SET date_creation=NOW()
WHERE libelle='Ressources Humaines';

-- Question 2c
DELETE FROM services WHERE libelle='Marketing';
DELETE FROM services WHERE date_creation<'2024-01-01';

-- Question 3a
INSERT INTO employees (nom, prenom, id_service)
VALUES
    ('Martin', 'Paul', (SELECT id_service FROM services WHERE libelle='IT' LIMIT 1)),
    ('Dupont', 'Claire', (SELECT id_service FROM services WHERE libelle='IT' LIMIT 1)),
    ('Bernard', 'Sophie', (SELECT id_service FROM services WHERE libelle='Ressources Humaines' LIMIT 1));

-- Question 3b
UPDATE employees
SET nom='Martinez'
WHERE nom='Martin';

-- Question 3b
DELETE FROM employees WHERE prenom='Claire';

-- Question 4
SELECT * FROM services;
SELECT * FROM employees;