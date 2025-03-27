CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    target_id INTEGER REFERENCES users,
    zip TEXT,
    weapon_type INTEGER,
    confirm_status BIT
);