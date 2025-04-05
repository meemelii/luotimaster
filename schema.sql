CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    target_id INTEGER REFERENCES users,
    zip TEXT,
    confirm_status BIT
);

CREATE TABLE details (
    id INTEGER PRIMARY KEY,
    title TEXT,
    info TEXT,
    describe TEXT
);


CREATE TABLE event_details (
    id INTEGER PRIMARY KEY,
    event_id REFERENCES events,
    title TEXT,
    info TEXT
);