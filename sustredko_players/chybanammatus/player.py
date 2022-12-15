#!/usr/bin/python
from proboj import *
from collections import deque

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
INVALID_POS = (-1, -1)


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "1C36ED"

    def get_name(self) -> str:
        return "Alica_vola_s_matusom"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def path_to_sth(self, x, y, goal_x, goal_y):
        queue = deque()
        vis = [[INVALID_POS] * self.world.width for i in range(self.world.height)]
        cur, goal = (x, y), (goal_x, goal_y)
        queue.append(cur)
        while queue and cur != goal:
            cur = queue.popleft()
            for dx, dy in D:
                nx, ny = dx + cur[0], dy + cur[1]
                if (
                    self.isInRange(nx, ny)
                    and vis[ny][nx] == INVALID_POS
                    and self.world.oxygen[ny][nx] > 0
                ):
                    vis[ny][nx] = cur
                    # self.log(f'from {cur_x} {curw_y} to {nx} {ny}')
                    queue.append((nx, ny))

        if cur != goal:
            return -1, -1

        # self.log("ciel", cur_x, cur_y)
        while cur != (x, y):
            old, cur = cur, vis[cur[1]][cur[0]]
            # self.log("parent of", cur_x,cur_y,"is",old_x,old_y)
        return old

    def bfs(self, x, y, goal) -> list:
        queue = deque()
        vis = [[False] * self.world.width for i in range(self.world.height)]
        queue.append((x, y))
        # self.log("start:",x,y)
        while queue:
            x, y = queue.popleft()
            # self.log(f'x: {x}, y: {y}')
            for dx, dy in D:
                nx, ny = x + dx, y + dy
                if (
                    self.isInRange(nx, ny)
                    and not vis[ny][nx]
                    and self.world.oxygen[ny][nx] > 0
                ):
                    t = self.world.tiles[ny][nx].type
                    # self.log(type(t),t)
                    if t == TileType.EMPTY:
                        queue.append((nx, ny))
                        vis[ny][nx] = True
                        # self.log("emptyyyyyyy")
                    elif t == goal:
                        return (nx, ny)
                    # else:
                    # self.log(x,y,t)

        # self.log(f'returning {wanted_trees} and {wanted_turbine}')
        return INVALID_POS

    def is_next_to(self, fir_x, fir_y, sec_x, sec_y):
        return abs(fir_x - sec_x) + abs(fir_y - sec_y) == 1

    # def log(self, *args):
    #     pass

    def make_turn_unsafe(self) -> list[Turn]:
        turns = []
        for i, lemur in enumerate(self.myself.lemurs, start=1):
            self.log(i, "novy lemur", lemur.x, lemur.y)
            turn = Turn(Command.NOOP)
            trees = self.bfs(lemur.x, lemur.y, TileType.TREE)
            turbs = self.bfs(lemur.x, lemur.y, TileType.TURBINE)
            irons = self.bfs(lemur.x, lemur.y, TileType.IRON)
            self.log("tree:",trees)
            self.log("turbine:",turbs)
            if i >= 2:
                self.log(lemur)
                if not lemur.lemon:
                    if self.is_next_to(
                        lemur.x, lemur.y, *trees
                    ):  # abs(lemur.x - trees[1] + lemur.y - trees[0]) == 1
                        self.log("tree:", *trees)
                        self.log("lemur:", lemur.x, lemur.y)
                        turn = Turn(Command.TAKE, *trees, InventorySlot.LEMON, 1)
                        self.log("taken lemon", lemur.lemon)
                    else:
                        spravna_cesta = self.path_to_sth(lemur.x, lemur.y, *trees)
                        self.log("spravna cesta", spravna_cesta)
                        if spravna_cesta == INVALID_POS:
                            continue
                        # self.log("posunutie",*spravna_cesta)
                        # self.log("som tu",lemur.y, lemur.x)
                        if self.is_next_to(lemur.x, lemur.y, *spravna_cesta):
                            turn = Turn(Command.MOVE, *spravna_cesta)
                            self.log("posunul sa")
                        else:
                            self.log(
                                "neni vedla neho XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                            )

                else:
                    if self.is_next_to(
                        lemur.x, lemur.y, *turbs
                    ):  # abs(lemur.x - trees[1] + lemur.y - trees[0]) == 1
                        self.log("tree:", *turbs)
                        self.log("lemur:", lemur.x, lemur.y)
                        turn = Turn(Command.PUT, *turbs, InventorySlot.LEMON, 1)
                        self.log("putted lemon", lemur.lemon)
                    else:
                        spravna_cesta = self.path_to_sth(lemur.x, lemur.y, *turbs)
                        if spravna_cesta[0] == INVALID_POS:
                            continue
                        # self.log("posunutie",*spravna_cesta)
                        # self.log("som",lemur.y, lemur.x)
                        if self.is_next_to(lemur.x, lemur.y, *spravna_cesta):
                            turn = Turn(Command.MOVE, *spravna_cesta)
                            self.log("posunul sa")
                        else:
                            self.log(
                                "neni vedla neho XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                            )

            else:
                if not lemur.have_tool(Tool.KNIFE):
                    # if lemur.tools[Lemur.tool_index(Tool.KNIFE)] == None:
                    if lemur.iron == 0:
                        if self.is_next_to(lemur.x, lemur.y, *irons):
                            turn = Turn(Command.BREAK, *irons)
                        else:
                            if irons == INVALID_POS:
                                turn = Turn(Command.NOOP)
                            else:
                                self.log(lemur.x, lemur.y, *irons)
                                path_to_iron = self.path_to_sth(
                                    lemur.x, lemur.y, *irons
                                )
                                if self.world.tiles[path_to_iron[1]][path_to_iron[0]].type == TileType.EMPTY:
                                    turn = Turn(Command.MOVE, *path_to_iron)
                                else:
                                    turn = Turn(Command.BREAK, *path_to_iron)

                    else:
                        turn = Turn(Command.CRAFT, Tool.KNIFE)

                else:
                    self.log("mam noz")
                    for opp in self.players:
                        if opp == self.myself:
                            pass
                        else:
                            for opp_lemur in opp.lemurs:
                                if self.is_next_to(
                                    opp_lemur.x, opp_lemur.y, lemur.x, lemur.y
                                ):
                                    turn = Turn(Command.STAB, opp_lemur.x, opp_lemur.y)

            turns.append(turn)
            self.log()

        return turns

    def make_turn(self) -> list[Turn]:
        try:
            return self.make_turn_unsafe()
        except Exception as err:
            self.log(err)
            raise err
        return []


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
