from proboj import *
from collections import deque
from util import *

def builder(self :ProbojPlayer,lemur:Lemur):
    
    grid=self.world.grid
    oxygen=self.world.oxygen

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

        if grid[y][x].type == TileType.TURBINE:
            turbinedist = t[1]
            turbinecoord = (y, x)
            break

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))

    if turbinecoord is None:
        return STRATEGYFAIL
    
    