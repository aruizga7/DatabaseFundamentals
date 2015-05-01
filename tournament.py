#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pg = connect();
    c = pg.cursor();
    c.execute("DELETE FROM matches")
    pg.commit();
    pg.close()


def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect();
    c = pg.cursor();
    c.execute("DELETE FROM players")
    pg.commit();
    pg.close()

def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect();
    c = pg.cursor();
    c.execute("SELECT COUNT(*) FROM players");
    r = c.fetchone();
    pg.close()
    return r[0];

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg = connect()
    c = pg.cursor()
    c.execute("INSERT INTO players(name) VALUES (%s)", (name,));
    pg.commit()
    pg.close()


def playerStandings():

    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    base_query = """
    select players.id, name, count(matches.id) as {win_or_loss}
        from players left join matches
            on players.id = {field}
        group by players.id
        order by {win_or_loss} desc
    """
    query_wins = base_query.format(field='winner', win_or_loss='wins')
    query_losses = base_query.format(field='loser', win_or_loss='losses')
    query_join = """
    select winners.id, winners.name, wins, wins+losses as matches
        from ({query_wins}) as winners left join ({query_losses}) as losers
            on winners.id = losers.id;
    """.format(query_wins=query_wins, query_losses=query_losses)
    db = connect()
    c = db.cursor()
    c.execute(query_join + ';')
    results = c.fetchall()

    db.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg = connect()
    c = pg.cursor() 
    add_query = """
    INSERT INTO matches (winner, loser)
    VALUES ({winner}, {loser})
    """.format(winner=winner, loser=loser)
    c.execute(add_query)
    pg.commit()   
    pg.close()
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


    standings = playerStandings()
    pairings = []
    for i in range(0, len(standings), 2):
        standing1 = standings[i]
        standing2 = standings[i+1]
        pairings.append([standing1[1], standing2[1], standing1[0], standing2[0]])

    return pairings


