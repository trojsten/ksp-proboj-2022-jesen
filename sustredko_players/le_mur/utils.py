from proboj import *

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def inside(world: World, x, y):
    return 0 <= x < world.width and 0 <= y < world.height


def walkable(world: World, players: list[Player], x, y):
    for p in players:
        for l in p.lemurs:
            if l.x == x and l.y == y:
                return False
    return world.tiles[y][x].type == TileType.EMPTY and world.oxygen[y][x] > 0


def no_knife(step: tuple[int, int], players: list[Player], myself: Player):
    x, y = step
    for player in players:
        if player == myself:
            continue
        for lemur in player.lemurs:
            if lemur.alive and lemur.x == x and lemur.y == y and Tool.KNIFE in lemur.tools:
                return False
    return True


def nearest_turbine_lemons(self: ProbojPlayer, l: Lemur, search: dict):
        turbine = search[TileType.TURBINE]
        if not turbine:
            return 10
        x, y = turbine[0]
        if not self.world.tiles[y][x].type == TileType.TURBINE:
            return 10
        return self.world.tiles[y][x].lemon


def everyone_has_item(lemurs, item: Tool):
    for lemur in lemurs:
        if item not in lemur.tools and lemur.alive:
            return False
    return True


def knife_safe(world: World, x, y, players: list[Player], myself: Player):
    for dx, dy in ((2, 0), (0, 2), (-2, 0), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        new_x, new_y = x + dx, y + dy
        if inside(world, new_x, new_y) and not no_knife((new_x, new_y), players, myself):
            return False
    return True


def all_lemurs(players: list[Player], myself: Player) -> list[Lemur]:
    lemur_list = []
    for player in players:
        if player == myself:
            continue
        lemur_list.extend(player.lemurs)
    return lemur_list


def enum_to_str(x):
    try:
        return x.name
    except AttributeError:
        return x
