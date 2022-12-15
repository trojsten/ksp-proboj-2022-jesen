from proboj import *
from utils import D, inside, knife_safe, no_knife, all_lemurs
from searching import step_to, distance


class MinerMixin:
    def mine_block(self: ProbojPlayer, l: Lemur):
        for dx, dy in D:
            new_x, new_y = l.x + dx, l.y + dy
            if inside(self.world, new_x, new_y) \
                    and knife_safe(self.world, l.x, l.y, self.players, self.myself):
                tile = self.world.tiles[new_y][new_x]
                if tile.type == TileType.IRON or tile.type == TileType.STONE:
                    return Turn(Command.BREAK, new_x, new_y)

    def go_to_nearest_resource(self: ProbojPlayer, l: Lemur, search, resource: TileType, distance_limit=float("inf")):
        if resource not in search:
            return None
        for block in search[resource]:
            if (step := step_to(self.world, self.players, block[0], block[1], l)) \
                    and knife_safe(self.world, step[0], step[1], self.players, self.myself):
                if distance(self.world, self.players, block[0], block[1], l) <= distance_limit:
                    return Turn(Command.MOVE, step[0], step[1])
