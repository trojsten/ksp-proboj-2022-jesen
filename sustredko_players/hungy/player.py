#!/usr/bin/python
from proboj import *
from random import shuffle, randrange

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DD = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "ffff00"

    def get_name(self) -> str:
        return "HungB"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def BFS(self, sx: int, sy: int, fx: int, fy: int) -> list[tuple[int]]:
        q = [(sx, sy)]
        vis = [[0 for i in range(self.world.width)] for j in range(self.world.height)]
        bct = {}
        while len(q) != 0:
            cx, cy = q[0]
            q.pop(0)
            if cx == fx and cy == fy:
                px, py = bct[f"{cx}:{cy}"]
                cesta = [(cx, cy)]
                while not (px == sx and py == sy):
                    cesta.append((px, py))
                    px, py = bct[f"{px}:{py}"]
                return cesta
            if vis[cy][cx] == 0:
                if self.world.tiles[cy][cx].type == TileType.EMPTY:
                    if (cx == sx and cy == sy) or ((cx, cy) not in self.prekazky):
                        vis[cy][cx] = 1
                        shuffle(DD)
                        for d in DD:
                            xx = cx+d[0]
                            yy = cy+d[1]
                            if (self.isInRange(xx, yy)):
                                q.append((xx, yy))
                                if (f"{xx}:{yy}" not in bct):
                                    bct[f"{xx}:{yy}"] = (cx, cy)
        
        return [(-1, -1)]
        
    def NajdiNajblizsie(self, x: int, y: int, vec: TileType) -> tuple[int]:
        q = [(x, y)]
        vis = [[0 for i in range(self.world.width)] for j in range(self.world.height)]
        while len(q) != 0:
            cx, cy = q[0]
            q.pop(0)
            if self.world.tiles[cy][cx].type == vec:
                if not (cx == x and cy == y):
                    return (cx, cy)
            if vis[cy][cx] == 0 and self.world.tiles[cy][cx].type == TileType.EMPTY:
                vis[cy][cx] = 1
                for d in D:
                    xx = cx+d[0]
                    yy = cy+d[1]
                    if (self.isInRange(xx, yy)):
                        q.append((xx, yy))
        
        return (-1, -1)

    def SusediS(self, x: int, y: int, vec: TileType) -> tuple[int]:
        for d in D:
            xx = x+d[0]
            yy = y+d[1]
            if (self.isInRange(xx, yy)):
                if (self.world.tiles[yy][xx].type == vec):
                    return (xx, yy)
        return (-1, -1)
    
    def ChodDo(self, lemur: Lemur, vec: TileType) -> Turn:
        d = randrange(4)
        turn = Turn(Command.MOVE, lemur.x+D[d][0], lemur.y+D[d][1])
        najblizsiCitron = self.NajdiNajblizsie(lemur.x, lemur.y, vec)
        if (najblizsiCitron != (-1, -1)):
            cesta = self.BFS(lemur.x, lemur.y, najblizsiCitron[0], najblizsiCitron[1])
            if cesta != [(-1,-1)]:
                turn = Turn(Command.MOVE, cesta[-1][0], cesta[-1][1])
        return turn
    
    def make_turn(self) -> list[Turn]:
        self.prekazky = []
        for lemur in self.myself.lemurs:
            self.prekazky.append((lemur.x, lemur.y))
        '''
        for riadok in self.world.tiles:
            temp = ""
            for policko in riadok:
                temp += str(int(policko.type)) + " "
            self.log(temp)
        '''
        turns = []
        for lemur in self.myself.lemurs:
            d = randrange(4)
            turn = Turn(Command.MOVE, lemur.x+D[d][0], lemur.y+D[d][1])
            
            if (self.SusediS(lemur.x, lemur.y, TileType.TURBINE) != (-1, -1) and lemur.lemon != 0):
                tx, ty = self.SusediS(lemur.x, lemur.y, TileType.TURBINE)
                turn = Turn(Command.PUT, tx, ty, InventorySlot.LEMON, lemur.lemon)
            elif (lemur.lemon != 0):
                turn = self.ChodDo(lemur, TileType.TURBINE)
            elif (self.SusediS(lemur.x, lemur.y, TileType.TREE) != (-1, -1)):
                stromx, stromy = self.SusediS(lemur.x, lemur.y, TileType.TREE)
                if (self.world.tiles[stromy][stromx].has_lemon):
                    turn = Turn(Command.TAKE, stromx, stromy, InventorySlot.LEMON, 1)
            else:
                turn = self.ChodDo(lemur, TileType.TREE)
            turns.append(turn)
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
