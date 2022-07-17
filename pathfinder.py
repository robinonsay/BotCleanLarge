import heapq
import math
import random
from typing import NamedTuple
from util import GridWorld, Position, Bot

State = NamedTuple("State", [("pos", Position), ("dirt", frozenset[Position])])
StateInfo = NamedTuple("StateInfo", [("state", State), ("path", list[str]), ("cost", int)])
Successor = NamedTuple("Successor", [("state", State), ("action", str), ("step_cost", int)])
PQItem = NamedTuple("PQItem", [("priority", int), ("state_info", StateInfo)])


def getDist(pos1: Position, pos2: Position) -> int:
    """
    Calculates manhattan distance between two grid points
    :param pos1: Coordinates of first position
    :param pos2: Coordinates of second position
    :return: Euclidean distance of two points
    """
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


class DirtVertex:
    flag = Position(-1, -1)

    def __init__(self, pos:Position, cost=math.inf, edge:Position=flag):
        self.pos = pos
        self.cost = cost
        self.edge = edge

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def copy(self):
        return DirtVertex(self.pos, self.cost, self.edge)


class PathFinder:
    def __init__(self, grid_world: GridWorld):
        self.grid_world = grid_world

    @staticmethod
    def _get_heuristic(state: State):
        estimate = len(state.dirt)
        PPQItem = NamedTuple("PPQItem", [("cost", int), ("pos", Position), ("seq", int)])
        rd_heap = list()
        i = 0
        for d in state.dirt:
            rd_heap.append(PPQItem(getDist(d, state.pos), d, i))
            i += 1
        heapq.heapify(rd_heap)
        invalid = set()
        rd_map = dict()
        for item in rd_heap:
            rd_map[item.pos] = (item.cost, item.seq)
        while rd_heap:
            item = heapq.heappop(rd_heap)
            cost, dirt, seq = item
            if item in invalid:
                continue
            estimate += cost
            rd_map.pop(dirt)
            for pos, value in rd_map.items():
                invalid.add(PPQItem(value[0], pos, value[1]))
                c = getDist(pos, dirt)
                heapq.heappush(rd_heap, PPQItem(c, pos, i))
                rd_map[pos] = (c, i)
                i += 1
        return estimate

    def _get_successors(self, state: State) -> Successor:
        bot_pos = state.pos
        actions = list()
        if bot_pos.x > 0:
            actions.append("LEFT")
        if bot_pos.x < (self.grid_world.dim.w - 1):
            actions.append("RIGHT")
        if bot_pos.y > 0:
            actions.append("UP")
        if bot_pos.y < (self.grid_world.dim.h - 1):
            actions.append("DOWN")
        if bot_pos in state.dirt:
            actions.append("CLEAN")
        for action in actions:
            ghost_bot = Bot(state.pos)
            dirt = state.dirt
            step_cost = 1
            if action == "LEFT":
                ghost_bot.left()
            elif action == "RIGHT":
                ghost_bot.right()
            elif action == "UP":
                ghost_bot.up()
            elif action == "DOWN":
                ghost_bot.down()
            elif action == "CLEAN":
                step_cost = 1
                dirt = dirt - {ghost_bot.pos}
            yield Successor(State(ghost_bot.pos, dirt), action, step_cost)

    def get_path(self, depth: int = None) -> list[str]:
        pq = []
        explored = set()
        start_state = State(self.grid_world.get_bot_pos(), self.grid_world.dirt)
        goal_states = set([State(d, frozenset()) for d in self.grid_world.dirt])
        heapq.heappush(pq, PQItem(self._get_heuristic(start_state), StateInfo(start_state, list(), 0)))
        while len(pq) > 0:
            _, item = heapq.heappop(pq)
            # Get the items from the pq
            state, path, cost = item
            if state in explored:
                continue
            # If we reach a goal state, return
            if state in goal_states or (depth is not None and len(path) == depth):
                # print(path)
                return path
            # Add the state to the set of explored states
            explored.add(state)
            for next_state, action, step_cost in self._get_successors(state):
                # Calculate new cost
                new_cost = cost + step_cost
                # Initialize the path
                new_path = path.copy()
                # Add action to the path we took
                new_path.append(action)
                # Calculate the priority for pq and push onto pq
                priority = PathFinder._get_heuristic(next_state) + new_cost
                item = StateInfo(next_state, new_path, new_cost)
                heapq.heappush(pq, PQItem(priority, item))
