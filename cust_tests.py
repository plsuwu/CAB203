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



# class TestGamesOK(unittest.TestCase):
#     def test_noLoops(self):
#         assert_no_loops(self, P.gamesOK)
#
#     def test_k33(self):
#         games = {(u, v) for u in range(3) for v in range(3, 6)}
#         self.assertTrue(P.gamesOK(games))
#     #
#     def test_triangles(self):
#         games = {(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)}
#         self.assertTrue(P.gamesOK(games))
#     # #
#     def test_bad_triangles_1(self):
#         games = {
#             (0, 2),
#             (0, 3),
#             (0, 4),
#             (1, 3),
#             (1, 4),
#             (1, 5),
#             (2, 4),
#             (2, 5),
#             (3, 5),
#             (0, 5),
#         }
#         self.assertFalse(P.gamesOK(games))
#     #
#     def test_5cycle(self):
#         games = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)}
#         self.assertFalse(P.gamesOK(games))
#     #
#     def test_k5(self):
#         games = {(u, v) for u in range(5) for v in range(5) if u < v}
#         self.assertTrue(P.gamesOK(games))

class TestReferees(unittest.TestCase):
   def test_no_loops(self):
      assert_no_loops(self, P.referees)


   # def test_1(self):
   #    refereecsvfilename = os.path.join(scriptDirectory, 'referees1.csv')
   #    games = { ('Bob', 'Alice'), ('Joe', 'Charlie'), ('Elaine', 'Rene') }
   #    self.assertEqual(P.referees(games, refereecsvfilename), {
   #       ('Bob', 'Alice'): 'Rene',
   #       ('Joe', 'Charlie'): 'David',
   #       ('Elaine', 'Rene'): 'Joe'
   #    })
   #
   #
   # def test_2(self):
   #    refereecsvfilename = os.path.join(scriptDirectory, 'referees1.csv')
   #    games = { ('Bob', 'Alice'), ('Joe', 'Charlie'), ('Ellie', 'Rene') }
   #    self.assertEqual(P.referees(games, refereecsvfilename), None)


   def test_3(self):
      refereecsvfilename = os.path.join(scriptDirectory, 'referees2.csv')
      games = {
         ('Gong Gong', 'Jobu Tupaki'),
         ('Gong Gong', 'Deirdre'),
         ('Joy', 'Waymond'),
         ('Deirdre', 'Jobu Tupaki')
      }
      r = P.referees(games, refereecsvfilename)
      self.assertEqual(r, {
         ('Gong Gong', 'Jobu Tupaki'): 'Deirdre',
         ('Gong Gong', 'Deirdre'): 'Waymond',
         ('Joy', 'Waymond'): 'Gong Gong',
         ('Deirdre', 'Jobu Tupaki'): 'Evalyn'
      })

# {
#         ('Gong Gong', 'Jobu Tupaki'): 'Deirdre',
#  ('Deirdre', 'Jobu Tupaki'): 'Evalyn',
#  ('Joy', 'Waymond'): 'Jobu Tupaki',
#  ('Gong Gong', 'Deirdre'): 'Waymond'}


   def test_4(self):
      refereecsvfilename = os.path.join(scriptDirectory, 'referees3.csv')
      games = {
         ('Spike Spiegel', 'Vicious'),
         ('Jet Black', 'Ein'),
         ('Faye Valentine', 'Edward'),
         ('Edward', 'Julia'),
         ('Ein', 'Faye Valentine'),
         ('Vicious', 'Jet Black'),
         ('Julia', 'Spike Spiegel')
      }
      r = P.referees(games, refereecsvfilename)
      self.assertEqual(r, {
         ('Edward', 'Julia'): 'Faye Valentine',
         ('Ein', 'Faye Valentine'): 'Julia',
         ('Faye Valentine', 'Edward'): 'Vicious',
         ('Jet Black', 'Ein'): 'Spike Spiegel',
         ('Julia', 'Spike Spiegel'): 'Ein',
         ('Spike Spiegel', 'Vicious'): 'Jet Black',
         ('Vicious', 'Jet Black'): 'Edward'
      })


   def test_5(self):
      refereecsvfilename = os.path.join(scriptDirectory, 'referees3.csv')
      games = {
         ('Spike Spiegel', 'Vicious'),
         ('Jet Black', 'Ein'),
         ('Faye Valentine', 'Edward'),
         ('Edward', 'Julia'),
         ('Ein', 'Faye Valentine'),
         ('Vicious', 'Edward'),
         ('Julia', 'Spike Spiegel')
      }
      r = P.referees(games, refereecsvfilename)
      self.assertEqual(r, None)

if __name__ == "__main__":
    unittest.main(argv=["-q"])
