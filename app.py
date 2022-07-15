import tkinter
import time
from util import Position, Dim, GridWorld
from typing import NamedTuple
from pathfinder import PathFinder

GRID_SIZE = 20
World = NamedTuple("World", [("grid_dim", Dim), ("window", tkinter.Tk), ("canvas", tkinter.Canvas)])
TkBot = NamedTuple("TkBot", [("pos", Position), ("bot_id", int)])
Context = NamedTuple("Context", [("world", World), ("grid_world", GridWorld), ("dirt_map", dict[Position, int])])


def create_world() -> World:
    # dim = Dim(random.randint(1, 50), random.randint(1, 50))
    dim = Dim(10, 10)
    window = tkinter.Tk()
    window.title("BotCleanLarge Grid World")
    window.geometry(f'{dim.w * GRID_SIZE}x{dim.h * GRID_SIZE}')
    canvas = tkinter.Canvas(window, height=dim.h * GRID_SIZE, width=dim.w * GRID_SIZE)
    canvas.configure(bg="White")
    canvas.pack(fill="both", expand=True)
    world = World(dim, window, canvas)
    for i in range(0, dim.h * GRID_SIZE, GRID_SIZE):
        canvas.create_line(Position(0, i), Position(dim.w*GRID_SIZE-1, i))
    for j in range(0, dim.w * GRID_SIZE, GRID_SIZE):
        canvas.create_line(Position(j, 0), Position(j, dim.h*GRID_SIZE-1))
    return world


def initialize_world(world: World):
    grid_world = GridWorld(world.grid_dim)
    dirt_map = dict()
    for d in grid_world.dirt:
        x1y1 = (d.x * GRID_SIZE, d.y * GRID_SIZE)
        x2y2 = ((d.x + 1) * GRID_SIZE, (d.y + 1) * GRID_SIZE)
        dirt_map[d] = world.canvas.create_rectangle(x1y1, x2y2, fill="black")
    pos = grid_world.get_bot_pos()
    x1y1 = (pos.x * GRID_SIZE, pos.y * GRID_SIZE)
    x2y2 = ((pos.x + 1) * GRID_SIZE, (pos.y + 1) * GRID_SIZE)
    bot_id_ = world.canvas.create_rectangle(x1y1, x2y2, fill="red")
    world.window.update()
    return Context(world, grid_world, dirt_map), bot_id_


def play(context: Context, bot_id_: int):
    gw = context.grid_world
    print(gw)
    pf = PathFinder(gw)
    moves = pf.get_path()
    for move in moves:
        context.world.canvas.itemconfig(bot_id_, fill="red")
        if move == "UP":
            gw.move_bot("UP")
        elif move == "DOWN":
            gw.move_bot("DOWN")
        elif move == "LEFT":
            gw.move_bot("LEFT")
        elif move == "RIGHT":
            gw.move_bot("RIGHT")
        elif move == "CLEAN":
            gw.remove_dirt(gw.get_bot_pos())
            context.world.canvas.delete(context.dirt_map[gw.get_bot_pos()])
            context.world.canvas.itemconfig(bot_id_, fill="blue")
        bot_pos = gw.get_bot_pos()
        xy = (bot_pos.x * GRID_SIZE, bot_pos.y * GRID_SIZE)
        context.world.canvas.moveto(bot_id_, *xy)
        context.world.window.update()
        time.sleep(0.5)


my_world = create_world()
this_context, bot_id = initialize_world(my_world)
play(this_context, bot_id)
my_world.window.mainloop()
