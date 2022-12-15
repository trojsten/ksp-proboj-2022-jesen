from proboj import *
from utils import D, inside, knife_safe, no_knife, all_lemurs
from searching import step_to, distance


class SurvivalistMixin:
    def interact_turbine_tree(self: ProbojPlayer, l: Lemur):
        # Interact with the neighboring tree or turbine
        for dx, dy in D:
            new_x, new_y = l.x + dx, l.y + dy
            if inside(self.world, new_x, new_y) and knife_safe(self.world, l.x, l.y, self.players, self.myself):
                tile = self.world.tiles[new_y][new_x]
                if tile.type == TileType.TREE and tile.has_lemon:
                    return Turn(Command.TAKE, new_x, new_y, InventorySlot.LEMON, 1)
                elif tile.type == TileType.TURBINE and l.lemon > 0:
                    return Turn(Command.PUT, new_x, new_y, InventorySlot.LEMON, 1)

    def go_to_lemon_tree(self: ProbojPlayer, l: Lemur, search: dict):
        # Go to the nearest tree that has lemon
        for tree in search[TileType.TREE]:
            if self.world.tiles[tree[1]][tree[0]].has_lemon and l.lemon == 0:
                if (step := step_to(self.world, self.players, tree[0], tree[1], l, distance_limit=100)) \
                        and knife_safe(self.world, step[0], step[1], self.players, self.myself):
                    return Turn(Command.MOVE, step[0], step[1])

    def go_to_turbine(self: ProbojPlayer, l: Lemur, search: dict):
        # Go to nearest turbine
        for turbine in search[TileType.TURBINE]:
            if (step := step_to(self.world, self.players, turbine[0], turbine[1], l, distance_limit=100)) \
                    and knife_safe(self.world, step[0], step[1], self.players, self.myself):
                return Turn(Command.MOVE, step[0], step[1])

    def run_away_from_knives(self: ProbojPlayer, l: Lemur):
        #  Run away from knives if nothing else to do
        if not knife_safe(self.world, l.x, l.y, self.players, self.myself):
            for dx, dy in D:
                new_x, new_y = l.x + dx, l.y + dy
                if inside(self.world, new_x, new_y) \
                        and knife_safe(self.world, new_x, new_y, self.players, self.myself):
                    return Turn(Command.MOVE, new_x, new_y)

    def wait_for_pickaxe(self: ProbojPlayer, l: Lemur):
        for lemur in self.myself.lemurs:
            if abs(l.x - lemur.x) + abs(l.y - lemur.y) <= 1 and lemur.tools[1] == Tool.PICKAXE:
                return Turn(Command.NOOP)

        if Tool.PICKAXE not in l.tools:
            return Turn(Command.NOOP)
