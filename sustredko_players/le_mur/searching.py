from proboj import *
from utils import inside, D, walkable


def search(l: Lemur, world: World) -> dict[TileType, list[tuple[int, int]]]:
    x, y = l.x, l.y
    grid = world.tiles
    queue, visited = [(x, y)], set()
    dist = {(x, y): 0}
    output = {
        TileType.IRON: [],
        TileType.STONE: [],
        TileType.TREE: [],
        TileType.TURBINE: [],
        TileType.EMPTY: []
    }

    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        if dist[(x, y)] > 100:
            break
        visited.add((x, y))

        if grid[y][x].type in output:
            if grid[y][x].type != TileType.EMPTY or world.oxygen[y][x] > 0:
                output[grid[y][x].type].append((x, y))

        for dx, dy in D:
            if inside(world, x + dx, y + dy) and grid[y + dy][x + dx].type != TileType.UNKNOWN:
                queue.append((x + dx, y + dy))
                if (x + dx, y + dy) not in dist:
                    dist[(x + dx, y + dy)] = dist[(x, y)] + 1
    return output


def step_to(world: World, players: list[Player], to_x, to_y, l: Lemur, distance_limit=float("inf")):
    x, y = l.x, l.y
    queue, visited = [(x, y)], set()
    parent, dist = {}, {(x, y): 0}
    if (to_x, to_y) == (l.x, l.y):
        return None

    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        if dist[(x, y)] > 100:
            return None
        visited.add((x, y))
        if x == to_x and y == to_y:
            break

        for dx, dy in D:
            new_x, new_y = x + dx, y + dy
            if inside(world, new_x, new_y) and (walkable(world, players, new_x, new_y)
                                                or (new_x, new_y) == (to_x, to_y)):
                queue.append((new_x, new_y))
                if (new_x, new_y) not in parent:
                    parent[(new_x, new_y)] = (x, y)
                if (new_x, new_y) not in dist:
                    dist[(new_x, new_y)] = dist[(x, y)] + 1
                    if dist[(new_x, new_y)] + 1 >= distance_limit:
                        return None

    if (to_x, to_y) not in visited:
        return None
    target = (to_x, to_y)
    while parent[target] != (l.x, l.y):
        target = parent[target]
    return target


def distance(world: World, players: list[Player], to_x, to_y, l: Lemur) -> int:
    x, y = l.x, l.y
    queue, visited = [(x, y)], set()
    shortest = {(x, y): 0}

    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        if shortest[(x, y)] >= 100:
            return float("inf")
        visited.add((x, y))
        if x == to_x and y == to_y:
            break

        for dx, dy in D:
            new_x, new_y = x + dx, y + dy
            if inside(world, new_x, new_y) and (walkable(world, players, new_x, new_y)
                                                or (new_x, new_y) == (to_x, to_y)):
                queue.append((new_x, new_y))
                shortest[(new_x, new_y)] = min(shortest.get((new_x, new_y), float("inf")),
                                               shortest[(x, y)] + 1)
    return shortest.get((to_x, to_y), float('inf'))


def absolute_distance(world: World, to_x, to_y, l: Lemur) -> int:
    x, y = l.x, l.y
    queue, visited = [(x, y)], set()
    shortest = {(x, y): 0}

    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if x == to_x and y == to_y:
            break

        for dx, dy in D:
            new_x, new_y = x + dx, y + dy
            if inside(world, new_x, new_y) and (world.tiles[new_y][x].type == TileType.EMPTY
                                                or (new_x, new_y) == (to_x, to_y)):
                queue.append((new_x, new_y))
                shortest[(new_x, new_y)] = min(shortest.get((new_x, new_y), float("inf")),
                                               shortest[(x, y)] + 1)
    return shortest.get((to_x, to_y), float('inf'))
