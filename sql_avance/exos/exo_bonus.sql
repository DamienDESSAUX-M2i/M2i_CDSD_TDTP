-- 1
DROP VIEW IF EXISTS v_restaurant_stat CASCADE;

CREATE OR REPLACE VIEW v_restaurant_stat AS
SELECT
    r.restaurant_id,
    r.name,
    r.city,
    COUNT(o.order_id) AS nb_orders,
    SUM(o.amount) AS total_amount_per_restaurant,
    ROUND(AVG(o.amount), 2) AS avg_amount_per_restaurant
FROM orders AS o
INNER JOIN restaurants AS r ON o.restaurant_id = r.restaurant_id
WHERE o.status <> 'CANCELLED'
GROUP BY r.restaurant_id;

DROP VIEW IF EXISTS v_global_stat CASCADE;

CREATE OR REPLACE VIEW v_global_stat AS
SELECT
    MIN(nb_orders) AS min_nb_orders,
    MAX(nb_orders) AS max_nb_orders,
    SUM(nb_orders) AS total_nb_orders,
    ROUND(AVG(nb_orders), 2) AS avg_nb_orders,
    MIN(total_amount_per_restaurant) AS min_total_amount_per_restaurant,
    MAX(total_amount_per_restaurant) AS max_total_amount_per_restaurant,
    SUM(total_amount_per_restaurant) AS total_amount,
    ROUND(AVG(total_amount_per_restaurant), 2) AS avg_amount
FROM v_restaurant_stat;

SELECT * FROM v_global_stat;

-- 2
SELECT
    rs.restaurant_id,
    rs.name,
    rs.city,
    rs.nb_orders,
    gs.min_nb_orders,
    gs.max_nb_orders,
    gs.avg_nb_orders,
    rs.total_amount_per_restaurant,
    gs.min_total_amount_per_restaurant,
    gs.max_total_amount_per_restaurant,
    gs.avg_amount
FROM v_restaurant_stat AS rs, v_global_stat AS gs;

-- 3
SELECT
    c.customer_id,
    c.full_name,
    c.city
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id
INNER JOIN restaurants AS r ON o.restaurant_id = r.restaurant_id
WHERE r.city = 'Paris'
ORDER BY c.full_name;

-- 4
WITH courier_delivery_sup_30 AS (
    SELECT
        c.courier_id,
        c.full_name,
        c.vehicle,
        d.delivery_id,
        d.delivery_time_min
    FROM deliveries AS d
    INNER JOIN couriers AS c ON d.courier_id = c.courier_id
    WHERE d.delivery_time_min > 30
    ORDER BY d.delivery_time_min DESC
)

SELECT
    courier_id,
    full_name,
    vehicle
FROM courier_delivery_sup_30
GROUP BY courier_id, full_name, vehicle
ORDER BY full_name;

-- 5
SELECT *
FROM v_restaurant_stat
WHERE nb_orders > 1;

-- 6
WITH restaurant_stat AS (
    SELECT
        r.restaurant_id,
        r.name,
        r.city,
        COUNT(o.order_id) AS nb_orders,
        SUM(o.amount) AS total_amount_per_restaurant,
        ROUND(AVG(o.amount), 2) AS avg_amount_per_restaurant
    FROM orders AS o
    INNER JOIN restaurants AS r ON o.restaurant_id = r.restaurant_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY r.restaurant_id;
)

SELECT *
FROM restaurant_stat
WHERE nb_orders > 1;

-- 7
DROP VIEW IF EXISTS v_courier_stat CASCADE;

CREATE OR REPLACE VIEW v_courier_stat AS
SELECT
    c.courier_id,
    c.full_name,
    c.vehicle,
    COUNT(d.delivery_id) AS nb_deliveries_per_courier,
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time_min_per_courier
FROM deliveries AS d
INNER JOIN couriers AS c ON d.courier_id = c.courier_id
GROUP BY c.courier_id;

DROP VIEW IF EXISTS v_global_stat CASCADE;

CREATE OR REPLACE VIEW v_global_courier_stat AS
SELECT
    MIN(nb_deliveries_per_courier) AS min_nb_deliveries,
    MAX(nb_deliveries_per_courier) AS max_nb_deliveries,
    SUM(nb_deliveries_per_courier) AS total_nb_deliveries,
    ROUND(AVG(nb_deliveries_per_courier), 2) AS avg_nb_deliveries,
    ROUND(SUM(avg_delivery_time_min_per_courier * nb_deliveries_per_courier) / SUM(nb_deliveries_per_courier), 2) AS avg_delivery_time_min
FROM v_courier_stat;

SELECT
    cs.courier_id,
    cs.full_name,
    cs.vehicle,
    cs.nb_deliveries_per_courier,
    gs.min_nb_deliveries,
    gs.max_nb_deliveries,
    gs.avg_nb_deliveries,
    cs.avg_delivery_time_min_per_courier,
    gs.avg_delivery_time_min
FROM v_courier_stat AS cs, v_global_courier_stat AS gs;