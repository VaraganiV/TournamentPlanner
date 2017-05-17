# import PostgreSQL DB library
import psycopg2

# Connect to DB
def connect():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect("dbname=tournament")


# Cleanup matches
def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    query = "DELETE from matches WHERE matchid NOTNULL;"
    cursor.execute(query)
    DB.commit()
    DB.close()
    refreshViews()

# Delete matches
def deletePlayers():
    """Remove all player records from the database."""
    DB = connect()
    c = DB.cursor()
    q = "DELETE from players WHERE id NOTNULL;"
    c.execute(q)
    DB.commit()
    DB.close()
    refreshViews()

# Count player
def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    q = "SELECT count(id) as num FROM players;"
    c.execute(q)
    count = int(c.fetchone()[0])
    DB.close()
    return count

# Register players
def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
    name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    q = "INSERT INTO players (name) values (%s)"
    c.execute(q, (name,))
    DB.commit()
    DB.close()
    refreshViews()

# Players still standing
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
    refreshViews()
    DB = connect()
    c = DB.cursor()
    q = """
		SELECT players.id, players.name, winners.wins, rounds.matches
		FROM players
		LEFT JOIN winners ON players.id = winners.player
		LEFT JOIN rounds ON players.id = rounds.player
		GROUP BY players.id, players.name, winners.wins, rounds.matches
		ORDER BY winners.wins DESC;
	"""
    c.execute(q)
    standings = c.fetchall()
    DB.close()
    return standings


# Report matches
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
    winner:  the id number of the player who won
    loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    q = "INSERT INTO matches (winner, loser) values (%s, %s);"
    c.execute(q, (int(winner), int(loser)))
    DB.commit()
    DB.close()
    refreshViews()


def breakIntoGroups(list, size=2):
    size = max(1, size)
    return [list[i:i + size] for i in range(0, len(list), size)]


# Swiss Pairing
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
    grouped_pool = breakIntoGroups(standings, 2)
    matched_pairs = list()

    for pair in grouped_pool:
        pairing = list()
        for player in pair:
            pairing.append(player[0])
            pairing.append(player[1])
        matched_pairs.append(pairing)

    return matched_pairs

# Refresh views
def refreshViews():
    """Refreshes materialized views derived from MATCHES."""
    DB = connect()
    c = DB.cursor()
    c.execute("REFRESH MATERIALIZED VIEW winners;")
    c.execute("REFRESH MATERIALIZED VIEW loosers;")
    c.execute("REFRESH MATERIALIZED VIEW rounds;")
    DB.commit()
    DB.close()