from proboj import *


def make_turn_lemon(p, l):
    for dx, dy in D:
        if self.notSegfault(l.x + dx, l.y + dy) and self.world.tiles[l.y + dy][l.x + dx].type == TileType.TREE:
            if self.world.tiles[l.y + dy][l.x + dx].has_lemon:
                return Turn(Command.TAKE, l.x + dx, l.y + dy, InventorySlot.LEMON, 1)
    stromy = self.find_building(TileType.TREE)
    self.log(stromy)
    return self.move_like_bfs(self.bfs(stromy), l.x, l.y)