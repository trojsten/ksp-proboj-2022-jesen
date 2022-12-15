from proboj import *
D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]
inf = 2 ** 32


def notSegfault(p, x, y):
    return x >= 0 and x < p.world.width and y >= 0 and y < p.world.height


def prechodne(p, x, y):
    return notSegfault(p,x, y) and p.world.tiles[y][x].type == TileType.EMPTY

def prechodne_pickaxe(p, x, y):
    return notSegfault(p, x, y) and p.world.tiles[y][x].type in [TileType.EMPTY, TileType.IRON, TileType.STONE,
                                                                                          TileType.UNKNOWN,
                                                                                          TileType.WALL]

def kyslik(p, x, y, l):
    return notSegfault(p, x, y) and (p.world.oxygen[y][x] > 0 or (l.have_tool(Tool.JUICER) and l.lemon > 0))
