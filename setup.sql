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
    name TEXT NOT NULL,
    exp BIGINT NOT NULL,
    l_x INT NOT NULL,
    l_y INT NOT NULL
)