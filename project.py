#!/usr/bin/env python

import graphs
import digraphs
import csv

from collections import defaultdict


# 1. determine whether the tournament structure has the required properties:
#
#   a) for each distinct player, either they play against each other, or there are (minimum) two
#       other players that they BOTH play against.
#
#   b) all players have the same number of games.
#
# {(0, 1), (2, 3), (1, 2), (4, 0), (3, 4)}
#
# (0, 1)
# (2, 3)
# (1, 2)
# (4, 0)
# (3, 4)
def gamesOK(games: set) -> bool:
    # set of all vertices == all players
    V = {v for (v, u) in games} | {u for (v, u) in games}
    E = games | {(v, u) for (u, v) in games}  # 2|E| -> all (a,b) && (b,a)

    N = {x: {u for (v, u) in E if v == x} for (x, y) in E}
    d = {
        len(u) for v, u in N.items()
    }  # degrees == number of games each player has played

    if len(d) != 1:
        return False

    # this doesnt make sense lol
    played_against = all(
        (len(N[v] & N[u])) >= 2 for v in N for u in N if v != u and u not in N[v]
    )
    return played_against


def referees(games, refereecsvfilename):
    pass


def gameGroups(assignedReferees):
    pass


def gameSchedule(assignedReferees, gameGroups):
    pass


def scores(p, s, c, games):
    pass
