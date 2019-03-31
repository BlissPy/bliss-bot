CREATE TABLE IF NOT EXISTS prefixes (
    guildid BIGINT PRIMARY KEY,
    prefix VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS usernames (
    userid BIGINT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS players (
    ownerid BIGINT PRIMARY KEY,
    name TEXT,
    exp BIGINT,
    l_x INT,
    l_y INT
)