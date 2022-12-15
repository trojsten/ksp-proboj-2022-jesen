from proboj import *
from collections import deque
from heapq import *


DIRECTIONS = [0, 1, 0, -1]
PICKAXE_COST = 2
KNIFE_COST = 1
STRATEGYFAIL = None


class LemurRoles:  # id su aj move priority
    KAMIKADZE = -100
    GARDENER = 1
    WARRIOR = 2
    BEGGAR = 3
    MINER = 4
    BROKE = 5
    TRADER = 6


# DIRS = [
#     (y - 1, x - 1),
#     (y - 1, x),
#     (y - 1, x + 1),
#     (y, x - 1),
#     (y, x),
#     (y, x + 1),
#     (y + 1, x - 1),
#     (y + 1, x),
#     (y + 1, x + 1),
# ]


def movetowards(self, lemur, to):
    blocked = set()
    for i in self.players:
        for lem in i.lemurs:
            blocked.add((lem.y, lem.x))
    grid = self.world.tiles
    oxygen = self.world.oxygen

    dq = deque()

    for i in range(4):
        nx = lemur.x + DIRECTIONS[i]
        ny = lemur.y + DIRECTIONS[(i + 1) % 4]

        if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
            continue

        if grid[ny][nx].type == TileType.EMPTY:
            dq.append(((ny, nx), (ny, nx)))

    seen = set()

    while len(dq):
        t = dq.pop()
        if t[0] in seen:
            continue
        seen.add(t[0])
        y, x = t[0]

        if to == t[0]:
            return Turn(Command.MOVE, t[1][1], t[1][0])

        if grid[y][x].type != TileType.EMPTY:
            continue

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1]))
    return STRATEGYFAIL


NOTHING = 0
KNIFEEXTRA = -2
BONKEXTRA = -4


def dangerlevels(self: ProbojPlayer):
    world = self.world
    players = self.players

    h = world.height
    w = world.width

    dists = [[0] * w for _ in range(h)]

    q = []
    seen = set()

    for i in players:
        if i == self.myself:
            continue
        for lemur in i.lemurs:
            x = lemur.x
            y = lemur.y
            if Tool.STICK in lemur.tools:
                dist = BONKEXTRA
            elif Tool.KNIFE in lemur.tools:
                dist = KNIFEEXTRA
            else:
                dist = NOTHING
            heappush(q, (dist, (y, x)))

    while q:
        t = q.pop()
        if t[1] in seen:
            continue
        seen.add(t[1])
        y, x = t[1]

        dists[y][x] = t[0]

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dst = 1 if world.tiles[ny][nx].type == TileType.EMPTY else 2

            heappush(q, (t[0] + dst, (ny, nx)))

    return dists
