CREATE TABLE IF NOT EXISTS livres (
	id_livre INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title VARCHAR(255),
	author VARCHAR(255),
	year_publication INT,
	genre VARCHAR(255),
	copies_available INT
);

DROP TABLE livres;