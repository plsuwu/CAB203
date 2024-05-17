#!/usr/bin/env python

import graphs
import digraphs
import csv

from functools import reduce
from typing import Tuple


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
    # each `Tournament` is defined by a set of Bonkers games `G`, a set of players `P`
    #
    # each game `g` is played by a player and their opponent, `(p,o)`, where the game `(p,o)`
    #   is the same as `(o,p)` and `p` is any player from the set of players `P`
    #   and their opponent `o` is any player in `P` other than `p` such that `o != p`.
    #
    # a 'valid' tournament must contain games `G` such that any player `p` plays the same number
    #   of games `Pg` as any opponent `o` such that any `|Pg(p,o)| == |Pg(o,o)|`.
    #
    # a 'valid' tournament must contain games where all players `p` play against all other
    #   opponents `o` at least once, or play against a minimum of two opponents such that
    #   !(p1,p2) -> ((p1,o1) and (p1,o2)) and ((p2,o1) and (p2,o2))

    # number of unique vertices is the set of all p in {(p,o) | (o,p)}
    S = {a for (a, b) in games} | {b for (a, b) in games}
    E = games | {(a, b) for (b, a) in games}  # all possible edges 2|E|

    # unique vertices x that forms an edge with any u in S
    N = {x: {u for (v, u) in E if v == x} for (x, y) in E}

    # number of edges containing both v and any vertex u in S
    d = {len(N[u]) for u in S}

    # invalid if there is a differing number of edges for any u in N
    if len(d) != 1:
        return False

    # ----------------------------------------------------
    # i feel like there is a better way to write this code
    # ----------------------------------------------------
    # if (u,v) is not an edge in E, determine the intersect for non-(u,v) edges that
    # contain either u or v as a vertex
    #
    # valid if the length of this intersect is >= 2, otherwise invalid
    e = all((len(N[v] & N[u])) >= 2 for u in S for v in S if v != u and u not in N[v])

    return e


def referees(
    games: set[Tuple[str, str]], refereecsvfilename: str
) -> dict[Tuple[str, str], str] | None:

    # Referee,  Conflict1,  Conflict2,  Conflict3,  Conflict4
    # Joe,      Ashley,     Bob,        Charlie,    Ellie
    # Rene,     Charlie,    David,      Ellie
    # David,    Elaine,     Alice,      Ellie

    # games = {
    #   (joe, charlie)
    #   (bob, alice)
    #   (ellie, rene)
    # }
    # with open(refereecsvfilename, newline="") as f:
    #     reader = csv.reader(f)

    # parse the csv into a dictionary of each referee and a set of the referee's conflicts
    # discard the header column
    with open(refereecsvfilename, newline="") as f:
        reader = csv.reader(f)

        # parse the csv into a dictionary of each referee and a set of the referee's conflicts
        # discard the header column
        conflicts = {
            row[0].strip(): set(row[1:])
            for row in reader
            if row[0] != "Referee"
        }

        # find edges between edges in games `(p,o)` as a set of vertices g and referees as a set of vertices r
        # ignoring those where either `p | o` is found in a set of vertices `conflicts` that form an edge with r
        E = [ (g, r) for g in games for r in set(conflicts) if all(p not in conflicts[r] for p in g) ]

        # find a maximum matching set of edges in the graph G of (games | referees, edges E = (games, refs))
        max = digraphs.maxMatching(set(games), set(conflicts.keys()), E)

        # filter to the expected set of games and their referees such that the graph G = { (p,o): r }
        matched = {g: r for g, r in max if isinstance(g, tuple) and isinstance(r, str)}

        # if the output of matched edges contains the same number of items as the input, each game could be
        # assigned a referee without conflicts
        if len(matched) == len(games):
            return matched

        # otherwise, return `None` as our input is invalid.
        else:
            return None

def gameGroups(assignedReferees):
    pass


def gameSchedule(assignedReferees, gameGroups):
    pass


def scores(p, s, c, games):
    pass
