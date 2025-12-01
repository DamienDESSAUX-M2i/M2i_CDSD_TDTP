-- 1. Synthèse des commandes
-- L’équipe métier souhaite disposer d’une vue qui centralise, pour chaque commande :
-- les informations de base de la commande (client, date, statut),
-- le montant total de la commande.
-- Mettre en place une vue adaptée à ce besoin à partir des tables existantes.
-- Exploiter cette vue pour obtenir la liste des commandes complétées, avec leurs montants, classées par date puis par identifiant de commande.

CREATE OR REPLACE VIEW v_orders_infos AS
SELECT
    o.order_id,
    c.customer_id,
    c.full_name AS customer_full_name,
    o.order_date,
    o.status,
    SUM(oi.quantity * oi.unit_price) AS total_amout
FROM order_items AS oi
INNER JOIN orders AS o ON oi.order_id = o .order_id
INNER JOIN customers AS c ON o.customer_id = c.customer_id
GROUP BY o.order_id, customer_id;

SELECT *
FROM v_orders_infos
WHERE status = 'COMPLETED'
ORDER BY order_date, order_id;

-- 2. Statistiques de ventes par jour
-- Le service de reporting a besoin d’un tableau de bord quotidien indiquant, pour chaque jour :
-- le nombre de commandes complétées,
-- le chiffre d’affaires total de ces commandes.
-- Pour optimiser les performances, ce tableau de bord doit être construit à partir d’une vue matérialisée basée sur les données des commandes.
-- Mettre en place une vue matérialisée qui fournit ces statistiques quotidiennes.
-- Interroger cette vue pour afficher la totalité des jours connus, classés par date.
-- Interroger cette même vue pour obtenir uniquement les jours dont le chiffre d’affaires est supérieur ou égal à 200.

DROP MATERIALIZED VIEW IF EXISTS mv_orders_completed;

CREATE MATERIALIZED VIEW mv_orders_completed AS
SELECT
    o.order_date,
    COUNT(o.order_id) AS nd_orders,
    SUM(oi.quantity * oi.unit_price) AS total_amout
FROM order_items AS oi
INNER JOIN orders AS o ON oi.order_id = o.order_id
WHERE o.status = 'COMPLETED'
GROUP BY o.order_date;

SELECT *
FROM mv_orders_completed
ORDER BY order_date ASC;

SELECT *
FROM mv_orders_completed
WHERE total_amout > 200
ORDER BY total_amout DESC;

-- 3. Clients les plus rentables
-- La direction souhaite identifier les clients les plus intéressants commercialement, en se basant uniquement sur les commandes complétées :
-- Pour chaque client, on veut connaître :
-- le nombre de commandes complétées,
-- le chiffre d’affaires total associé.
-- Mettre en place une vue matérialisée qui regroupe ces informations par client.
-- Exploiter cette vue pour afficher la liste des clients, classés du plus gros chiffre d’affaires au plus faible.
-- Exploiter cette vue pour afficher uniquement les clients ayant passé au moins deux commandes complétées.

DROP MATERIALIZED VIEW IF EXISTS mv_customers_completed;

CREATE MATERIALIZED VIEW mv_customers_completed AS
SELECT
    c.customer_id,
    c.full_name,
    c.city,
    COUNT(o.order_id) AS nd_orders,
    SUM(oi.quantity * oi.unit_price) AS total_amout
FROM order_items AS oi
INNER JOIN orders AS o ON oi.order_id = o.order_id
INNER JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id;

SELECT *
FROM mv_customers_completed
ORDER BY total_amout DESC;

SELECT *
FROM mv_customers_completed
WHERE nd_orders >= 2
ORDER BY nd_orders DESC;

-- 4. Optimisation via index
-- Certaines requêtes sont particulièrement fréquentes :
-- filtrer ou trier les statistiques par date,
-- interroger souvent les clients par chiffre d’affaires total.
-- Proposer un ou plusieurs index pertinents sur les vues matérialisées précédentes afin d’optimiser ces usages.
-- Justifier brièvement, pour chaque index, le type de requête qu’il permet d’accélérer.

-- Index pour filtrer par date :
CREATE INDEX i_order_date ON mv_orders_completed(order_date);

-- Index pour récupérer les chiffres d'affaires
CREATE INDEX i_order_total_amout ON mv_orders_completed(total_amout);
CREATE INDEX i_customer_total_amout ON mv_customers_completed(total_amout);

-- 5. Données à jour vs vues matérialisées
-- On simule maintenant l’arrivée de nouvelles données dans le système :
-- Une nouvelle commande complétée est enregistrée pour le client 2 :
-- INSERT INTO orders (order_id, customer_id, order_date, status)
-- VALUES (7, 2, DATE '2024-05-04', 'COMPLETED');
-- INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
--     (8, 7, 3, 1, 89.00),
--     (9, 7, 4, 1, 19.90);
-- Vérifier, à l’aide de la vue classique mise en place à la question 1, que cette nouvelle commande est bien prise en compte.
-- Vérifier, à l’aide de la vue matérialisée de statistiques quotidiennes, si les données reflètent ou non cette nouvelle commande.
-- Mettre à jour la vue matérialisée de statistiques quotidiennes pour qu’elle reflète l’état actuel des données.
-- Refaire la vérification et expliquer (en quelques mots, par commentaire ou à l’oral) la différence de comportement entre la vue classique et la vue matérialisée.

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
    (7, 2, DATE '2024-05-04', 'COMPLETED');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (8, 7, 3, 1, 89.00),
    (9, 7, 4, 1, 19.90);

-- VIEW
SELECT *
FROM v_orders_infos
WHERE status = 'COMPLETED'
ORDER BY order_date;

-- MATERIALIZED VIEW
SELECT *
FROM mv_orders_completed
ORDER BY order_date ASC;

-- REFRESH MATERIALIZED VIEWS
REFRESH MATERIALIZED VIEW mv_orders_completed;
REFRESH MATERIALIZED VIEW mv_customers_completed;

-- MATERIALIZED VIEW
SELECT *
FROM mv_orders_completed
ORDER BY order_date ASC;