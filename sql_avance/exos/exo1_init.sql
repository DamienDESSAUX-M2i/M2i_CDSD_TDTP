DROP TABLE IF EXISTS listenings;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS users;

-- =========================
-- TABLE : users
-- =========================
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    username      TEXT        NOT NULL,
    country       TEXT        NOT NULL,
    subscription  TEXT        NOT NULL  -- 'Free' ou 'Premium'
);

INSERT INTO users (user_id, username, country, subscription) VALUES
    (1, 'alice',   'France',  'Free'),
    (2, 'bruno',   'France',  'Premium'),
    (3, 'carla',   'Belgique','Premium'),
    (4, 'david',   'Canada',  'Free'),
    (5, 'emma',    'France',  'Premium');

-- =========================
-- TABLE : artists
-- =========================
CREATE TABLE artists (
    artist_id  INTEGER PRIMARY KEY,
    name       TEXT        NOT NULL,
    country    TEXT        NOT NULL
);

INSERT INTO artists (artist_id, name, country) VALUES
    (1, 'Electro Pulse',   'France'),
    (2, 'Rocking Stones',  'USA'),
    (3, 'LoFi Dreams',     'Canada');

-- =========================
-- TABLE : tracks
-- =========================
CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    title      TEXT        NOT NULL,
    duration_s INTEGER     NOT NULL,
    artist_id  INTEGER     NOT NULL REFERENCES artists(artist_id)
);

INSERT INTO tracks (track_id, title, duration_s, artist_id) VALUES
    (1, 'Morning Energy',  210, 1),
    (2, 'Night Runner',    190, 1),
    (3, 'Stone Highway',   230, 2),
    (4, 'Chill Vibes',     300, 3),
    (5, 'Deep Focus',      280, 3);

-- =========================
-- TABLE : listenings
-- =========================
CREATE TABLE listenings (
    listening_id   INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id),
    track_id       INTEGER NOT NULL REFERENCES tracks(track_id),
    listened_at    TIMESTAMP NOT NULL,
    seconds_played INTEGER NOT NULL
);

INSERT INTO listenings (listening_id, user_id, track_id, listened_at, seconds_played) VALUES
    (1, 1, 1, TIMESTAMP '2025-01-10 09:00:00', 180),
    (2, 1, 4, TIMESTAMP '2025-01-10 09:30:00', 200),
    (3, 2, 1, TIMESTAMP '2025-01-11 10:00:00', 210),
    (4, 2, 2, TIMESTAMP '2025-01-11 10:30:00', 190),
    (5, 2, 3, TIMESTAMP '2025-01-11 11:00:00', 230),
    (6, 3, 4, TIMESTAMP '2025-01-12 08:45:00', 250),
    (7, 3, 5, TIMESTAMP '2025-01-12 09:15:00', 260),
    (8, 4, 3, TIMESTAMP '2025-01-13 14:00:00', 120),
    (9, 5, 1, TIMESTAMP '2025-01-14 18:00:00', 210),
    (10,5, 5, TIMESTAMP '2025-01-14 18:30:00', 200);