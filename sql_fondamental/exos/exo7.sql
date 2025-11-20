-- Question a
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
INNER JOIN Achats AS a
ON c.id = a.client_id;

-- Question b
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
LEFT JOIN Achats AS a
ON c.id = a.client_id;

-- Question c
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
RIGHT JOIN Achats AS a
ON c.id = a.client_id;

-- Question d
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
FULL JOIN Achats AS a
ON c.id = a.client_id;

-- Bonus 1
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
LEFT JOIN Achats AS a
ON c.id = a.client_id
WHERE a.client_id IS NULL;

-- Bonus 2
SELECT c.nom, c.prenom, a.produit, a.montant
FROM Clients AS c
RIGHT JOIN Achats AS a
ON c.id = a.client_id
WHERE c.id IS NULL;