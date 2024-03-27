-- Create User table
CREATE TABLE player (
    google_uid VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    right_handed BOOLEAN DEFAULT true,
    PRIMARY KEY(google_uid)
);

-- Create Chord Shape table for c major shapes
CREATE TABLE chord_shape (
    id SERIAL PRIMARY KEY,
    chord_type VARCHAR(50) NOT NULL,
    chord_fingering VARCHAR (128) NOT NULL
);

-- Create Chord_Played table with foreign key references and chord root pos for transposition
CREATE TABLE chord_played (
    player_id VARCHAR(255) REFERENCES player(google_uid),
    chord_id INTEGER REFERENCES chord_shape(id),
    chord_root_pos INTEGER NOT NULL,
    times_looped INTEGER NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY(player_id, chord_id, chord_root_pos)
);