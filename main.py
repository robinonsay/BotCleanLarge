"""
Meet the bot MarkZoid. It's a cleaning bot whose sensor is a head mounted camera
and whose actuators are the wheels beneath it. It's used to clean the floor.

The bot here is positioned at the top left corner of a 5*5 grid.
Your task is to move the bot to clean all the dirty cells.

Input Format

The first line contains two space separated integers which indicate the current position of the bot.
The board is indexed using Matrix Convention
5 lines follow representing the grid. Each cell in the grid is represented
by any of the following 3 characters:
    'b' (ascii value 98) indicates the bot's current position
    'd' (ascii value 100) indicates a dirty cell
    '-' (ascii value 45) indicates a clean cell in the grid

**Note If the bot is on a dirty cell, the cell will still have 'd' on it**

Output Format:

The output is the action that is taken by the bot in the current step,
and it can be either one of the movements in 4 directions or
cleaning up the cell in which it is currently located.
The valid output strings are LEFT, RIGHT, UP and DOWN or CLEAN.
If the bot ever reaches a dirty cell, output CLEAN to clean the dirty cell.
Repeat this process until all the cells on the grid are cleaned.

Sample Input #00:

0 0
b---d
-d--d
--dd-
--d--
----d
Sample Output #00:

RIGHT

Resultant state:

-b--d
-d--d
--dd-
--d--
----d
"""
import heapq
import math
from collections import namedtuple

Position = namedtuple("Position", ["i", "j"])
State = namedtuple("State", ["pos", "num_dirt"])
Item = namedtuple("Item", ["state", "path", "cost"])
PQItem = namedtuple("PQItem", ["priority", "item"])
BOARD_SIZE = 5


def getDirtLocations(grid: list) -> set:
    """
    Finds all the dirt locations
    O(m*n)
    :param grid: The grid to search
    :return: Set of coordinates of all the dirt locations
    """
    dirt_locs = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if 'd' == grid[i][j]:
                dirt_locs.add(Position(i, j))
    return dirt_locs


def getDist(pos1: Position, pos2: Position) -> float:
    """
    Calculates euclidean distance between two grid points
    :param pos1: Coordinates of first position
    :param pos2: Coordinates of second position
    :return: Euclidean distance of two points
    """
    return math.sqrt((pos1.i - pos2.i)**2 + (pos1.j - pos2.j)**2)


def heuristic(state: State, dirt_set: set) -> int:
    """
    This is where the fun begins...
    Uses Nearest neighbor method to calculate heuristic
    :param state: The state to calculate from
    :param dirt_set: Locations of the dirt
    :return: A heuristic value
    """
    # Copies dirt locations to a list
    dirt_list = list(dirt_set)
    estimate = 0
    pos = state.pos
    # While there is dirt in the list
    while len(dirt_list) > 0:
        closest_dirt = min(dirt_list, key=lambda dirt: getDist(dirt, pos))
        index = 0
        for i in range(len(dirt_list)):
            if dirt_list[i] == closest_dirt:
                index = i
                break
        # Get the euclidean distance to that dirt
        estimate += getDist(closest_dirt, pos)
        # Move the position to the dirt we just "visited"
        pos = dirt_list.pop(index)
    return estimate


def getSuccessors(state: State, dirt_locs: set) -> set:
    """
    Gets successor states given the current state
    :param state: The current state
    :param dirt_locs: Location of the dirt
    :return: Set of successor states
    """
    actions = set()
    successors = set()
    pos = state.pos
    if pos in dirt_locs:
        actions.add("CLEAN")
    if pos.i - 1 >= 0:
        actions.add("UP")
    if pos.i + 1 < BOARD_SIZE:
        actions.add("DOWN")
    if pos.j - 1 >= 0:
        actions.add("LEFT")
    if pos.j + 1 < BOARD_SIZE:
        actions.add("RIGHT")
    for action in actions:
        successor = None
        if action == "CLEAN":
            successor = (State(state.pos, state.num_dirt - 1), action, 1)
        elif action == "UP":
            successor = (State(Position(pos.i - 1, pos.j), state.num_dirt), action, 2)
        elif action == "DOWN":
            successor = (State(Position(pos.i + 1, pos.j), state.num_dirt), action, 2)
        elif action == "LEFT":
            successor = (State(Position(pos.i, pos.j - 1), state.num_dirt), action, 2)
        elif action == "RIGHT":
            successor = (State(Position(pos.i, pos.j + 1), state.num_dirt), action, 2)
        successors.add(successor)
    return successors


def next_move(posr: int, posc: int, grid: list) -> str:
    """
    Calculates the next move given the position of the robot and the grid using A*
    :param posr: Row poisition
    :param posc: Column poisition
    :param grid: The grid
    :return: The next move to make
    """
    # Priority Queue
    pq = []
    # Explored nodes
    explored = set()
    # Gets the location of the dirt
    dirt_set = getDirtLocations(grid)
    # The starting state
    start_state = State(Position(posr, posc), len(dirt_set))
    # Set of goal states
    goal_states = set([State(dirt, 0) for dirt in dirt_set])
    # First priority for the start state
    priority = heuristic(start_state, dirt_set) + 0
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
        for nextState, action, stepCost in getSuccessors(state, dirt_set):
            # Calculate new cost
            newCost = cost + stepCost
            # Initialize the path
            newPath = []
            if path is not None:
                newPath = path.copy()
            # Add action to the path we took
            newPath.append(action)
            # Calculate the priority for pq and push onto pq
            priority = heuristic(nextState, dirt_set) + newCost
            item = Item(nextState, newPath, newCost)
            heapq.heappush(pq, PQItem(priority, item))


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)