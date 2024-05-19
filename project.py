#!/usr/bin/env python

import graphs
import digraphs
import csv

from functools import reduce
from collections import defaultdict
from typing import Tuple

def gamesOK(games: set) -> bool:
    # each `Tournament` is defined by a set of Bonkers games `A`, a set of players `P`
    #
    # each game `g` is played by a player and their opponent, `(p,o)`, where the game `(p,o)`
    #   is the same as `(o,p)` and `p` is any player from the set of players `P`
    #   and their opponent `o` is any player in `P` other than `p` - in other words, `o` is any item in `P` where `o != p`.
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
                row[n].strip()
                for n in range(1, len(row))
                if row[n] != ""
            )
            for row in reader
            # discard header row
            if row[0].strip() != "Referee"
        }

        # convert set games to a list so iterators over `games` to give them a fixed order
        A = list(games)
        B = set(C.keys())  # referees

        # find the set of edges E with each edge `e = (g, r)` assigning a referee `r` from the
        # set `B` to a game `g` in `A` where `g = (p, p)` and `r = (r: c)` in the set of conflicts
        # `C` such that `r` or any `c` is not also in their assigned `g`
        E = {
            (g, r)
            for g in A
            for r, c in C.items()
            if all(r not in p and u not in p for u in c for p in g)
        }

        # find the maximum matching in the bipartite graph `G = (A | B, E)` such that each edge in E is
        # filtered so that any referee in B is not assigned more than one game from A
        # store the result in `M` as a dictionary such that each game `g` as edge `(p,o)` as the key is
        # assigned a referee `r` as its value
        M = {
            g: r
            for g, r in digraphs.maxMatching(set(A), B, E)
            # if any value `g` is not a tuple of strings then the function is likely wrong anyway
            if isinstance(g, tuple) and all(isinstance(p, str) for p in g)
        }

        # if the size of `M` matches the size of the input and the game has a referee that is not a player,
        # then a referee was successfully assigned to each game and we return the valid output
        if len(M) == len(A) and not all(r in g for g in A for r in B):
            return M

        # otherwise, the tournament is invalid and we return `None`.
        else:
            return None


def gameGroups(
    assignedReferees: dict[Tuple[str, str], str]
) -> list[set[Tuple[str, str]]] | None:

    # build a graph `G = (V, E)` where V is a list of the games and their assigned referees,
    # and E is any edge `e = (u,v)` where u is a game with a referee `u = (player, player), referee`
    # and v is any conflicting game `v = (player, player), referee` such that the size of the intersection
    # `|(u & v)| = 1`

    # create edges `E` as described above:
    # find the intersect of game `u` and game `v` where `u != v`.
    # a vertex `u` forms an edge with a vertex `v` if some element `u` in game `g1 = (player_a, player_b), referee`
    # is also an element in game `g2 = (other_player_a, other_player_b), other_referee`
    E = {
        ((a, b), (c, d)) # (player_a, player_b), (other_player_a, other_player_b)
        for (a, b), r1 in assignedReferees.items()
        for (c, d), r2 in assignedReferees.items()
        if (a, b) != (c, d) # discard identical games
        and (
            # e = (u,v) if `player_a` or `player_b` is `other_player_a` or `other_player_b`
            #           , or if `referee` is `other_player_a` or `other_player_b`
            #           , or `other_referee` is `player_a` or `player_b`
            #
            # for each edge `e` found, ensure it is undirected so that the set of edges `E`
            # can be colored
            a in (c, d) or b in (c, d) or r1 == r2
            or r1 in (c, d) or r2 in (a, b)
        )
    }

    # find the minimum number of colors required for each vertex in
    # `assignedReferees` such that any edge `e1` in E does not share a color
    # with any other edge `e2` in E where `e1 != e2`
    #
    # fix the order of `assignedReferees` by converting to a list so that
    # iterators over keys in `assignedReferees` yield a deterministic output
    k, C = graphs.minColouring(list(assignedReferees), E)

    # create a partition list P where each vertex `u` (C.keys()) into a set of each vertex of the same color `C[u]` and
    # return P
    P = graphs.colourClassesFromColouring(C)
    return P


def gameSchedule(assignedReferees, gameGroups):


    pass


def scores(p, s, c, games):
    pass
