from proboj import *

RESOURCES = {
    Tool.KNIFE: lambda l: l.iron >= 1,
    Tool.PICKAXE: lambda l: l.stone >= 2,
    TileType.TREE: lambda l: l.stone >= 5
}


class CrafterMixin:
    def craft(self, recipe: Tool, l: Lemur):
        if RESOURCES[recipe](l) and l.tools.count(None) >= 1:
            return Turn(Command.CRAFT, recipe)

    def build(self, recipe: TileType, l: Lemur, target_x, target_y, world: World):
        if target_x is None or target_y is None:
            return None
        if RESOURCES[recipe](l) and world.tiles[target_y][target_x] == TileType.EMPTY:
            return Turn(Command.BUILD, target_x, target_y, recipe)

    def give_slot2(self: ProbojPlayer, l: Lemur):
        if not l.tools[1]:
            return None
        for target in self.myself.lemurs:
            if abs(target.x - l.x) + abs(target.y - l.y) <= 1:
                if target.alive and l.tools[1] not in target.tools and target.tools.count(None) >= 1:
                    return Turn(Command.PUT, target.x, target.y, InventorySlot.TOOL2, 1)
