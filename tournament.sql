-- Drop Database 
DROP DATABASE IF EXISTS tournament;

-- Create DATABASE
CREATE DATABASE tournament;

-- Switch DATABASE
\c tournament;


-- Create players table
CREATE TABLE players(
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- Create match table
CREATE TABLE matches(
    matchid SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id)
);

-- Create winners view
CREATE MATERIALIZED VIEW winners AS
    SELECT players.id AS player, count(matches.winner) AS wins
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id, matches.winner
    ORDER BY players.id;

-- Create loosers view
CREATE MATERIALIZED VIEW loosers AS
    SELECT players.id AS player, count(matches.loser) AS losses
    FROM players LEFT JOIN matches
    ON players.id = matches.loser
    GROUP BY players.id, matches.loser
    ORDER BY players.id;

-- Create match combination view
CREATE MATERIALIZED VIEW rounds AS
    SELECT players.id AS player, count(matches) AS matches
    FROM players LEFT JOIN matches
    ON(players.id=matches.winner) OR(players.id=matches.loser)
    GROUP BY players.id
    ORDER BY players.id ASC;
