CREATE TABLE users (
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    verification_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(email)
);

-- Create Chord Shape table for c major shapes
CREATE TABLE chord_shape (
    id SERIAL PRIMARY KEY,
    chord_type VARCHAR(50) NOT NULL,
    chord_fingering VARCHAR (128) NOT NULL
);

CREATE TABLE chord_played (
    id SERIAL PRIMARY KEY,
    chord_progression_played_id INTEGER REFERENCES chord_progression_played(id),
    chord_id INTEGER REFERENCES chord_shape(id),
    chord_root_pos INTEGER NOT NULL
);

CREATE TABLE chord_progression_played (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(255) REFERENCES player(google_uid),
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
