from proboj import *
from collections import deque
from util import *


def kamikadze(self, lemur: Lemur):


    grid = self.world.tiles
    oxygen = self.world.oxygen
    dq = deque()
    seen = set()

    for i in range(4):
        self.log("a")
        nx = lemur.x + DIRECTIONS[i]
        ny = lemur.y + DIRECTIONS[(i + 1) % 4]

        if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
            self.log("b")
            continue

        self.log(grid[ny][nx].type)
        if grid[ny][nx].type == TileType.TURBINE:
            self.log(0)
            if lemur.progress == 0:
                if grid[nx][ny].lemon == 0:
                    lemur.progress = 1

                else:
                    self.log(4)
                    lemur.progress = 1
                    return Turn(
                        Command.TAKE, nx, ny, InventorySlot.LEMON, grid[nx][ny].lemon
                    )
            if lemur.progress == 1:
                lemur.progress = 2
                return Turn(Command.BREAK, nx, ny)
    if lemur.progress == 2:
        lemur.progress = 3
        self.log("AAAAAAAAA")
        return Turn(Command.CRAFT, Tool.KNIFE)
    if lemur.progress == 3:
        lemur.progress = 4
        lemur.role = LemurRoles.GARDENER
        return Turn(Command.CRAFT, Tool.JUICER)

    dq.append(((lemur.y, lemur.x), 0))

    turbine = None

    while len(dq):
        t = dq.pop()

        if t[0] in seen:
            continue

        seen.add(t[0])
        y, x = t[0]

        if grid[y][x].type == TileType.TURBINE:
            turbine = (y, x)

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))
    if turbine is None:
        self.log("wtf")
        lemur.role = LemurRoles.GARDENER
        return STRATEGYFAIL
    else:
        return movetowards(self, lemur, turbine)


def shouldikamikadze(self: ProbojPlayer, lemur: Lemur):
    return False
    self.log(12)
    if not Tool.PICKAXE in lemur.tools:
        return False
    grid = self.world.tiles
    oxygen = self.world.oxygen
    dq = deque()
    seen = set()

    dq.append(((lemur.y, lemur.x), 0))

    turbines = 0
    friends = 0
    opponents = 0

    while len(dq):
        t = dq.pop()

        if t[0] in seen:
            continue

        seen.add(t[0])
        y, x = t[0]

        if grid[y][x].type == TileType.TURBINE:
            turbines += 1

        if (y, x) != (lemur.y, lemur.x) and grid[y][x].type != TileType.EMPTY:
            continue

        if oxygen[y][x] == 0:
            continue

        for i in range(4):
            nx = x + DIRECTIONS[i]
            ny = y + DIRECTIONS[(i + 1) % 4]

            if nx < 0 or nx >= self.world.width or ny < 0 or ny >= self.world.height:
                continue

            dq.appendleft(((ny, nx), t[1] + 1))
    for i in self.players:
        for j in i.lemurs:
            if (j.y, j.x) in seen:
                if i == self.myself:
                    friends += 1
                else:
                    opponents += 1
    self.log(turbines)

    if turbines != 1:
        return False

    self.log(opponents, friends)
    return opponents >= friends
