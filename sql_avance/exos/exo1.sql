-- 1. Catalogue public des morceaux
-- Le service Produit souhaite afficher une liste publique des morceaux, contenant :
-- les informations du morceau,
-- la durée,
-- le nom de l’artiste associé.

CREATE OR REPLACE VIEW v_tracks_artist AS
SELECT
    t.track_id,
    t.title AS track_title,
    t.duration_s,
    a.name AS artist_name
FROM tracks AS t
INNER JOIN artists AS a ON t.artist_id = a.artist_id;

SELECT *
FROM v_tracks_artist
ORDER BY artist_name, track_title;

-- 2. Utilisateurs Premium français
-- L’équipe marketing souhaite travailler spécifiquement sur les utilisateurs :
-- ayant un abonnement Premium,
-- résidant en France.

CREATE OR REPLACE VIEW v_users_france_prenium AS
SELECT
    user_id,
    username,
    country,
    subscription
FROM users
WHERE country = 'France' AND subscription = 'Premium';

SELECT *
FROM v_users_france_prenium
ORDER BY username;

-- 3. Historique détaillé des écoutes
-- L’équipe Data souhaite une vue qui rassemble toutes les informations utiles sur les écoutes :
-- l’utilisateur (identifiant, nom, pays),
-- le morceau (titre),
-- l’artiste,
-- la date/heure d’écoute,
-- la durée réellement écoutée.

CREATE OR REPLACE VIEW v_listenings_user_track AS
SELECT
    u.user_id,
    u.username,
    u.country AS user_country,
    t.track_id,
    t.title AS track_name,
    a.artist_id,
    a.name AS artist_name,
    l.listening_id,
    l.listened_at,
    l.seconds_played
FROM listenings AS l
INNER JOIN users AS u ON l.user_id = u.user_id
INNER JOIN tracks AS t ON l.track_id = t.track_id
INNER JOIN artists AS a ON t.artist_id = a.artist_id;

SELECT *
FROM v_listenings_user_track
WHERE user_country = 'France';

-- 4. Statistiques d’écoute par artiste
-- Pour optimiser l’analyse, cette statistique doit être construite à partir d’une vue matérialisée reposant sur les écoutes détaillées :
-- Pour chaque artiste, calculer :
-- le nombre total d’écoutes,
-- le nombre total de secondes écoutées,
-- la durée moyenne écoutée par écoute.

DROP MATERIALIZED VIEW IF EXISTS mv_artists_stats;

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_artists_stats AS
SELECT
    a.artist_id,
    a.name AS artist_name,
    a.country AS artist_country,
    COUNT(l.listening_id) AS nb_listening,
    SUM(l.seconds_played) AS sum_seconds_played,
    ROUND(AVG(l.seconds_played)) AS avg_seconds_played
FROM listenings AS l
INNER JOIN tracks AS t ON l.track_id = t.track_id
INNER JOIN artists AS a ON t.artist_id = a.artist_id
GROUP BY a.artist_id;

SELECT *
FROM mv_artists_stats
ORDER BY nb_listening DESC;

SELECT *
FROM mv_artists_stats
ORDER BY sum_seconds_played DESC;

-- 5. Analyse par pays d’artiste
-- À partir des statistiques d’écoute par artiste, analyser maintenant la performance :
-- par pays d’artiste,
-- en regroupant l’ensemble des artistes du même pays.
-- Produire une requête donnant, pour chaque pays :
-- le volume total d’écoute cumulé,
-- le nombre d’artistes concernés,
-- et ordonner ce classement.

SELECT
    artist_country,
    SUM(nb_listening) AS total_listening,
    COUNT(artist_id) AS nb_artists
FROM mv_artists_stats
GROUP BY artist_country;

-- 6. Optimisation et index
-- Certaines colonnes de ces vues matérialisées seront utilisées très souvent dans des filtres et tris (par exemple le total de secondes ou la moyenne par écoute).
-- Identifier les colonnes les plus pertinentes à indexer, et proposer les index adaptés pour optimiser ces usages.

CREATE INDEX IF NOT EXISTS mv_artists_stats
ON mv_artists_stats(nb_listening, sum_seconds_played, avg_seconds_played);