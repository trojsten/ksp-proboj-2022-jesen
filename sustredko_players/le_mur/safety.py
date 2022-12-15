from proboj import *


class SafetyMixin:
    ...
    # def feed_turbine_if_low(self: ProbojPlayer, l: Lemur, search: dict):
    #     turbine = search[TileType.TURBINE]
    #     if not turbine:
    #         return
    #     x, y = turbine[0]
    #     if not self.world.tiles[y][x].type == TileType.TURBINE:
    #         return
    #     if self.world.tiles[y][x].lemon <= 2:
    #         return
