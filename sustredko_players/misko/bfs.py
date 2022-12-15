
from utils import *
import heapq

zratane = {}


def bfs(p, ciely, l):

    if (str(ciely), l.have_tool(Tool.PICKAXE), (l.have_tool(Tool.JUICER) and l.lemon > 1)) in zratane:
        return zratane[(str(ciely), l.have_tool(Tool.PICKAXE), l.lemon > 1)]

    vis = [[inf for _ in range(p.world.width)] for _ in range(p.world.height)]
    Q = [(v, p) for p,v in ciely]

    heapq.heapify(Q)

    while len(Q):
        v, (x, y) = heapq.heappop(Q)
        for i in range(4):
            if prechodne(p,x + DX[i], y + DY[i]) and kyslik(p,x + DX[i], y + DY[i], l) and vis[y + DY[i]][x + DX[i]] == inf:
                vis[y + DY[i]][x + DX[i]] = v + 1
                heapq.heappush(Q, (v+1, (x + DX[i], y + DY[i])))
            if l.have_tool(Tool.PICKAXE) and prechodne_pickaxe(p,x + DX[i], y + DY[i]) and vis[y + DY[i]][x + DX[i]] == inf:
                vis[y + DY[i]][x + DX[i]] = v + 1.5
                heapq.heappush(Q, (v+1.5, (x + DX[i], y + DY[i])))
    zratane[(str(ciely), l.have_tool(Tool.PICKAXE), l.lemon > 1)] = vis
    return vis


def move_like_bfs(p,vzd, x, y, l):
    if vzd[y][x] == 1 or vzd[y][x] == inf:
        p.log("vzd 1 or inf")
        return Turn(Command.NOOP)

    opt = []

    for dx, dy in D:
        if kyslik(p,x + dx, y + dy, l) and vzd[y][x] > vzd[y + dy][x + dx]:
            opt.append((vzd[y + dy][x + dx], x+dx, y+dy, prechodne(p, x+dx, y+dy)))

    opt = sorted(opt)
    for h, x, y, p in opt:
        if p:
            return Turn(Command.MOVE,x, y)
        elif l.have_tool(Tool.PICKAXE):
            return Turn(Command.BREAK, x, y)



    return Turn(Command.NOOP)