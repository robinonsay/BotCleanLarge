import tkinter
import time
from util import Position, Dim, GridWorld
from typing import NamedTuple

GRID_SIZE = 10
World = NamedTuple("World", [("grid_dim", Dim), ("window", tkinter.Tk), ("canvas", tkinter.Canvas)])
TkBot = NamedTuple("TkBot", [("pos", Position), ("bot_id", int)])
Context = NamedTuple("Context", [("world", World), ("grid_world", GridWorld)])


def create_world() -> World:
    # dim = Dim(random.randint(1, 50), random.randint(1, 50))
    dim = Dim(5, 5)
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
    return Context(world, grid_world), bot_id_


def play(context: Context, bot_id_: int):
    time.sleep(5)
    gw = context.grid_world
    print(gw)
    # while not gw.dirt_empty():
    # next_move = bcl.next_move(bot_pos.i, bot_pos.j, world.grid_dim.h, world.grid_dim.w, grid)
    # print(next_move)
    gw.move_bot("DOWN")
    # if next_move == "UP":
    #     x -= 1
    # elif next_move == "DOWN":
    #     x += 1
    # elif next_move == "LEFT":
    #     y -= 1
    # elif next_move == "RIGHT":
    #     y += 1
    # elif next_move == "CLEAN":
    bot_pos = gw.get_bot_pos()
    xy = (bot_pos.x * GRID_SIZE, bot_pos.y * GRID_SIZE)
    context.world.canvas.moveto(bot_id_, *xy)
    context.world.window.update()
    time.sleep(1)


my_world = create_world()
this_context, bot_id = initialize_world(my_world)
play(this_context, bot_id)
my_world.window.mainloop()
