#!/usr/bin/python
import random
import traceback
from typing import Callable

from proboj import *

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Role:
    FARM = 2 ** 6
    PRIMARY = 2 ** 7
    BACKUP = 2 ** 5


class Route:
    path: list[tuple[int, int]] = []
    target: tuple[int, int] = (0, 0)
    execute: Callable[[], Turn] | Turn | None = None
    targetCondition: Callable[[Tile], bool] | None = None
    lastCheck: int = 0

    def __init__(self, path: list[tuple[int, int]], target: tuple[int, int],
                 execute: Callable[['MyPlayer'], Turn] | Turn | None = None,
                 targetCondition: Callable[[Tile], bool] | None = None):
        self.path = path
        self.target = target
        self.execute = execute
        self.targetCondition = targetCondition


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "%06x" % random.randint(0, 0xFFFFFF)

    def get_name(self) -> str:
        return "Adam_Záhradník"

    lemur = None
    lemurId = None

    total_lemurs: int
    alive_lemurs = 0
    roles: list[int] = []
    routes: list[Route | None] = []
    firstMove = True

    safe = dict()
    turbines = []
    move = 0
    move_limit = 150

    dev = False

    def dist(self, f: tuple[int, int], t: tuple[int, int]):
        return abs(f[0] - t[0]) + abs(f[1] - t[1])

    def is_neighbour(self, x: int, y: int, tx: int, ty: int) -> bool:
        return abs(x - tx) + abs(y - ty) == 1

    def in_bounds(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def is_occupied(self, x, y, *valid: tuple[int, int]):
        if (x, y) in valid:
            return False

        for p in self.players:
            for l in p.lemurs:
                if l == self.lemur:
                    continue
                if l.x == x and l.y == y:
                    return True

        return False

    def is_safe(self, x, y, lemur=None):
        if lemur is not None and lemur.have_tool(Tool.JUICER) and lemur.lemon > 0:
            return True

        if self.world.oxygen[y][x] == 0:
            return False
        return True
    #

    def nearest(self, checker: Callable[[Tile], bool]) -> tuple[tuple[int, int], Tile, int]:
        # bfs search self.world for nearest tileType
        # return coordinates, tile and distance
        q = [(self.lemur.x, self.lemur.y, 0)]
        visited = set()
        while q:
            x, y, d = q.pop(0)

            visited.add((x, y))

            if checker(self.world.tiles[y][x]):
                return (x, y), self.world.tiles[y][x], d

            for dx, dy in D:
                nx, ny = x + dx, y + dy

                if (nx, ny) in visited:
                    continue
                if not self.in_bounds(nx, ny):
                    continue
                if self.is_occupied(nx, ny) and not checker(self.world.tiles[ny][nx]):
                    continue
                if not self.is_safe(nx, ny, self.lemur):
                    continue

                q.append((nx, ny, d + 1))

    def nearest_tile(self, type: TileType) -> tuple[tuple[int, int], Tile, int]:
        return self.nearest(lambda tile: tile.type == type)

    #

    def create_path(self, origin, target, lemur: Lemur | None = None) -> list[tuple[int, int]]:
        # TODO: optimise

        self.log("new path", origin, target)

        q = [(origin[0], origin[1], 0)]
        visited = dict()
        while q:
            x, y, d = q.pop(0)

            visited[(x, y)] = d
            if (x, y) == target:
                c = target
                res = []

                def findLowest(x, y):
                    lowest = None
                    ld = None
                    for dx, dy in D:
                        if not (x + dx, y + dy) in visited:
                            continue
                        if lowest == None or visited[(x + dx, y + dy)] < lowest:
                            lowest = visited[(x + dx, y + dy)]
                            ld = (dx, dy)
                    return (x + ld[0], y + ld[1])

                while c != origin:
                    c = findLowest(*c)
                    res.append(c)

                res = res[:-1]

                self.log("path", res)

                return res

            for dx, dy in D:
                nx, ny = x + dx, y + dy

                if (nx, ny) in visited:
                    continue
                if not self.in_bounds(nx, ny):
                    continue
                if not self.is_safe(nx, ny, lemur):
                    continue
                if (self.is_occupied(nx, ny) or self.world.tiles[ny][nx].type != TileType.EMPTY) and not (nx, ny) == target:
                    continue

                q.append((nx, ny, d + 1))

    def kill_lemur(self) -> Turn:
        # find closest hostile lemur, use bfs
        # remember first move

        self.log("kill lemur")

        hostiles = []
        for p in self.players:
            if p == self.myself:
                continue
            for l in p.lemurs:
                if l.alive:
                    hostiles.append(l)

        if not hostiles:
            return Turn(Command.NOOP)

        def bfs():
            nonlocal hostiles
            q = [(self.lemur.x, self.lemur.y, (self.lemur.x, self.lemur.y), 0)]
            visited = set()

            while q:
                x, y, from_, d = q.pop(0)

                if d > 10:
                    return None

                visited.add((x, y))

                for l in hostiles:
                    if l.x == x and l.y == y:
                        # found
                        return from_

                for dx, dy in D:
                    nx, ny = x + dx, y + dy

                    if (nx, ny) in visited:
                        continue
                    if not self.in_bounds(nx, ny):
                        continue
                    if self.is_occupied(nx, ny):
                        continue

                    q.append((nx, ny, from_, d + 1))

        f = bfs()
        if f is None:
            if self.nextRandom is not None:
                nr = self.nextRandom
                self.nextRandom = None
                nx, ny = self.lemur.x + nr[0], self.lemur.y + nr[1]
                if self.in_bounds(nx, ny) and not self.is_occupied(nx, ny) and self.is_safe(nx, ny) and self.world.tiles[ny][nx].type == TileType.EMPTY:
                    return Turn(Command.MOVE, nr[0], nr[1])
            # move randomly
            self.log("move randomly")
            SD = D.copy()
            random.shuffle(SD)

            for dx, dy in SD:
                nx, ny = self.lemur.x + dx, self.lemur.y + dy

                if not self.in_bounds(nx, ny):
                    continue
                if not self.is_safe(nx, ny):
                    continue
                if self.is_occupied(nx, ny):
                    continue

                self.log("move randomly", nx, ny)

                self.nextRandom = (dx, dy)

                return Turn(Command.MOVE, nx, ny)
            self.log("move randomly failed")
            return Turn(Command.NOOP)
        if self.is_neighbour(f, self.lemur.x, self.lemur.y, *f):
            return Turn(Command.STAB, f[0], f[1])
        else:
            return Turn(Command.MOVE, f[0], f[1])

    nextRandom = None

    #

    def first_move(self):
        self.total_lemurs = len(self.myself.lemurs)
        for i in range(self.total_lemurs):
            if self.myself.lemurs[i].have_tool(Tool.PICKAXE):
                self.roles.append(Role.PRIMARY)
            else:
                self.roles.append(0)
            self.routes.append(None)
        self.roles[-1] |= Role.FARM

    def validate_primary(self):
        # get id from roles which is primary
        i = next((i for i, v in enumerate(self.roles) if v & Role.PRIMARY), -1)
        # if primary is not alive, set new primary to first backup
        if i == -1 or not self.myself.lemurs[i].alive:
            if i != -1:
                self.roles[i] = 0
            i = next((i for i, v in enumerate(self.roles) if v & Role.BACKUP), -1)
            if i != -1:
                if self.alive_lemurs > 1:
                    self.roles[i] = Role.PRIMARY
                else:
                    self.roles[i] = Role.FARM | Role.PRIMARY
                self.primary = {
                    "hasItems": False,
                    "crafting": False,
                    "ready": False,
                    "giveTarget": -1
                }

    def make_turn(self) -> list[Turn]:
        self.logid = None
        if self.dev and self.move >= self.move_limit:
            self.log("move limit reached")
            while True:
                pass
        self.move += 1
        if self.firstMove:
            self.first_move()
            self.firstMove = False

        # count alive lemurs
        for l in self.myself.lemurs:
            if l.alive:
                self.alive_lemurs += 1

        self.validate_primary()

        turns = []
        for id, lemur in enumerate(self.myself.lemurs):
            if not lemur.alive:
                turns.append(Turn(Command.NOOP))
                continue

            self.lemur = lemur
            self.lemurId = id
            self.logid = id

            try:
                turn = self.lemur_turn(lemur, id)
            except Exception as e:
                self.log(e)
                traceback.print_exc(None, sys.stderr)
                turn = Turn(Command.NOOP)
                if self.dev:
                    exit(-1)
            turns.append(turn)

        return turns

    def follow_path(self, lemur, id):
        path = self.routes[id]
        if path is not None:
            if len(path.path) > 0:
                if path.targetCondition is not None and path.lastCheck < self.move - 1:
                    if not path.targetCondition(self.world.tiles[path.target[1]][path.target[0]]):
                        self.routes[id] = None
                        self.log("Path no longer valid")
                        return None

            if len(path.path) == 1:
                if path.path[-1] != (lemur.x, lemur.y):
                    # self.log("moveB", *path.path[-1])
                    return Turn(Command.MOVE, *path.path[-1])
                else:
                    self.routes[id] = None
                    self.log("Path complete, running end function")
                    if path.execute is not None:
                        if type(path.execute) == Turn:
                            self.log("Executing turn", path.execute)
                            return path.execute
                        else:
                            self.log("Executing function")
                            t = path.execute()
                            self.log("returned", t)
                            return t
            else:
                if path.path[-1] == (lemur.x, lemur.y):
                    path.path.pop()
                x, y = path.path[-1]
                if self.is_neighbour(lemur.x, lemur.y, x, y):
                    # self.log("move", x, y)
                    return Turn(Command.MOVE, x, y)
                else:
                    self.routes[id] = None
                    self.log("ERROR path not adjacent")

    def lemur_turn(self, lemur, id) -> Turn:
        turn = self.follow_path(lemur, id)
        if turn is not None:
            return turn

        if self.roles[id] & Role.FARM != 0:
            nearest_tree = self.nearest(lambda tile: tile.type == TileType.TREE and tile.has_lemon)
            current = (self.lemur, self.lemurId)
            # temporarily replace lemur with a primary lemur
            primaryId = next((i for i, v in enumerate(self.roles) if v & Role.PRIMARY), -1)
            if primaryId != -1:
                self.lemur = self.myself.lemurs[primaryId]
                self.lemurId = primaryId

            nearest_turbine = self.nearest_tile(TileType.TURBINE)
            turbine_lemons = nearest_turbine[1].lemon if nearest_turbine is not None else None

            self.lemur = current[0]
            self.lemurId = current[1]

            if nearest_turbine is not None and (
                    turbine_lemons <= 1 or turbine_lemons * 8 < nearest_turbine[2]) and self.lemur.lemon > 0:
                if self.is_neighbour(lemur.x, lemur.y, nearest_turbine[0][0], nearest_turbine[0][1]):
                    turn = Turn(Command.PUT, *nearest_turbine[0], InventorySlot.LEMON, self.lemur.lemon)
                else:
                    path = self.create_path((lemur.x, lemur.y), nearest_turbine[0])
                    self.routes[id] = Route(path, nearest_turbine[0],
                                            lambda: Turn(Command.PUT, *nearest_turbine[0], InventorySlot.LEMON,
                                                        self.lemur.lemon))
                    last = self.routes[id].path[-1]
                    turn = Turn(Command.MOVE, *last)
            elif nearest_tree is not None:
                if self.is_neighbour(lemur.x, lemur.y, nearest_tree[0][0], nearest_tree[0][1]):
                    turn = Turn(Command.TAKE, *nearest_tree[0], InventorySlot.LEMON, 1)
                else:
                    path = self.create_path((lemur.x, lemur.y), nearest_tree[0])
                    self.routes[id] = Route(path, nearest_tree[0],
                                            Turn(Command.TAKE, *nearest_tree[0], InventorySlot.LEMON, 1),
                                            lambda tile: tile.type == TileType.TREE and tile.has_lemon)
                    last = self.routes[id].path[-1]
                    turn = Turn(Command.MOVE, *last)
            else:
                self.log("No turbines need lemons and no trees have lemons")
                pass

        if self.roles[id] & Role.PRIMARY != 0 and turn is None:
            self.log("Primary lemur")
            # check if we have knife
            if self.primary["ready"]:
                self.log("Going to attack")
                # follow and kill other lemurs
                # check if we are next to another lemur which isn't ours
                turn = self.kill_lemur()
            else:
                if self.lemur.iron >= 1 and self.lemur.stone >= 3:
                    self.log("Items ready")
                    self.primary["hasItems"] = True

                if self.primary["crafting"]:
                    self.log("Crafting")
                    if self.lemur.have_tool(Tool.KNIFE):
                        if self.lemur.have_tool(Tool.JUICER):
                            self.primary["ready"] = True
                            self.primary["crafting"] = False
                            self.primary["hasItems"] = False
                            self.log("Primary is ready")
                        else:
                            self.log("Primary crafting juicer")
                            turn = Turn(Command.CRAFT, Tool.JUICER)
                    else:
                        self.log("Primary crafting knife")
                        turn = Turn(Command.CRAFT, Tool.KNIFE)
                elif self.primary["hasItems"]:
                    if self.lemur.have_tool(Tool.PICKAXE):
                        # give pickaxe to next living lemur that isn't backup or farmer
                        # if none, discard pickaxe
                        self.log("Giving pickaxe")
                        target = -1
                        for i in range(self.total_lemurs):
                            if i != id and self.roles[i] & Role.PRIMARY == 0 and self.roles[i] & Role.FARM == 0 and self.myself.lemurs[i].alive:
                                target = i
                                break
                        if target == -1:
                            self.log("Primary discarding pickaxe")
                            turn = Turn(Command.DISCARD, InventorySlot.TOOL1, 1)
                            self.primary["crafting"] = True
                        else:
                            self.log("Primary giving pickaxe to", target)
                            pos = self.myself.lemurs[target].x, self.myself.lemurs[target].y
                            if self.is_neighbour(lemur.x, lemur.y, pos[0], pos[1]):
                                turn = Turn(Command.PUT, *pos, InventorySlot.TOOL1, 1)
                            else:
                                path = self.create_path((lemur.x, lemur.y), pos)
                                self.routes[id] = Route(path, pos,
                                                        Turn(Command.PUT, *pos, InventorySlot.TOOL1, 1))
                                last = self.routes[id].path[-1]
                                turn = Turn(Command.MOVE, *last)

                    else:
                        self.primary["crafting"] = True
                        self.log("Ready to craft")
                else:
                    # mine until we have 1 iron and 3 stone
                    if self.lemur.iron >= 1:
                        self.log("Primary has iron, mining stone (" + str(self.lemur.stone) + "/3)")
                        stone = self.nearest_tile(TileType.STONE)
                        if self.is_neighbour(lemur.x, lemur.y, stone[0][0], stone[0][1]):
                            turn = Turn(Command.BREAK, *stone[0])
                        else:
                            path = self.create_path((lemur.x, lemur.y), stone[0])
                            self.routes[id] = Route(path, stone[0], Turn(Command.BREAK, *stone[0]))
                            last = self.routes[id].path[-1]
                            turn = Turn(Command.MOVE, *last)
                    else:
                        self.log("Primary mining iron (" + str(self.lemur.iron) + "/1)")
                        iron = self.nearest_tile(TileType.IRON)
                        if self.is_neighbour(lemur.x, lemur.y, iron[0][0], iron[0][1]):
                            turn = Turn(Command.BREAK, *iron[0])
                        else:
                            path = self.create_path((lemur.x, lemur.y), iron[0])
                            self.routes[id] = Route(path, iron[0], Turn(Command.BREAK, *iron[0]))
                            last = self.routes[id].path[-1]
                            turn = Turn(Command.MOVE, *last)
        if turn is None:
            self.log("ERROR no turn")
            turn = Turn(Command.NOOP)

        self.log(turn)

        return turn

    primary = {
        "hasItems": False,
        "crafting": False,
        "ready": False,
        "giveTarget": -1
    }

if __name__ == "__main__":
    p = MyPlayer()
    p.run()
