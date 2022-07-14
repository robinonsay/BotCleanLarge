import random
from unittest import TestCase
import bcl


def generate_grid(dim: bcl.Dim):
    items = ['d', '-']
    grid = [[None for j in range(dim.w)] for i in range(dim.h)]
    dirt = set()
    for i in range(dim.h):
        for j in range(dim.w):
            item = random.choice(items)
            if item == 'd':
                dirt.add(bcl.Position(i, j))
            grid[i][j] = item
    pos = bcl.Position(random.randrange(dim.h), random.randrange(dim.w))
    if grid[pos.i][pos.j] == '-':
        grid[pos.i][pos.j] = 'b'
    return pos, grid, dirt


class Test(TestCase):
    def test_get_dirt_locations(self):
        dim = bcl.Dim(1, 1)
        pos, grid, dirt_truth = generate_grid(dim)
        dirt = bcl.getDirtLocations(grid, dim)
        self.assertTrue(dirt == dirt_truth, msg=f"Dirt {dim}: Does not equal truth")
        dim = bcl.Dim(1, 50)
        pos, grid, dirt_truth = generate_grid(dim)
        dirt = bcl.getDirtLocations(grid, dim)
        self.assertTrue(dirt == dirt_truth, msg=f"Dirt {dim}: Does not equal truth")
        dim = bcl.Dim(50, 1)
        pos, grid, dirt_truth = generate_grid(dim)
        dirt = bcl.getDirtLocations(grid, dim)
        self.assertTrue(dirt == dirt_truth, msg=f"Dirt {dim}: Does not equal truth")
        dim = bcl.Dim(random.randint(1, 50), random.randint(1, 50))
        pos, grid, dirt_truth = generate_grid(dim)
        dirt = bcl.getDirtLocations(grid, dim)
        self.assertTrue(dirt == dirt_truth, msg=f"Dirt {dim}: Does not equal truth")

    def test_get_dist(self):
        truth = 20
        pos1 = bcl.Position(11, 11)
        pos2 = bcl.Position(1, 1)
        dist = bcl.getDist(pos1, pos2)
        self.assertTrue(truth == dist, msg=f"dist ({dist}) != truth ({truth})")
        truth = 20
        pos1 = bcl.Position(0, 0)
        pos2 = bcl.Position(0, 20)
        dist = bcl.getDist(pos1, pos2)
        self.assertTrue(truth == dist, msg=f"dist ({dist}) != truth ({truth})")
        truth = 20
        pos1 = bcl.Position(0, 0)
        pos2 = bcl.Position(20, 0)
        dist = bcl.getDist(pos1, pos2)
        self.assertTrue(truth == dist, msg=f"dist ({dist}) != truth ({truth})")

    def test_heuristic_simple(self):
        states = [bcl.State(bcl.Position(0, 0), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(1, 0), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(1, 1), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(1, 2), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(2, 2), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(4, 2), {bcl.Position(4, 4), bcl.Position(4, 2)}),
                  bcl.State(bcl.Position(4, 2), {bcl.Position(4, 4)}),
                  bcl.State(bcl.Position(4, 4), {bcl.Position(4, 4)}),
                  bcl.State(bcl.Position(4, 4), frozenset())]
        for i in range(len(states)-1):
            self.assertTrue(bcl.heuristic(states[i+1]) <= bcl.heuristic(states[i]))

