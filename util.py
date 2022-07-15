import random
from typing import NamedTuple

Position = NamedTuple("Position", [("x", int), ("y", int)])
Dim = NamedTuple("Dim", [("h", int), ("w", int)])


class Bot:
    def __init__(self, pos: Position):
        self._pos = pos

    def __str__(self):
        return self._pos

    def __repr__(self):
        return str(self)

    @property
    def x(self):
        return self._pos.x

    @property
    def y(self):
        return self._pos.y

    @property
    def pos(self):
        return self._pos

    def set_pos(self, pos: Position):
        self._pos = pos

    def up(self):
        self._pos = Position(self._pos.x, self._pos.y - 1)

    def down(self):
        self._pos = Position(self._pos.x, self._pos.y + 1)

    def left(self):
        self._pos = Position(self._pos.x - 1, self._pos.y)

    def right(self):
        self._pos = Position(self._pos.x + 1, self._pos.y)


class GridWorld:
    def __init__(self, dim: Dim = None, grid: list[list[str]] = None, bot: Bot = None):
        if dim is None:
            self._dim = Dim(random.randrange(1, 50), random.randrange(1, 50))
        else:
            self._dim = dim
        self._dirt: set[Position] = set()
        if grid is None:
            items = ['d', '-']
            self._grid = [['-' for j in range(self._dim.w)] for i in range(self._dim.h)]
            for y in range(self._dim.h):
                for x in range(self._dim.w):
                    item = random.choice(items)
                    if item == 'd':
                        self._dirt.add(Position(x, y))
                    self._grid[y][x] = item
        else:
            self._grid = grid
        if bot is None:
            self._bot = Bot(Position(random.randrange(self._dim.w), random.randrange(self._dim.h)))
            if self._grid[self._bot.y][self._bot.x] == '-':
                self._grid[self._bot.y][self._bot.x] = 'b'
        else:
            self._bot = bot

    def __str__(self):
        string = str()
        for row in self._grid:
            for item in row:
                string += item + ' '
            string.removesuffix(' ')
            string += '\n'
        return string

    def __repr__(self):
        return str(self)

    def remove_dirt(self, pos: Position):
        if pos in self._dirt:
            self._dirt.remove(pos)
            if pos == self._bot:
                self._grid[self._bot.y][self._bot.x] = 'b'
            else:
                self._grid[self._bot.y][self._bot.x] = '-'

    def get_bot_pos(self):
        return self._bot.pos

    def dirt_empty(self):
        return len(self._dirt) == 0

    @property
    def dirt(self):
        return frozenset(self._dirt)

    @property
    def grid(self):
        return self._grid.copy()

    @property
    def dim(self):
        return self._dim

    def move_bot(self, action: str) -> Position:
        old_pos = self._bot.pos
        if action == "UP":
            self._bot.up()
        elif action == "DOWN":
            self._bot.down()
        elif action == "LEFT":
            self._bot.left()
        elif action == "RIGHT":
            self._bot.right()
        if old_pos in self._dirt:
            self._grid[old_pos.y][old_pos.x] = 'd'
        else:
            self._grid[old_pos.y][old_pos.x] = '-'
        if self._bot.pos not in self._dirt:
            self._grid[self._bot.y][self._bot.x] = 'b'
        return self._bot.pos
