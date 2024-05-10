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

    # number of unique vertexes
    S = {v for (v, u) in games} | {u for (v, u) in games}
    E = games | {(v, u) for (u, v) in games} # all possible edges 2|E|

    # unique vertices x that form an edge with any u in S
    N = {x: {u for (v, u) in E if v == x} for (x, y) in E}

    # number of edges containing both v and any vertex u in S
    d = { len(N[u]) for u in S }

    # invalid if there is a differing number of edges for any u in N
    if len(d) != 1:
        return False

    # ----------------------------------------------------
    # i feel like there is a better way to write this code
    # ----------------------------------------------------
    # if (u,v) is not an edge in E, determine the intersect for non-(u,v) edges that
    # contain exactly one of (u,v) as a vertex
    #
    # valid if the length of this intersect is >= 2, otherwise invalid
    e = all( (len(N[v] & N[u])) >= 2 for u in S for v in S if v != u and u not in N[v] )

    return e


def referees(games, refereecsvfilename):
    pass


def gameGroups(assignedReferees):
    pass


def gameSchedule(assignedReferees, gameGroups):
    pass


def scores(p, s, c, games):
    pass
