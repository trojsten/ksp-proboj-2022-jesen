#!/usr/bin/python
from collections import deque

from proboj import *
from lemon_move import *
from utils import *
from bfs import *


#D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


turnTimer = 0
krompace = 10


class MyPlayer(ProbojPlayer):

    def get_color(self) -> str:

        return "ff00ff"

    def get_name(self) -> str:
        return "eeh"

    def make_turn_lemon(self, l):
        for dx, dy in D:
            if notSegfault(self,l.x + dx, l.y + dy) and self.world.tiles[l.y + dy][l.x + dx].type == TileType.TREE:
                if self.world.tiles[l.y + dy][l.x + dx].has_lemon:
                    return Turn(Command.TAKE, l.x + dx, l.y + dy, InventorySlot.LEMON, 1)
        stromy = self.find_building(TileType.TREE)
        return move_like_bfs(self,bfs(self,stromy, l), l.x, l.y, l)

    def find_building(self, type):
        out = []
        for y in range(self.world.height):
            for x in range(self.world.width):
                if self.world.tiles[y][x].type == type:
                    out.append(((x, y), 0))
        return out

    def find_enemy_lemurs(self):
        res = []
        for player in self.players:
            if player == self.myself:
                continue
            for l in player.lemurs:
                if l.alive:
                    res.append(((l.x, l.y), 0))
        return res

    def find_ally_lemurs_bez_krompaca(self, lem):
        res = []
        for l in self.myself.lemurs:
            if l != lem and not l.have_tool(Tool.PICKAXE):
                res.append(((l.x, l.y), 0))
        return res


    def make_turn_knife(self, l):
        lemurs = self.find_enemy_lemurs()
        # Ak mám nôž zabíjam
        if l.have_tool(Tool.KNIFE):
            self.log("zabijam")
            for dx, dy in D:
                if notSegfault(self,l.x + dx, l.y + dy) and (l.x + dx, l.y + dy) in [l[0] for l in lemurs]:
                    return Turn(Command.STAB, l.x + dx, l.y + dy)
            vzd = bfs(self, lemurs, l)
            if vzd[l.y][l.x] == inf:
                return self.make_turn_zberac(l)
            return move_like_bfs(self,vzd, l.x, l.y, l)

        # ak mám iron craftím nôž

        if l.iron > 0 and not l.have_tool(Tool.KNIFE):
            self.log("craftim")
            return Turn(Command.CRAFT, Tool.KNIFE)

        # inak idem ťažiť iron

        self.log("tazim")

        for dx, dy in D:
            if notSegfault(self,l.x + dx, l.y + dy) and self.world.tiles[l.y + dy][l.x + dx].type == TileType.IRON:
                return Turn(Command.BREAK, l.x + dx, l.y + dy)

        for dx, dy in D:
            if notSegfault(self,l.x + dx, l.y + dy) and self.world.tiles[l.y + dy][l.x + dx].type == TileType.STONE:
                return Turn(Command.BREAK, l.x + dx, l.y + dy)

        irons = self.find_building(TileType.IRON)
        stone = self.find_building(TileType.STONE)
        stone = [(p, h+3) for p, h in stone]
        irons.extend(stone)
        return move_like_bfs(self,bfs(self,irons, l), l.x, l.y, l)

    def make_turn_zberac(self, l):
        if l.lemon == 0:
            return self.make_turn_lemon(l)
        else:
            # turns.append(Turn(Command.NOOP))
            return self.make_turn_turbine(l)


    def make_turn_krompac(self, l):
        if not l.have_tool(Tool.PICKAXE) and l.stone >= 2:
            self.log("craftim")
            return Turn(Command.CRAFT, Tool.PICKAXE)

        if l.stone >= 2:
            self.log("nosim")
            for dx, dy in D:
                for l2 in self.myself.lemurs:
                    if not l2.have_tool(Tool.PICKAXE) and l2.x == l.x+dx and l2.y == l.y+dy:
                        return Turn(Command.PUT, l.x+dx, l.y+dy, InventorySlot.STONE, 2)
            return move_like_bfs(self, bfs(self, self.find_ally_lemurs_bez_krompaca(l), l), l.x, l.y, l)

        if l.have_tool(Tool.PICKAXE):
            self.log("tazim")
            for dx, dy in D:
                if self.world.tiles[l.y+dy][l.x+dx].type == TileType.STONE:
                    return Turn(Command.BREAK, l.x+dx, l.y+dy)
            return move_like_bfs(self, bfs(self, self.find_building(TileType.STONE), l), l.x, l.y, l)

        return self.make_turn_zberac(l)

    def lemur_bez_krompaca(self):
        for l in self.myself.lemurs:
            if not l.have_tool(Tool.PICKAXE):
                return True
        return False

    def make_turn(self) -> list[Turn]:
        global turnTimer
        turnTimer += 1
        turns = []

        if turnTimer < krompace and self.lemur_bez_krompaca():
            self.log("krompace")
            for l in self.myself.lemurs:
                turns.append(self.make_turn_krompac(l))

        else:
            turns.append(self.make_turn_knife(self.myself.lemurs[0]))
            for l in self.myself.lemurs[1:]:
                turns.append(self.make_turn_zberac(l))

        return turns

    def make_turn_turbine(self, l):
        for dx, dy in D:
            if notSegfault(self,l.x + dx, l.y + dy) and self.world.tiles[l.y + dy][l.x + dx].type == TileType.TURBINE:
                return Turn(Command.PUT, l.x + dx, l.y + dy, InventorySlot.LEMON, l.lemon)
        turbiny = self.find_building(TileType.TURBINE)
        return move_like_bfs(self,bfs(self,turbiny, l), l.x, l.y, l)


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
