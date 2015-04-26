-- Table definitions for the tournament project.
-- drop tables if already exist
drop table if exists players, matches;

-- create players table to keep track of players' stats
create table players (
    id serial primary key,
    name text,
    wins int default 0,
    matches int default 0
);

-- create matches table to record match results
create table matches (
    id serial primary key,
    winner int references players(id),
    loser int references players(id)
);
