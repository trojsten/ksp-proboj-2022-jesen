from proboj import *
from collections import deque
from util import *
from oberac import *


def miner(self: ProbojPlayer, lemur: Lemur):
    grid = self.world.tiles
    oxygen = self.world.oxygen

    for i in range(4):
        nx = lemur.x + DIRECTIONS[i]
        ny = lemur.y + DIRECTIONS[(i + 1) % 4]

        if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
            continue

        if grid[ny][nx].type in (TileType.STONE,):
            return Turn(Command.BREAK, nx, ny)

        if grid[ny][nx].type in (TileType.IRON,):
            return Turn(Command.BREAK, nx, ny)

    dq = deque()

    seen = set()

    dq.append(((lemur.y, lemur.x), 0))

    edge = {}

    while len(dq):
        t = dq.pop()
        if t[0] in seen:
            continue
        seen.add(t[0])
        y, x = t[0]

        if grid[y][x].type in (TileType.STONE, TileType.IRON, TileType.WALL):
            edge[t[0]] = t[1] - (5 if grid[y][x].type == TileType.IRON else 0)
            continue

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))

    if len(edge) == 0:
        lemur.role = LemurRoles.GARDENER
        return STRATEGYFAIL

    arr = [(edge[i], i) for i in edge]
    arr.sort()

    return movetowards(self, lemur, arr[0][1])
