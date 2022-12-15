from proboj import *
from util import *


def lemur_with_nothing(self: ProbojPlayer, lemur: Lemur):
    if lemur.stone >= PICKAXE_COST:
        lemur.role = LemurRoles.MINER
        return Turn(Command.CRAFT, Tool.PICKAXE)

    grid = self.world.tiles
    oxygen = self.world.oxygen

    dq = deque()

    seen = set()

    for i in self.myself.lemurs:
        if i.role == LemurRoles.MINER:
            dq.appendleft(((i.y, i.x), i))

    while len(dq):
        t = dq.pop()
        if t[0] in seen:
            continue
        seen.add(t[0])
        y, x = t[0]

        if (lemur.y, lemur.x) == t[0]:
            return movetowards(self, lemur, (t[1].y, t[1].x))

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
