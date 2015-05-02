-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop tables if already exist
DROP TABLE IF EXISTS players, matches;
-- create players table to keep track of players' stats
CREATE TABLE players (
    id serial primary key,
    name text
);

-- create matches table to record match results
CREATE TABLE matches (
    id serial primary key,
    winner int references players(id),
    loser int references players(id)
);
