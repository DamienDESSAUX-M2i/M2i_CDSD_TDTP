DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS couriers;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;

-- =========================
-- TABLE : customers
-- =========================
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    full_name   TEXT NOT NULL,
    city        TEXT NOT NULL
);

INSERT INTO customers VALUES
    (1, 'Alice Moreau', 'Lille'),
    (2, 'Bruno Martin', 'Lyon'),
    (3, 'Chloé Bernard','Paris'),
    (4, 'David Leroy',  'Marseille');

-- =========================
-- TABLE : restaurants
-- =========================
CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    city          TEXT NOT NULL
);

INSERT INTO restaurants VALUES
    (1, 'PastaBello',   'Lille'),
    (2, 'BurgerTop',    'Paris'),
    (3, 'SushiZen',     'Paris'),
    (4, 'TacoWave',     'Lyon');

-- =========================
-- TABLE : couriers (Livreurs)
-- =========================
CREATE TABLE couriers (
    courier_id INTEGER PRIMARY KEY,
    full_name  TEXT NOT NULL,
    vehicle    TEXT NOT NULL
);

INSERT INTO couriers VALUES
    (1, 'Lucas Roy',    'Vélo'),
    (2, 'Emma Perrin',  'Scooter'),
    (3, 'Hugo Lefebvre','Vélo');

-- =========================
-- TABLE : orders
-- =========================
CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id),
    amount        NUMERIC(8,2) NOT NULL,
    status        TEXT NOT NULL, -- 'DELIVERED', 'CANCELLED'
    order_date    DATE NOT NULL
);

INSERT INTO orders VALUES
    (1, 1, 1, 25.50, 'DELIVERED', DATE '2024-03-10'),
    (2, 1, 4, 18.90, 'DELIVERED', DATE '2024-03-15'),
    (3, 2, 2, 30.00, 'CANCELLED', DATE '2024-03-12'),
    (4, 3, 3, 42.00, 'DELIVERED', DATE '2024-03-11'),
    (5, 3, 2, 15.00, 'DELIVERED', DATE '2024-03-12'),
    (6, 4, 1, 28.50, 'DELIVERED', DATE '2024-03-12');

-- =========================
-- TABLE : deliveries (assignation du coursier)
-- =========================
CREATE TABLE deliveries (
    delivery_id INTEGER PRIMARY KEY,
    order_id    INTEGER NOT NULL REFERENCES orders(order_id),
    courier_id  INTEGER NOT NULL REFERENCES couriers(courier_id),
    delivery_time_min INTEGER NOT NULL -- durée effective de livraison
);

INSERT INTO deliveries VALUES
    (1, 1, 1, 35),
    (2, 2, 3, 30),
    (3, 4, 2, 25),
    (4, 5, 1, 40),
    (5, 6, 2, 20);