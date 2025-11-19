CREATE TABLE IF NOT EXISTS clients (
    id_client INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS commandes (
    id_commande INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_commande DATE DEFAULT CURRENT_DATE,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    id_client INT NOT NULL,
    CONSTRAINT fk_id_client FOREIGN KEY (id_client) REFERENCES clients(id_client)
);

DROP TABLE commandes;
DROP TABLE clients;