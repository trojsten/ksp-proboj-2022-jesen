from proboj import *
from util import *
from give_to_beggar import *


def communist_trader(self, lemur):

    donor = {}
    acceptor = {}

    self.players[i].lemurs

    for lem in self.myself.lemurs:
        if lem == lemur:
            continue
        if lem.iron > KNIFE_COST or (lem.iron > 0 and Tool.KNIFE in lem.tools):
            donor[(lem.y, lem.x)] = lem
        if lem.iron < KNIFE_COST and Tool.KNIFE not in lem.tools:
            acceptor[(lem.y, lem.x)] = lem

    grid = self.world.tiles
    oxygen = self.world.oxygen

    dq = deque()
    seen = set()

    dq.append(((lemur.y, lemur.x), 0))
    l_dist = 0
    l_coord = 0

    while len(dq):
        t = dq.pop()

        if t[0] in seen:
            continue

        seen.add(t[0])
        y, x = t[0]

        if (y, x) in donor.keys() or (
            lemur.iron > KNIFE_COST and (y, x) in acceptor.keys()
        ):
            return Turn(Command.MOVE, t[0][1], t[0][0])

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
