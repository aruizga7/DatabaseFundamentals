-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS standings CASCADE;

CREATE TABLE players(
	id SERIAL PRIMARY KEY,
	name TEXT);

CREATE TABLE matches(
	id SERIAL PRIMARY KEY,
	winner_id INTEGER REFERENCES players,
	loser_id INTEGER REFERENCES players);

CREATE VIEW standings AS
	SELECT players.id as player_id, players.name, 
		(SELECT count(*) FROM matches WHERE matches.winner_id = players.id) AS matches_won, 
		(SELECT count(*) FROM matches WHERE players.id in (winner_id, loser_id)) as matches_played
		FROM players
	GROUP BY players.id
	ORDER BY matches_won DESC;