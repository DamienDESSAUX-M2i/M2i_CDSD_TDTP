CREATE SCHEMA music_stream;

CREATE TABLE IF NOT EXISTS music_stream.users(
    id_user INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name_user VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    date_sign_up DATE DEFAULT CURRENT_DATE,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS music_stream.songs(
    id_song INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    name_artist VARCHAR(255) NOT NULL,
    name_album VARCHAR(255) NOT NULL,
    song_length TIME NOT NULL,
    genre VARCHAR(255) NOT NULL,
    year_release DATE NOT NULL CHECK(year_release < NOW())
);

CREATE TABLE IF NOT EXISTS music_stream.playlists(
    id_playlist INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name_playlist VARCHAR(255) NOT NULL,
    id_user INT NOT NULL,
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES music_stream.users(id_user),
    id_song INT NOT NULL,
    CONSTRAINT fk_id_song FOREIGN KEY (id_song) REFERENCES music_stream.songs(id_song),
    date_playlist TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE music_stream.playlists;
DROP TABLE music_stream.songs;
DROP TABLE music_stream.users;
DROP SCHEMA music_stream;