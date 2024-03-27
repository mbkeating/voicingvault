DROP TABLE IF EXISTS chord_played;
DROP TABLE IF EXISTS chord_progression_played;

CREATE TABLE chord_progression_played (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(255) REFERENCES player(google_uid),
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE chord_played (
    id SERIAL PRIMARY KEY,
    chord_progression_played_id INTEGER REFERENCES chord_progression_played(id),
    chord_id INTEGER REFERENCES chord_shape(id),
    chord_root_pos INTEGER NOT NULL
);