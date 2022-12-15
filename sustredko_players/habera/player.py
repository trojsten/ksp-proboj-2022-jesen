#!/usr/bin/python
from proboj import *
from queue import Queue
import random 

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyPlayer(ProbojPlayer):

    fazaTazica = 0
    fazaPichaca = 0
    fazaKrmica = 0

    def get_color(self) -> str:
        return "4d0076"

    def get_name(self) -> str:
        return "Sexx"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def bfs_dycha(self, x1, y1, x2, y2):
        if(self.world.tiles[y2][x2].type != TileType.EMPTY):
            return (x1, x2)
        q = Queue(maxsize = 0)
        navstivene = [[False]*self.world.height for i in range(self.world.width)]
        skadial = [[[0]*2 for i in range(self.world.height)] for j in range(self.world.width)]
        #for i in range(self.world.width):
            #for j in range(self.world.height):
                #self.log(i, j, self.world.width, self.world.height)
        q.put((x1,y1,0))
        while (not q.empty()):
            x,y,vzd = q.get()
            if (navstivene[x][y]): continue
            navstivene[x][y] = True
            for dx, dy in D:
                if(self.isInRange(x+dx, y+dy)):
                    if(navstivene[x+dx][y+dy]==False and self.world.tiles[y+dy][x+dx].type == TileType.EMPTY and self.world.oxygen[y+dy][x+dx]!=0):
                        skadial[x+dx][y+dy] = [-dx, -dy]
                        q.put((x+dx, y+dy, vzd+1))
        x = x2
        y = y2
        return_x = x
        return_y = y
        self.log("pred while", x,y,return_x, return_y)
        while (x!=x1 or y!=y1):
            return_x = x
            return_y = y
            self.log(skadial[x][y])
            x += skadial[return_x][return_y][0]
            y += skadial[return_x][return_y][1]
            self.log(x,y,return_x, return_y, x1, y1)
        
        return (return_x, return_y)

    def bfs(self, x1, y1, x2, y2):
        if(self.world.tiles[y2][x2].type != TileType.EMPTY):
            return (x1, x2)
        q = Queue(maxsize = 0)
        navstivene = [[False]*self.world.height for i in range(self.world.width)]
        skadial = [[[0]*2 for i in range(self.world.height)] for j in range(self.world.width)]
        #for i in range(self.world.width):
            #for j in range(self.world.height):
                #self.log(i, j, self.world.width, self.world.height)
        q.put((x1,y1,0))
        navstivene[x1][y1] = True
        while (not q.empty()):
            x,y,vzd = q.get()
            for dx, dy in D:
                if(self.isInRange(x+dx, y+dy)):
                    if(navstivene[x+dx][y+dy]==False and self.world.tiles[y+dy][x+dx].type == TileType.EMPTY):
                        skadial[x+dx][y+dy] = [-dx, -dy]
                        navstivene[x+dx][y+dy] = True
                        q.put((x+dx, y+dy, vzd+1))
        x = x2
        y = y2
        return_x = x
        return_y = y
        self.log("pred while", x,y,return_x, return_y)
        while (x!=x1 or y!=y1):
            return_x = x
            return_y = y
            self.log(skadial[x][y])
            x += skadial[return_x][return_y][0]
            y += skadial[return_x][return_y][1]
            self.log(x,y,return_x, return_y, x1, y1)
        
        return (return_x, return_y)

    def najdi_nablizsi_dycha(self, x, y, CO):
        q = Queue(maxsize = 0)
        navstivene = [[False]*self.world.height for i in range(self.world.width)]
        #for i in range(self.world.width):
            #for j in range(self.world.height):
                #self.log(i, j, self.world.width, self.world.height)
        q.put((x,y,0))
        navstivene[x][y] = True
        while (not q.empty()):
            x,y,vzd = q.get()
            for dx, dy in D:
                if(self.isInRange(x+dx, y+dy)):
                    if (self.world.tiles[y+dy][x+dx].type == CO):
                        return (x,y)
                    if(navstivene[x+dx][y+dy]==False and self.world.tiles[y+dy][x+dx].type == TileType.EMPTY and self.world.oxygen[y+dy][x+dx]!=0):
                        q.put((x+dx, y+dy, vzd+1))
                        navstivene[x+dx][y+dy] = True
        return (x, y)

    def akodalekooosiiiiii(self, x, y, CO):
        q = Queue(maxsize = 0)
        navstivene = [[False]*self.world.height for i in range(self.world.width)]
        #for i in range(self.world.width):
            #for j in range(self.world.height):
                #self.log(i, j, self.world.width, self.world.height)
        q.put((x,y,0))
        while (not q.empty()):
            x,y,vzd = q.get()
            if (navstivene[x][y]): continue
            navstivene[x][y] = True
            for dx, dy in D:
                if(self.isInRange(x+dx, y+dy)):
                    if (self.world.tiles[y+dy][x+dx].type == CO):
                        return (vzd)
                    if(navstivene[x+dx][y+dy]==False and self.world.tiles[y+dy][x+dx].type == TileType.EMPTY and self.world.oxygen[y+dy][x+dx]!=0):
                        q.put((x+dx, y+dy, vzd+1))
        return (10000000)

    def najdi_nablizsi(self, x, y, CO):
        q = Queue(maxsize = 0)
        navstivene = [[False]*self.world.height for i in range(self.world.width)]
        #for i in range(self.world.width):
            #for j in range(self.world.height):
                #self.log(i, j, self.world.width, self.world.height)
        q.put((x,y,0))
        while (not q.empty()):
            x,y,vzd = q.get()
            if (navstivene[x][y]): continue
            navstivene[x][y] = True
            for dx, dy in D:
                if(self.isInRange(x+dx, y+dy)):
                    if (self.world.tiles[y+dy][x+dx].type == CO):
                        return (x,y)
                    if(navstivene[x+dx][y+dy]==False and self.world.tiles[y+dy][x+dx].type == TileType.EMPTY):
                        q.put((x+dx, y+dy, vzd+1))
        return (x, y)

    def taz(self, x, y, CO, ALEBOTOINE):
        if(self.akodalekooosiiiiii(x, y, CO) <= self.akodalekooosiiiiii(x, y, ALEBOTOINE)):
            masx, masy = self.najdi_nablizsi_dycha(x, y, CO)
        else: 
            masx, masy = self.najdi_nablizsi_dycha(x, y, ALEBOTOINE)
        self.log(masx,masy)
        for dx, dy in D:
            if(self.world.tiles[y+dy][x+dx].type == CO or self.world.tiles[y+dy][x+dx].type == ALEBOTOINE):
                self.log("TAZIM")
                return Turn(Command.BREAK, x+dx, y+dy)
        if(self.world.oxygen[masy][masx] != 0):
            kamx, kamy = self.bfs_dycha(x, y, masx, masy)
            return Turn(Command.MOVE, kamx, kamy)
        else:
            return Turn(Command.NOOP)

    def je_tu_zly(self, x, y):
        rx = -1
        ry = -1
        for i in range(max(0,x-2), min(x+3, self.world.width)):
            for j in range(max(0,y-2), min(y+3, self.world.height)):
                if (self.world.tiles[j][i].type == TileType.ENEMYLEMUR):
                    for plr in self.players:
                        for he in plr.lemurs:
                            if(he.stunned <=1 and he.x == i and he.y == j):
                                rx = i
                                ry = j
                                continue
        return (rx,ry)

    def make_turn(self) -> list[Turn]:
        turns = []
        for hrac in self.players:
            for fuj in hrac.lemurs:
                if (fuj.alive == True):
                    self.world.tiles[fuj.y][fuj.x].type = TileType.ENEMYLEMUR
        for lemur in self.myself.lemurs:
                if (lemur.alive == True):
                    self.world.tiles[lemur.y][lemur.x].type = TileType.NASLEMUR
        jeden = 0
        dva = 1
        tri = 2
        if len(self.myself.lemurs) == 1:
            jeden = 1
            dva = 0
            tri = 1

        for lemur in self.myself.lemurs:

            #lemur nula co cykli lemony kokotko
            if (lemur.x==self.myself.lemurs[dva].x and lemur.y == self.myself.lemurs[dva].y and self.fazaKrmica == 0):
                COCEEEEEEM = ""
                if(lemur.lemon<1):
                    surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TREE)
                    COCEEEEEEM = "citron"
                else:
                    surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TURBINE)
                    COCEEEEEEM = "turbo"
                if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="citron"):
                    for dx, dy in D:
                        if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TREE):
                            turn = Turn(Command.TAKE, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                            turns.append(turn)
                    continue
                if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="turbo"):
                    for dx, dy in D:
                        if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TURBINE):
                            turn = Turn(Command.PUT, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                            turns.append(turn)
                    continue
                #self.log("idem hentu", surovinax, surovinay, self.world.tiles[surovinay][surovinax].type)
                kamx, kamy = self.bfs(lemur.x, lemur.y, surovinax, surovinay)
                #self.log(lemur.x, lemur.y, kamx, kamy)
                turn = Turn(Command.MOVE, kamx, kamy)
                turns.append(turn)
                #self.log(turn)
                continue
            
            #lemur co je pichac
            elif (lemur.x == self.myself.lemurs[tri].x and lemur.y == self.myself.lemurs[tri].y): 
                if (self.fazaPichaca == 0):
                    self.log("SOM absolutna nula nie jak ty misko :)")
                    COCEEEEEEM = ""
                    if(lemur.lemon<1):
                        self.log("nemam citron som sporsdty idem po citron")
                        surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TREE)
                        COCEEEEEEM = "citron"
                    else:
                        self.log("wow cotijb mam citron idm turbinova tubro brm brm")
                        surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TURBINE)
                        COCEEEEEEM = "turbo"
                    if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="citron"):
                        self.log("wowo strom som vedla tu mam citron mnam nma")
                        for dx, dy in D:
                            if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TREE):
                                turn = Turn(Command.TAKE, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                                turns.append(turn)
                                self.log(turn)
                        continue
                    if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="turbo"):
                        self.log("COOOOOOOO >TURBINA CO CHCES TU MAS PAPAJ CITRON")
                        for dx, dy in D:
                            if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TURBINE):
                                turn = Turn(Command.PUT, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                                turns.append(turn)
                                self.log(turn)
                        continue
                    self.log("idem hentu", surovinax, surovinay, self.world.tiles[surovinay][surovinax].type)
                    kamx, kamy = self.bfs(lemur.x, lemur.y, surovinax, surovinay)
                    self.log(lemur.x, lemur.y, kamx, kamy)
                    turn = Turn(Command.MOVE, kamx, kamy)
                    turns.append(turn)
                    self.log(turn)
                    continue
                elif(self.fazaPichaca==1):
                    turn = Turn(Command.NOOP)
                    turns.append(turn)
                    if lemur.tools:
                        self.fazaPichaca = 2
                    continue
                elif (self.fazaPichaca == 2):
                    x,y = self.je_tu_zly(max(0,lemur.x-2), min(lemur.x+3, self.world.width))
                    if(x!=-1 and y!=-1):
                        turn = Turn(Command.BONK,x ,y)
                    else:
                        turn = Turn(Command.NOOP)
                    turns.append(turn)
                    continue

            #lemur tazi a stava idk ma krompac tak ho abusujeme hajzl
            elif(lemur.x==self.myself.lemurs[jeden].x and lemur.y == self.myself.lemurs[jeden].y):
                if(self.fazaTazica == 0):
                    self.log("idem. tazim.")
                    turn = self.taz(lemur.x, lemur.y, TileType.IRON, TileType.STONE)
                    turns.append(turn)
                    self.log("0", turn)
                    if(lemur.stone >= 5):
                        self.fazaTazica = 1
                    continue

                if(self.fazaTazica == 1):
                    kdejex, kdejey = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TURBINE)
                    kamzex, kamzey = self.bfs(lemur.x, lemur.y, kdejex, kdejey)
                    if(lemur.x == kdejex and lemur.y == kdejey):
                        for dx, dy in D:
                            if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TURBINE):
                                turn = Turn(Command.BUILD, lemur.x-dy, lemur.y+dx, TileType.TREE)
                                turns.append(turn)
                                self.fazaTazica = 2
                                self.fazaPichaca = 1
                                self.log(turn)
                    else:
                        turn = Turn(Command.MOVE, kamzex, kamzey)
                        turns.append(turn)
                    continue

                if(self.fazaTazica == 2):
                    self.log("idem. tazim.")
                    turn = self.taz(lemur.x, lemur.y, TileType.IRON, TileType.STONE)
                    turns.append(turn)
                    self.log("0", turn)
                    if(lemur.iron >= 6):
                        self.fazaTazica = 3
                        self.log("idme do trojky ;)", self.fazaTazica)
                    continue

                if(self.fazaTazica == 3):
                    self.log("SOM UZ V TROJKEEEEEEEEE")
                    turn = Turn(Command.CRAFT, Tool.STICK)
                    turns.append(turn)
                    self.fazaTazica = 4
                    continue

                if(self.fazaTazica == 4):
                    for dx, dy in D:
                        self.log(self.world.tiles[self.myself.lemurs[tri].y + dy][self.myself.lemurs[tri].x + dx].type, self.myself.lemurs[tri].x + dx, self.myself.lemurs[tri].y + dy)
                        if(self.world.tiles[self.myself.lemurs[tri].y + dy][self.myself.lemurs[tri].x + dx].type == TileType.EMPTY or (self.myself.lemurs[tri].y + dy == lemur.y and self.myself.lemurs[tri].x + dx == lemur.x)):
                            kamx = self.myself.lemurs[tri].x + dx
                            kamy = self.myself.lemurs[tri].y + dy
                            break
                    dakamx, dakamy = self.bfs(lemur.x, lemur.y, kamx, kamy)
                    self.log("som 4 ako moja znamka v nemcine", lemur.x, lemur.y, kamx, kamy, dakamx, dakamy)
                    if(lemur.x == kamx and lemur.y == kamy):
                        for dx, dy in D:
                            self.log("idem dat", self.world.tiles[lemur.y+dy][lemur.x+dx].type)
                            if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.NASLEMUR):
                                self.log("uz fakt davam", lemur.x, lemur.y, lemur.x+dx, lemur.y+dy, InventorySlot.TOOL2)
                                turn = Turn(Command.PUT, lemur.x+dx, lemur.y+dy, InventorySlot.TOOL2, 1)
                                turns.append(turn)
                                self.fazaTazica = 5
                                self.log(lemur.tools, self.myself.lemurs[2].tools)
                    else:   
                        turn = Turn(Command.MOVE, dakamx, dakamy)
                        turns.append(turn)
                    continue

                if(self.fazaTazica == 5):
                    if (lemur.stone >= 23):
                        turn = Turn(Command.CRAFT, Tool.JUICER)
                        turns.append(turn)
                        self.fazaTazica = 6
                    else:
                        self.log("idem. tazim.")
                        turn = self.taz(lemur.x, lemur.y, TileType.IRON, TileType.STONE)
                        turns.append(turn)
                        self.log("0", turn)
                    continue
                
                somVolny = True

                if(self.fazaTazica == 6):
                    for dx, dy in D:
                        if(self.world.tiles[lemur.y + dy][lemur.x + dx].type != TileType.EMPTY and self.world.tiles[lemur.y + dy][lemur.x + dx].type != TileType.TREE):
                            if(self.world.tiles[lemur.y + dy][lemur.x + dx].type == TileType.NASLEMUR or self.world.tiles[lemur.y + dy][lemur.x + dx].type == TileType.ENEMYLEMUR):
                                kamleeex, kalmeeey = D[random.randrange(0, 4)]
                                turn = Turn(Command.MOVE, lemur.x + kamleeex, lemur.y + kalmeeey)
                                turns.append(turn)
                            else:
                                somVolny = False
                                turn = Turn(Command.BREAK, lemur.x + dx, lemur.y + dy)
                                turns.append(turn)
                            break
                    if(somVolny):
                        for dx, dy in D[:3]:
                            if(self.world.tiles[lemur.y + dy][lemur.x + dx].type == TileType.EMPTY):
                                turn = Turn(Command.BUILD, lemur.x + dx, lemur.y + dy, TileType.TREE)
                                turns.append(turn)
                                break
                    dalej = True
                    for dx, dy in D[:3]:
                        if(self.world.tiles[lemur.y + dy][lemur.x + dx].type != TileType.TREE and self.world.tiles[lemur.x + dx][lemur.y + dy].type != TileType.TREE):
                            dalej = False
                    if(dalej):
                        self.fazaTazica = 7
                        turn = Turn(Command.NOOP)
                        turns.append(turn)
                    continue
                
                if(self.fazaTazica == 7):
                    self.log("mam citrony", lemur.lemon)
                    if (lemur.lemon >= 30):
                        self.log("JEBEM TI MATER IDEM DO OSEEEEEEEEEEEM")
                        self.fazaTazica = 8
                        turn = Turn(Command.NOOP)
                        turns.append(turn)
                    else:
                        nemamnic = True
                        for dx, dy in D:
                            nx, ny = lemur.x + dx, lemur.y + dy
                            self.log("papam", self.world.tiles[ny][nx].type)
                            if (self.world.tiles[ny][nx].type == TileType.TREE and self.world.tiles[ny][nx].has_lemon):
                                self.log("BEREEEEEEEEEEEEM", ny, nx, self.world.tiles[ny][nx].type, self.world.tiles[ny][nx].has_lemon)
                                self.log(turns)
                                turn = Turn(Command.TAKE, nx, ny, InventorySlot.LEMON, 1)
                                self.log(lemur.lemon)
                                turns.append(turn)
                                self.log(turns)
                                nemamnic = False
                                break
                        if(nemamnic):
                            turn = Turn(Command.NOOP)
                            turns.append(turn)
                    continue

                if (self.fazaTazica== 8):
                    zburane = False
                    for dx, dy in D:
                        if (self.world.tiles[lemur.y + dy][lemur.x+dx].type == TileType. TREE):
                            turn = Turn(Command.BREAK,lemur.x+dx,lemur.y+dy)
                            turns.append(turn)
                            zburane = True
                            break
                    if(zburane == False):
                        self.fazaTazica = 9
                        turn = Turn(Command.DISCARD, InventorySlot.TOOL1, 1)
                        turns.append(turn)
                    continue

                if(self.fazaTazica == 9):
                    turn = Turn(Command.CRAFT, Tool.KNIFE)
                    turns.append(turn)
                    self.fazaTazica = 10
                    continue

                if(self.fazaTazica == 10):
                    x,y = self.najdi_nablizsi(lemur.x,lemur.y, TileType.ENEMYLEMUR)
                    uzsom = True
                    for dx,dy in D:
                        if (self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.ENEMYLEMUR):
                            turn = Turn(Command.STAB, lemur.x+dx, lemur.y+dy)
                            turns.append(turn)
                            uzsom = False
                            break
                    if (lemur.x == x and lemur.y == y and uzsom):
                        turn = Turn(Command.NOOP)
                        turns.append(turn)
                    elif(uzsom):
                        rx,ry = self.bfs(lemur.x,lemur.y,x,y)
                        turn = Turn(Command.MOVE, rx ,ry)
                        turns.append(turn)
                    continue

            #zvysni lemuri
            else:
                COCEEEEEEM = ""
                if(lemur.lemon<1):
                    surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TREE)
                    COCEEEEEEM = "citron"
                else:
                    surovinax, surovinay = self.najdi_nablizsi(lemur.x, lemur.y, TileType.TURBINE)
                    COCEEEEEEM = "turbo"
                if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="citron"):
                    for dx, dy in D:
                        if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TREE):
                            turn = Turn(Command.TAKE, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                            turns.append(turn)
                    continue
                if(lemur.x == surovinax and lemur.y == surovinay and COCEEEEEEM=="turbo"):
                    for dx, dy in D:
                        if(self.world.tiles[lemur.y+dy][lemur.x+dx].type == TileType.TURBINE):
                            turn = Turn(Command.PUT, lemur.x+dx, lemur.y+dy, InventorySlot.LEMON, 1)
                            turns.append(turn)
                    continue
                #self.log("idem hentu", surovinax, surovinay, self.world.tiles[surovinay][surovinax].type)
                kamx, kamy = self.bfs(lemur.x, lemur.y, surovinax, surovinay)
                #self.log(lemur.x, lemur.y, kamx, kamy)
                turn = Turn(Command.MOVE, kamx, kamy)
                turns.append(turn)
                #self.log(turn)
                continue
            
        self.log(turns)
        self.log(self.myself.lemurs)
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
