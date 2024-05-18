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
    # each `Tournament` is defined by a set of Bonkers games `A`, a set of players `P`
    #
    # each game `g` is played by a player and their opponent, `(p,o)`, where the game `(p,o)`
    #   is the same as `(o,p)` and `p` is any player from the set of players `P`
    #   and their opponent `o` is any player in `P` other than `p` such that `o != p`.
    #
    # a 'valid' tournament must contain games `A` such that any player `p` plays the same number
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

    with open(refereecsvfilename, newline="") as csv_file:
        # parse the csv file into a dictionary C of referees (keys) and their
        # respective conflicts of interest (values)
        reader = csv.reader(csv_file)
        C = {
            # referee (index 0) as key
            row[0].strip(): set(
                # read all columns after referee name into a set under the referee as the key
                # discard empty rows
                row[n].strip() for n in range(1, len(row)) if row[n] != ""
            )
            for row in reader
            # discard header row
            if row[0].strip() != "Referee"
        }

        # convert set games to a list so iterators over `games` to give them a fixed order
        A = list(games)
        B = set(C.keys()) # referees

        # find the set of edges E with each edge `e = (g, r)` assigning a referee `r` from the
        # set `B` to a game `g` in `A` where `g = (p, p)` and `r = (r: c)` in the set of conflicts
        # `C` such that `r` or any `c` is not also in their assigned `g`
        E = {
            (g, r)
            for g in A
            for r, c in C.items()
            if all(r not in p and u not in p for u in c for p in g)
        }

        # find the maximum matching in the bipartite graph `G = (A, B, E)`
        M = {
            g: r
            for g, r in digraphs.maxMatching(set(A), B, E)
            if isinstance(g, tuple) and all(isinstance(p, str) for p in g)
        }

        # if the size of M matches the size of the input and the game has a referee that is not a player,
        # then a referee was successfully assigned to each game and we return the valid output
        if len(M) == len(A) and not all(r in g for g in A for r in B):
            return M

        # otherwise, the tournament is invalid and we return `None`.
        else:
            return None


def gameGroups(assignedReferees):
    pass


def gameSchedule(assignedReferees, gameAroups):
    pass


def scores(p, s, c, games):
    pass
