-- Nettoyage préalable
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- =========================
-- TABLE : customers
-- =========================
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    full_name     TEXT        NOT NULL,
    city          TEXT        NOT NULL,
    created_at    DATE        NOT NULL
);

INSERT INTO customers (customer_id, full_name, city, created_at) VALUES
    (1, 'Alice Martin',    'Lille',   DATE '2024-01-10'),
    (2, 'Bruno Dubois',    'Paris',   DATE '2024-02-05'),
    (3, 'Chloé Petit',     'Lyon',    DATE '2024-03-12'),
    (4, 'David Leroy',     'Lille',   DATE '2024-04-01');

-- =========================
-- TABLE : products
-- =========================
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    name         TEXT        NOT NULL,
    category     TEXT        NOT NULL,
    unit_price   NUMERIC(10,2) NOT NULL
);

INSERT INTO products (product_id, name, category, unit_price) VALUES
    (1, 'Clavier mécanique',  'Informatique', 79.90),
    (2, 'Souris gamer',       'Informatique', 49.90),
    (3, 'Casque audio',       'Audio',        89.00),
    (4, 'Tapis de souris',    'Accessoires',  19.90);

-- =========================
-- TABLE : orders
-- =========================
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   DATE    NOT NULL,
    status       TEXT    NOT NULL   -- 'PENDING', 'COMPLETED', 'CANCELLED'
);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
    (1, 1, DATE '2024-05-01', 'COMPLETED'),
    (2, 1, DATE '2024-05-02', 'COMPLETED'),
    (3, 2, DATE '2024-05-02', 'COMPLETED'),
    (4, 2, DATE '2024-05-03', 'PENDING'),
    (5, 3, DATE '2024-05-03', 'COMPLETED'),
    (6, 4, DATE '2024-05-04', 'CANCELLED');

-- =========================
-- TABLE : order_items
-- =========================
CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price     NUMERIC(10,2) NOT NULL
);

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1, 79.90),
    (2, 1, 4, 2, 19.90),
    (3, 2, 2, 1, 49.90),
    (4, 2, 4, 1, 19.90),
    (5, 3, 3, 1, 89.00),
    (6, 5, 1, 2, 79.90),
    (7, 5, 2, 1, 49.90);