CREATE TABLE employes (
    nom_employe VARCHAR(255) PRIMARY KEY,
    service_employe VARCHAR(255)
);

INSERT INTO employes
VALUES ('Alice', 'IT'), ('Bob', 'RH'), ('Oscar', 'marketing');

CREATE TABLE services (
    nom_service VARCHAR(255) PRIMARY KEY
);

INSERT INTO services
VALUES ('IT'), ('RH'), ('Direction');

-- CROSS JOIN
SELECT * FROM employes, services;
SELECT * FROM employes CROSS JOIN services;

-- INNER JOIN
SELECT * FROM employes, services WHERE employes.service_employe = services.nom_service;
SELECT * FROM employes INNER JOIN services ON employes.service_employe = services.nom_service;

-- LEFT JOIN
SELECT * FROM employes LEFT JOIN services ON employes.service_employe = services.nom_service;

-- RIGHT JOIN
SELECT * FROM employes RIGHT JOIN services ON employes.service_employe = services.nom_service;

-- FULL JOIN
SELECT * FROM employes FULL JOIN services ON employes.service_employe = services.nom_service;