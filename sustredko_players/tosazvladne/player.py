#!/usr/bin/python
from proboj import *
from collections import deque
from queue import PriorityQueue

DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]
point = tuple[int, int]


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "6E57E0"

    def get_name(self) -> str:
        return "to_sa_asi_(ne)zvladne.py"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    """
    - ako daleko su hraci - keeping safe distance === s stickom, noz
    - zabijame ked je niekto vedla nas
    """

    def make_turn(self) -> list[Turn]:
        turns = []
        self.log("make_turn start")
        for lemur in self.myself.lemurs:
            if not lemur.alive:
                turns.append(Turn(Command.NOOP))
                continue
            hladam = TileType.TURBINE if lemur.lemon else TileType.TREE
            turns.append(self.najdi(lemur, hladam))
        self.log(turns)
        return turns

    def mozesPrejst(self, x, y, lemur: Lemur):
        typ = self.world.tiles[y][x].type
        if typ == TileType.EMPTY:
            return 1  # prejdem bez problemov
        elif typ == TileType.TREE:
            return -1  # zober lemon
        elif typ == TileType.STONE or typ == TileType.IRON or typ == TileType.WALL:
            if Tool.PICKAXE in lemur.tools:
                return 2  # vytazit rudu
            elif lemur.stone >= 2:
                return 3  # vytvorit krompac
        elif typ == TileType.TURBINE:
            return -2  # tyrbina
        return 0  # neda sa

    def vykonaj(self, typ: int, pos: point):
        if typ == 1:
            return Turn(Command.MOVE, *pos)
        elif typ == -1:
            return Turn(Command.TAKE, *pos, InventorySlot.LEMON, 1)
        elif typ == -2:
            return Turn(Command.PUT, *pos, InventorySlot.LEMON, 1000)
        elif typ == 2:
            return Turn(Command.BREAK, *pos)
        elif typ == 3:
            return Turn(Command.CRAFT, Tool.PICKAXE)

    def najdi(self, lemur, hladam):
        fronta = deque()
        mriezka = self.world.tiles
        poz_t = tuple[point, int]
        vzdialenosti = [[1000000000 for i in range(
            self.world.width)] for j in range(self.world.height)]
        navstivene: list[list[None | poz_t]] = [[None for i in range(self.world.width)]
                                                for j in range(self.world.height)]
        kam: point | None = None
        odkial = (lemur.x, lemur.y)
        fronta.append(odkial)
        vzdialenosti[odkial[1]][odkial[0]] = 0
        self.log("hladma", hladam)
        while fronta:
            v = fronta.popleft()
            for dir in DIR:
                tu = (v[0] + dir[0], v[1] + dir[1])
                narocnost_prejdenia = self.mozesPrejst(*tu, lemur)
                if not (
                        self.isInRange(tu[1], tu[0]) and
                        not navstivene[tu[1]][tu[0]] and
                        vzdialenosti[tu[1]][tu[0]] > vzdialenosti[v[1]][v[0]]+1 and
                        narocnost_prejdenia and
                        (self.world.oxygen[tu[1]][tu[0]] or self.world.oxygen[v[1]][v[0]])):
                    continue
                vzdialenosti[tu[1]][tu[0]] = vzdialenosti[v[1]][v[0]] + 1
                navstivene[tu[1]][tu[0]] = (v, narocnost_prejdenia)
                if mriezka[tu[1]][tu[0]].type == hladam:
                    kam = tu
                    fronta.clear()
                    break
                if narocnost_prejdenia > 0:
                    fronta.append(tu)

        self.log("kamm", kam)
        if kam is None:
            return Turn(Command.NOOP)
        cesta: list[point] = []
        for _ in range(vzdialenosti[kam[1]][kam[0]]):
            cesta.append(kam)
            kam = navstivene[kam[1]][kam[0]][0]
            self.log(kam)
        cesta.reverse()

        return self.vykonaj(self.mozesPrejst(*cesta[0], lemur), cesta[0])


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
