# Tournament Planner (Swiss-Style)

## Overview

Write python module that uses PostgreSQL database to keep track of players and 
matches in a tournament

Using python develop a database schema to store the game matches and players. it should also rank the players and pair them in matches.


## Run the project

**To create Database**

```
$ psql
vagrant=> \i tournament.sql

```

**To test**

```
$ python tournament_test.py

```


## Output
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!