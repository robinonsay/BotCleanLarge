import heapq
import random
from typing import NamedTuple
from util import GridWorld, Position, Bot

State = NamedTuple("State", [("pos", Position), ("dirt", frozenset[Position])])
StateInfo = NamedTuple("StateInfo", [("state", State), ("path", list[str]), ("cost", int)])
Successor = NamedTuple("Successor", [("state", State), ("action", str), ("step_cost", int)])
PQItem = NamedTuple("PQItem", [("priority", int), ("state_info", StateInfo)])


def getDist(pos1: Position, pos2: Position) -> float:
    """
    Calculates manhattan distance between two grid points
    :param pos1: Coordinates of first position
    :param pos2: Coordinates of second position
    :return: Euclidean distance of two points
    """
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


class PathFinder:
    def __init__(self, grid_world: GridWorld):
        self.grid_world = grid_world

    def _get_heuristic(self, state: State):
        weight = 1.5
        INF = 2**31-1
        PPQItem = NamedTuple("PPQItem", [("c", int), ("v", Position)])
        estimate = len(state.dirt) * weight
        remaining_dirt = [PPQItem(INF, d) for d in state.dirt]
        remaining_dirt.append(PPQItem(INF, state.pos))
        while remaining_dirt:
            c, pos = heapq.heappop(remaining_dirt)
            dirt = min(remaining_dirt, key=lambda d: getDist(pos, d))

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
                priority = self._get_heuristic(next_state) + new_cost
                item = StateInfo(next_state, new_path, new_cost)
                heapq.heappush(pq, PQItem(priority, item))
