CREATE TABLE IF NOT EXISTS predictions (
    prediction_id SERIAL PRIMARY KEY,
    feature VARCHAR(255) NOT NULL,
    prediction INTEGER NOT NULL,
    probability FLOAT NOT NULL
);