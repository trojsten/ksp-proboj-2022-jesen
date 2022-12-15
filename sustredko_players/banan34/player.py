#!/usr/bin/python
from proboj import *
from collections import deque

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def create_mat(w, h, v):
    return [[v for _ in range(w)] for _ in range(h)]


global state
state = []


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "#FF0000"

    def get_name(self) -> str:
        return "IsielLemurNaVandrovku"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def closest(self, start):
        start = [int(i) for i in start]
        q = deque()
        q.append([start[1], start[0]])

        tiles = self.world.tiles
        ans = {k: [10 ** 10] * 3 for k in
               (TileType.TREE, TileType.IRON, TileType.STONE, TileType.TURBINE)}  # closest tree/rock/turbine/
        vzdialenosti = create_mat(self.world.width, self.world.height, int(1e9))
        # self.log(q)

        vzdialenosti[start[1]][start[0]] = 0

        while q:
            cur = q.popleft()
            for dx, dy in D:
                y, x = cur[0] + dy, cur[1] + dx

                dist = vzdialenosti[cur[0]][cur[1]] + 1
                if not self.isInRange(x, y) or tiles[y][x].type == TileType.UNKNOWN or vzdialenosti[y][x] <= dist:
                    continue
                vzdialenosti[y][x] = dist
                # todo should not add to bfs if turbine or tree or not empty and doesn't have pickaxe
                q.append([y, x])
                tile_type = tiles[y][x].type
                if tile_type in ans:
                    ans[tile_type] = min(ans[tile_type], [vzdialenosti[y][x], x, y])
        return ans

    def closenem(self, start):
        start = [int(i) for i in start]
        q = deque()
        q.append([start[1], start[0]])

        tiles = self.world.tiles
        ans = {k: [10 ** 10] * 3 for k in
               (TileType.TREE, TileType.IRON, TileType.STONE, TileType.TURBINE)}  # closest tree/rock/turbine/
        vzdialenosti = create_mat(400, 400, int(1e9))
        # self.log(q)

        vzdialenosti[start[1]][start[0]] = 0

        while q:
            cur = q.popleft()
            for dx, dy in D:
                y, x = cur[0] + dy, cur[1] + dx

                dist = vzdialenosti[cur[0]][cur[1]] + 1
                if not self.isInRange(x, y) or tiles[y][x].type == TileType.UNKNOWN or vzdialenosti[y][x] <= dist:
                    continue
                vzdialenosti[y][x] = dist
                # todo should not add to bfs if turbine or tree or not empty and doesn't have pickaxe
                q.append([y, x])
                tile_type = tiles[y][x].type
                if tile_type in ans:
                    ans[tile_type] = min(ans[tile_type], [vzdialenosti[y][x], x, y])
        return ans

    def bfs(self, start, end):
        #self.log(end)
        if end[0] > self.world.width * self.world.height:
            return -1, -1

        UNSEEN = -1
        start = tuple(start)
        os = start
        t = self.world.tiles
        prev = create_mat(400, 400, (-1, -1))
        self.log(start)
        self.log(len(prev), len(prev[0]))
        prev[start[0]][start[1]] = [start[0], start[1]]
        start = [start]
        while start:
            new = []
            for curpos in start:
                for xh, yh in D:
                    xn = curpos[0] + xh
                    yn = curpos[1] + yh
                    if [xn, yn] == end:
                        prev[end[0]][end[1]] = curpos
                    if self.isInRange(xn, yn) and t[yn][xn].type == TileType.EMPTY and prev[xn][yn][0] == UNSEEN:
                        new.append([xn, yn])
                        prev[xn][yn] = curpos
            start = new
            if prev[end[0]][end[1]][0] != UNSEEN:
                break
        h = end
        if prev[end[0]][end[1]][0] == UNSEEN:
            return -1, -1
        while prev[h[0]][h[1]] != os:
            h = prev[h[0]][h[1]]
        return h

    def farmer(self, poz, my_tree, lem):
        turn = Turn(Command.NOOP)
        #self.log(my_tree, "tree")
        #self.log(poz, "poz")
        # self.log(turn)
        ans = MyPlayer.closest(self, poz)
        if lem < 3:
            if ans[TileType.TREE][0] == 1:
                turn = Turn(Command.TAKE, ans[TileType.TREE][1], ans[TileType.TREE][2], InventorySlot.LEMON, 1)
            else:
                move = MyPlayer.bfs(self, poz, my_tree)
                #self.log(move, "move")
                turn = Turn(Command.MOVE, move[0], move[1])
                if (move[0] == -1):
                    turn = Turn(Command.NOOP)
        else:
            if ans[TileType.TURBINE][0] == 1:
                turn = Turn(Command.PUT, ans[TileType.TURBINE][1], ans[TileType.TURBINE][2], InventorySlot.LEMON, 3)
            else:
                move = MyPlayer.bfs(self, poz, [ans[TileType.TURBINE][1], ans[TileType.TURBINE][2]])
                turn = Turn(Command.MOVE, move[0], move[1])
                #self.log(move, "move2")
                if (move[0] == -1):
                    turn = Turn(Command.NOOP)
        # self.log(turn)
        return turn

        """
        def builder(self, lemur,  poz, state):
            turn = Turn(Command.NOOP)
            h1 = MyPlayer.closest(self, poz)
            if state == 0:
                if lemur.stone < 5:
                    clos_stone = h1[TileType.STONE] # esta sa vyhrat kvoli kysliku
                    if (clos_stone[2] > 1):
                        turn = Turn(Command.MOVE, MyPlayer.bfs(self, poz,[clos_stone[1], clos_stone[2]]))
                    else:
                        turn = Turn(Command.BREAK, clos_stone[1], clos_stone[2])
                else:
                    clos_turb = h1[TileType.TURBINE]
                    if (clos_turb[2] == 1):
                        for x, y in D:
                            xn = lemur.x + x
                            yn = lemur.y + y
                            if ([yn][xn].type == TileType.EMPTY):
                                turn = Turn(Command.BUILD, xn, yn, TileType.TURBINE)
                                setup += 1
                                break
                    else:
                        turn = Turn(Command.MOVE, bfs(self, poz, [clos_turb[0], clos_turb[1]]))
            if state == 1:
                clos_iron = h1[TileType.IRON]
            return turn"""

    def make_turn(self) -> list[Turn]:
        self.log("zac")
        turns = []
        id = 0
        for lemur in self.myself.lemurs:
            poz = [lemur.x, lemur.y]
            ans = MyPlayer.closest(self, poz)
            if len(state) != len(self.myself.lemurs):
                tree = [ans[TileType.TREE][1], ans[TileType.TREE][2]]
                state.append(["f", tree])
            if state[id][0] == "f":
                #self.log([lemur.x, lemur.y], ans[TileType.TREE][1], ans[TileType.TREE][2], "pov poz")
                turns.append(MyPlayer.farmer(self, poz, state[id][1], lemur.lemon))
            id += 1
        if (len(turns) != len(self.myself.lemurs)):
            turns = []
            for i in self.myself.lemur:
                turns.append(Turn(Command.NOOP))
        self.log("kon")
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
