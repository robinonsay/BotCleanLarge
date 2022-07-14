import heapq
import math
from collections import namedtuple

Position = namedtuple("Position", ["i", "j"])
Dim = namedtuple("Dim", ["h", "w"])
State = namedtuple("State", ["pos", "dirt"])
Item = namedtuple("Item", ["state", "path", "cost"])
PQItem = namedtuple("PQItem", ["priority", "item"])


def getDirtLocations(grid: list, dim: Dim) -> set:
    """
    Finds all the dirt locations
    O(m*n)
    :param grid: The grid to search
    :return: Set of coordinates of all the dirt locations
    """
    dirt_locs = set()
    for i in range(dim.h):
        for j in range(dim.w):
            if 'd' == grid[i][j]:
                dirt_locs.add(Position(i, j))
    return frozenset(dirt_locs)


def getDist(pos1: Position, pos2: Position) -> float:
    """
    Calculates manhattan distance between two grid points
    :param pos1: Coordinates of first position
    :param pos2: Coordinates of second position
    :return: Euclidean distance of two points
    """
    return abs(pos1.i - pos2.i) + abs(pos1.j - pos2.j)


def heuristic(state: State) -> int:
    """
    This is where the fun begins...
    Uses Nearest neighbor method to calculate heuristic
    :param state: The state to calculate from
    :param dirt_set: Locations of the dirt
    :return: A heuristic value
    """
    # Copies dirt locations to a list
    dirt_list = list(state.dirt)
    estimate = 0
    pos = state.pos
    # While there is dirt in the list
    while len(dirt_list) > 0:
        index, dirt = min(enumerate(dirt_list), key=lambda dirt: getDist(dirt[1], pos))
        # Get the euclidean distance to that dirt
        estimate += getDist(dirt, pos)
        # Move the position to the dirt we just "visited"
        pos = dirt_list.pop(index)
    return estimate


def getSuccessors(state: State, dim: Dim) -> set:
    """
    Gets successor states given the current state
    :param state: The current state
    :param dirt_locs: Location of the dirt
    :return: Set of successor states
    """
    actions = set()
    successors = set()
    if state.pos in state.dirt:
        actions.add("CLEAN")
    if state.pos.i - 1 >= 0:
        actions.add("UP")
    if state.pos.i + 1 < dim.h:
        actions.add("DOWN")
    if state.pos.j - 1 >= 0:
        actions.add("LEFT")
    if state.pos.j + 1 < dim.w:
        actions.add("RIGHT")
    for action in actions:
        successor = None
        if action == "CLEAN":
            newDirt = set(state.dirt)
            newDirt.remove(state.pos)
            successor = (State(state.pos, frozenset(newDirt)), action, 1)
        elif action == "UP":
            successor = (State(Position(state.pos.i - 1, state.pos.j), state.dirt), action, 2)
        elif action == "DOWN":
            successor = (State(Position(state.pos.i + 1, state.pos.j), state.dirt), action, 2)
        elif action == "LEFT":
            successor = (State(Position(state.pos.i, state.pos.j - 1), state.dirt), action, 2)
        elif action == "RIGHT":
            successor = (State(Position(state.pos.i, state.pos.j + 1), state.dirt), action, 2)
        successors.add(successor)
    return successors


def next_move(pos_r: int, pos_c: int, dim_h: int, dim_w: int, grid: list) -> str:
    dim = Dim(dim_h, dim_w)
    # Priority Queue
    pq = []
    # Explored nodes
    explored = set()
    # Gets the location of the dirt
    dirt_set = getDirtLocations(grid, dim)
    # The starting state
    start_state = State(Position(pos_r, pos_c), dirt_set)
    # Set of goal states
    goal_states = set([State(dirt, frozenset()) for dirt in dirt_set])
    # First priority for the start state
    priority = heuristic(start_state)
    heapq.heappush(pq, PQItem(priority, Item(start_state, None, 0)))
    # While pq is not empty...
    while len(pq) != 0:
        # Pop the pq
        _, item = heapq.heappop(pq)
        # Get the items from the pq
        state, path, cost = item
        # If state has already been explored, continue
        if state in explored:
            continue
        # If we reach a goal state, return
        if state in goal_states:
            print(path[0])
            return path[0]
        # Add the state to the set of explored states
        explored.add(state)
        # Remove dirt from the set
        dirt_set -= explored
        # Get successor states
        for nextState, action, stepCost in getSuccessors(state, dim):
            # Calculate new cost
            newCost = cost + stepCost
            # Initialize the path
            newPath = []
            if path is not None:
                newPath = path.copy()
            # Add action to the path we took
            newPath.append(action)
            # Calculate the priority for pq and push onto pq
            priority = heuristic(nextState) + newCost
            item = Item(nextState, newPath, newCost)
            heapq.heappush(pq, PQItem(priority, item))


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    dim = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(dim[0])]
    next_move(pos[0], pos[1], dim[0], dim[1], board)