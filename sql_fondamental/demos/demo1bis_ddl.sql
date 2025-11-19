CREATE SCHEMA demo_padawan;
-- SET search_path TO 'demo_padawan', '$user', 'public';

CREATE TABLE IF NOT EXISTS demo_padawan.padawan (
	padawan_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS demo_padawan.niveau (
	niveau_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	libelle VARCHAR(50) NOT NULL UNIQUE, 
	bonus INT NOT NULL
);

CREATE TABLE IF NOT EXISTS demo_padawan.parcours (
	parcours_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	date_parcours DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	padawan_id INT NOT NULL,
	CONSTRAINT fk_padawan_id FOREIGN KEY (padawan_id) 
	REFERENCES demo_padawan.padawan(padawan_id)
);

CREATE TABLE IF NOT EXISTS demo_padawan.obstacles (
	obstacles_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	"name" VARCHAR(30) NOT NULL,
	min_grade INT NOT NULL DEFAULT 0,
	niveau_id INT NOT NULL,
	CONSTRAINT fk_niveau_id FOREIGN KEY (niveau_id) 
	REFERENCES demo_padawan.niveau(niveau_id)
);

CREATE TABLE IF NOT EXISTS demo_padawan.parcours_obstacles (
	parcours_id INT NOT NULL,
	obstacles_id INT NOT NULL,
	grade INT NOT NULL,
	"time" TIME NOT NULL,
	CONSTRAINT pk_parcours_obstacles PRIMARY KEY (parcours_id, obstacles_id),
	CONSTRAINT fk_parcours_id FOREIGN KEY (parcours_id) REFERENCES demo_padawan.parcours(parcours_id),
	CONSTRAINT fk_obstacles_id FOREIGN KEY (obstacles_id) REFERENCES demo_padawan.obstacles(obstacles_id)
);
