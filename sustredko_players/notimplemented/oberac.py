from proboj import *
from util import *

from heapq import *
from collections import deque


DIRECTIONS = [0, 1, 0, -1]
LEMON_RESPAWN = 10
TURBINE_REFILL = 8
BREATHLESS = 3


class StructObserver:
    blocked = []  # coords, who blocks
    structs = (
        {}
    )  # keys: (y, x) world coordinates of object, vals: time passed since last player interaction

    # trees, turbines = [], {}
    trees = {}  # keys: (y, x), vals: times since last take
    turbines = {}  # keys: (y, x), vals: number of lemons

    def __init__(self, map):
        self.update_timers(map)

    def update_timers(self, world):
        # to_view = set(self.structs.keys())

        for y in range(world.height):
            for x in range(world.width):
                tile_type = world.tiles[y][x].type
                if tile_type == TileType.TREE:
                    if (y, x) in self.trees.keys():
                        self.trees[(y, x)] += 1
                    else:
                        self.trees[(y, x)] = 0

                elif tile_type == TileType.TURBINE:
                    if (y, x) in self.turbines.keys():
                        self.turbines[(y, x)][0] += 1

                        if self.turbines[(y, x)][0] >= TURBINE_REFILL:
                            self.turbines[(y, x)][1] = max(
                                0, self.turbines[(y, x)][1] - 1
                            )
                            self.turbines[(y, x)][0] = 0

                    else:
                        self.turbines[(y, x)] = [0, world.tiles[y][x].lemon]

    def user_interaction(self, y, x, n=0):
        if (y, x) in self.turbines.keys():
            self.turbines[(y, x)][1] += n
            
        elif (y, x) in self.trees.keys():
            self.trees[(y, x)] = 0


def harvest(self, lemur: Lemur, observer):

    self.log("harv")

    grid = self.world.tiles
    oxygen = self.world.oxygen

    for i in range(4):
        nx = lemur.x + DIRECTIONS[i]
        ny = lemur.y + DIRECTIONS[(i + 1) % 4]

        if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
            continue

        if grid[ny][nx].type == TileType.TURBINE:
            if lemur.lemon > 0:
                observer.user_interaction(ny, nx, lemur.lemon)
                return Turn(Command.PUT, nx, ny, InventorySlot.LEMON, lemur.lemon)

        if grid[ny][nx].type == TileType.TREE:
            if grid[ny][nx].has_lemon:
                observer.user_interaction(ny, nx)
                return Turn(Command.TAKE, nx, ny, InventorySlot.LEMON, 1)

    # K TURBINEEEEEEE

    dq = deque()
    seen = set()

    dq.append(((lemur.y, lemur.x), 0))

    turbinedist = 0
    turbinecoord = None

    while len(dq):
        t = dq.pop()

        if t[0] in seen:
            continue

        seen.add(t[0])
        y, x = t[0]

        self.log(t)

        if grid[y][x].type == TileType.TURBINE:
            turbinedist = t[1]
            turbinecoord = (y, x)
            break

        self.log(t)

        if oxygen[y][x] == 0:
            continue

        self.log(t)
        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))

    if turbinecoord is None:
        self.log("FUUUUUCK", len(seen))
        return STRATEGYFAIL

    # K STROMOMMMM
    dq = deque()
    seen = set()

    dq.append(((lemur.y, lemur.x), 0))

    trees = {}

    for i in observer.blocked:
        if i[1] == lemur.id:
            observer.blocked.remove(i)

    while len(dq):
        t = dq.pop()

        if t[0] in seen:
            continue

        seen.add(t[0])
        y, x = t[0]

        if grid[y][x].type == TileType.TREE:
            for i in observer.blocked:
                if i[0] == (y, x):
                    continue
            # self.log(
            #    (
            #        turbinedist + 2 * t[1],
            #        TURBINE_REFILL * (1 + observer.turbines[turbinecoord][1])
            #        - observer.turbines[turbinecoord][0],
            #    )
            # )
            if (
                turbinedist + 2 * t[1]
                <= TURBINE_REFILL * (1 + observer.turbines[turbinecoord][1])
                - observer.turbines[turbinecoord][0]
            ):
                trees[t[0]] = max(t[1], LEMON_RESPAWN - observer.trees[(y, x)])

        if grid[y][x].type != TileType.EMPTY:
            continue

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))

    if len(trees) == 0:
        move = movetowards(self, lemur, turbinecoord)
        return move

    arr = [(trees[i], i) for i in trees]
    arr.sort()
    observer.blocked.append((arr[0][1], lemur.id))
    return movetowards(self, lemur, arr[0][1])
