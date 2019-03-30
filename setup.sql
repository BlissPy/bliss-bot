CREATE TABLE IF NOT EXISTS prefixes (
    guildid BIGINT PRIMARY KEY,
    prefix VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS usernames (
    userid BIGINT,
    name TEXT
);