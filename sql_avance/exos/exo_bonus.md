# SUJET – Sous-requêtes & CTE (Application de livraison)

## Contexte

Tu travailles pour une petite application de **livraison de repas**.
L’entreprise souhaite analyser différents aspects des commandes :

* chiffres clés globaux,
* comportement des livreurs,
* restaurants les plus performants,
* comparaison de performances,
* extraction conditionnelle d’informations.

Les concepts vus en cours portent sur :

* sous-requêtes **scalaires**,
* sous-requêtes **corrélées**,
* sous-requêtes dans **IN**,
* sous-requêtes dans **EXISTS**,
* sous-requêtes dans **FROM** (tables dérivées),
* **CTE** simples et multiples.

Tu dois produire plusieurs requêtes permettant d’exploiter ces concepts dans un contexte différent de la démonstration.

---

## 0. Préparation : schéma et données

Exécute le script suivant :

```sql
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
```

---

# EXERCICE

## 1. Statistique globale reprise sur chaque ligne

L’entreprise souhaite afficher, pour chaque restaurant, une statistique **globale** qui ne dépend pas du restaurant lui-même.

Élaborer une requête affichant, pour chaque restaurant, une information issue d’un calcul global portant sur toutes les commandes livrées.

---

## 2. Calcul par restaurant utilisant une valeur corrélée

On souhaite cette fois obtenir, pour chaque restaurant, une valeur calculée uniquement avec **les commandes de ce restaurant-ci**.

Élaborer une requête qui compare une statistique propre à chaque restaurant à une statistique identique mais **globale**.

---

## 3. Extraction conditionnelle avec IN

L’équipe Marketing souhaite obtenir la liste des clients ayant commandé dans un ensemble déterminé de restaurants situés à Paris.

Construire une requête retournant uniquement les clients qui correspondent à ce critère.

---

## 4. Extraction conditionnelle avec EXISTS

On cherche maintenant les livreurs ayant effectué au moins une livraison qui dépasse un certain seuil de temps.

Construire une requête qui identifie ces livreurs.

---

## 5. Table dérivée dans FROM

La direction souhaite analyser uniquement les restaurants ayant un volume de commandes suffisant.

Construire une requête qui s’appuie sur une table dérivée pour obtenir d’abord des statistiques par restaurant, puis appliquer un filtre sur le résultat intermédiaire.

---

## 6. CTE simple

Réécrire la logique précédente avec un CTE pour en améliorer la lisibilité.

---

## 7. CTE multiples

L’entreprise souhaite comparer :

* le temps moyen de livraison par livreur,
* au temps de livraison moyen **global**.

Construire une requête en utilisant plusieurs CTE pour calculer ces statistiques, puis présenter le résultat final en comparant ces deux valeurs.