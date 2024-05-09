#!/usr/bin/env python
import graphs

V = { 'A', 'B', 'C', 'D', 'E', 'F' }
E = { ('A', 'F'), ('B', 'C'), ('B', 'D'), ('B', 'E'), ('B','F'), ('C', 'F')}
E = E | { (v, u) for (u,v) in E }
u = 'A'

def distances1(V, E, u):
   d = dict()
   for v in V:
      d[v] = graphs.distance(V, E, u, v)

   return d

def distances2(V, E, u):
   return { v: graphs.distance(V, E, u, v) for v in V }

print(distances1(V, E, u))
print(distances2(V, E, u))

def distances3(V, E, u):
   d = dict()
   D = graphs.distanceClasses(V, E, u)

   for dist, distClass in enumerate(D):
      for v in distClass:
         d[v] = graphs.distance(V, E, u, v)

   return d

def distances4(V, E, u):
   D = graphs.distanceClasses(V, E, u)
   return { v: dist  for dist, distClass in enumerate(D)  for v in distClass }

print(distances3(V, E, u))
print(distances4(V, E, u))
