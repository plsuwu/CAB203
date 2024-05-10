#!/usr/bin/env python
import os
import ast
import unittest
from inspect import getsource
import project as P
from pprint import pprint


scriptDirectory = os.path.dirname(__file__)
allowed_modules = ["csv", "graphs", "digraphs"]


def assert_no_loops(s, f):
    f_ast = ast.parse(getsource(f))
    for node in ast.walk(f_ast):
        if isinstance(node, ast.For):
            s.fail(f'function {f.__name__} uses a for loop.')
        if isinstance(node, ast.While):
            s.fail(f'function {f.__name__} uses a while loop.')



class TestGamesOK(unittest.TestCase):
    def test_noLoops(self):
        assert_no_loops(self, P.gamesOK)

    def test_k33(self):
        games = {(u, v) for u in range(3) for v in range(3, 6)}
        self.assertTrue(P.gamesOK(games))
    #
    def test_triangles(self):
        games = {(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)}
        self.assertTrue(P.gamesOK(games))
    # #
    def test_bad_triangles_1(self):
        games = {
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 4),
            (2, 5),
            (3, 5),
            (0, 5),
        }
        self.assertFalse(P.gamesOK(games))
    #
    def test_5cycle(self):
        games = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)}
        self.assertFalse(P.gamesOK(games))
    #
    def test_k5(self):
        games = {(u, v) for u in range(5) for v in range(5) if u < v}
        self.assertTrue(P.gamesOK(games))


if __name__ == "__main__":
    unittest.main(argv=["-b"])
