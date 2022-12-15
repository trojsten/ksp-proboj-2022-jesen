#!/usr/bin/python
from proboj import *
import random

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


beakon = []  #zaciatocny
b_radius = 8 #zasah O2
stromy = [] #zaciatocne
'''
bezdak = 0
gardener = 1
miner = 2
bojovnik = 3
'''
castovy_sys = [] 
priradenie_stromov = []
kamidegarden = [] # True je k stromu False k beaknu
dodavac_prenasleduje = False
manoz = False
maxvzdialenostironu = 15


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "042069"

    def get_name(self) -> str:
        return "Example.py"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height



    #....tak od tailto su vlastne.................


    def hladanie_naj_strom(self, x, y):
        global stromy
        najblizsi = stromy[0]
        for strom in stromy:
            if abs(najblizsi[0] - x) + abs(najblizsi[1] - y) > abs(strom[0] - x) + abs(strom[1] - y):
                najblizsi = strom
        return najblizsi

    #..zisti, kde je beakon
    def start_najdi_beakon(self, bx, by):

        while self.world.oxygen[by][bx] != 15:
            for dx, dy in D:
                if self.isInRange(bx + dx, by + dy) and \
                        self.world.oxygen[by + dy][bx + dx] > self.world.oxygen[by][bx]:
                        
                    bx += dx
                    by += dy
                    self.log(beakon)
                    self.log(self.world.oxygen[by][bx])
        
        return [bx, by]


        
    def start_najdi_lepsi(self, bx, by):
        i = 0
        bull = True
        krock = 0

        run = True

        while run:
            self.log(bx," bx                 ",by," by")

            if bull:
                krock += 1
                bull = False
            
            else:
                bull = True


            for a in range(krock):

                bx += D[i][0]
                by += D[i][1]

                if self.isInRange(bx,by) and self.world.tiles[by][bx].type == TileType.TURBINE:

                    self.start_najdi_stromy(bx, by)
                    if len(stromy) != 0:
                        run = False
                        return[bx, by] 
            
            if i == 3:
                i = 0
            else:
                i += 1

        return [bx, by]

    def start_najdi_stromy(self, sx, sy):
        global stromy

        for a in range(b_radius * 2 + 1):
            for b in range(b_radius * 2 + 1):
                if self.isInRange(sx + b - b_radius, sy + a - b_radius):
                    if self.world.tiles[sy + a - b_radius][sx + b - b_radius].type == TileType.TREE:
                        stromy.append([sx + b - b_radius, sy + a - b_radius])

                        self.log(self.world.tiles[sy + a - b_radius][sx + b - b_radius].type)
            
    def start_casting(self):
        global castovy_sys, priradenie_stromov, kamidegarden
        c_gardener = 0
        c_pickaxe = -1
        for i in range(len(self.myself.lemurs)):
            castovy_sys.append(0)
        
        for i in range(len(self.myself.lemurs)-1,-1,-1):
            if c_gardener < 2:
                castovy_sys[i] = 1
                priradenie_stromov.append([])
                kamidegarden.append(True)
                c_gardener += 1
            else:
                if i == 0:
                    castovy_sys[i] = 3
                else:
                    castovy_sys[i] = 2
        
        g = 0
        for i in range(len(castovy_sys)):
            if castovy_sys[i] == 1:
                priradenie_stromov[g] = self.hladanie_naj_strom(self.myself.lemurs[i].x, self.myself.lemurs[i].y)
                g += 1
        
        self.log("casting:", castovy_sys, "    jajjaj:", priradenie_stromov)
        

    def pohyb_zahrad(self,i,kolklemur):
        global kamidegarden, priradenie_stromov
#        self.log(kamidegarden,"kamide")
#        self.log("kolkatylemur: ",kolklemur, "             kolkgarden: ", i)
        lem = self.myself.lemurs[kolklemur]
        pri = priradenie_stromov
        if kamidegarden[i]:
            for dx,dy in D:
#                self.log("1")
                if self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.TREE:
#                    self.log("2")
                    if self.world.tiles[lem.y+dy][lem.x+dx].has_lemon:
#                        self.log("3")
                        kamidegarden[i] = False
#                        self.log("bereme cintrooon")
                        return Turn(Command.TAKE, lem.x + dx, lem.y + dy, 0, 1)
#                    self.log("4")
#                    self.log("cakame na cintrooon")
                    return Turn(Command.NOOP)

#            self.log("5")
            for dx,dy in D:
                if abs(lem.x + dx - pri[i][0]) + abs(lem.y + dy - pri[i][1]) < abs(lem.y - pri[i][1]) + abs(lem.x - pri[i][0]):
#                    self.log("6")
                    if self.world.tiles[lem.y + dy][lem.x + dx].type == TileType.EMPTY:
#                        self.log("7")
#                        self.log("ideme k cintrooon")
                        return Turn(Command.MOVE, lem.x + dx, lem.y + dy)

            return Turn(Command.NOOP)

        else:
            for dx,dy in D:
                if self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.TURBINE:
                    kamidegarden[i] = True
                    self.log("odovzdavame cintrooon")
                    return Turn(Command.PUT, lem.x + dx, lem.y + dy, 0, 1)
            
            for dx,dy in D:
                    if abs(lem.x + dx - beakon[0]) + abs(lem.y + dy - beakon[1]) < abs(lem.y - beakon[1]) + abs(lem.x - beakon[0]):
                        self.log("ideme ododvzdat cintrooon")
                        return Turn(Command.MOVE, lem.x + dx, lem.y + dy)



    def pohyb_killerminer(self,kolklemur):
        global castovy_sys, manoz
        lem = self.myself.lemurs[kolklemur]
        
        self.log("zacali sme")
        if manoz:
            self.log("ma noz")
            nieco = self.prehladavanie(lem.x,lem.y,0, False)
            self.log(nieco," nieco")
            if nieco != -1:
                dx,dy = nieco
                self.log(dx,dy,"dx a dy")

                for plyer in self.players:
                    if plyer != self.myself:
                        for lemur in plyer.lemurs:
                            if lemur.x == lem.x+dx and lemur.y == lem.y + dy:
                                return Turn(Command.STAB,lemur.x,lemur.y)
                            else:
                                return Turn(Command.MOVE,lem.x+dx,lem.y+dy)
        
            self.log("nic nerobi lebo sa nevie nikam dostat")
            return Turn(Command.NOOP)
        

            
        else:
            self.log(lem.iron," pocet ironu")
            if lem.iron > 0:
                manoz = True
                return Turn(Command.CRAFT,Tool.KNIFE)
        
            self.log("nema noz")
            nieco = self.prehladavanie(lem.x,lem.y,TileType.IRON, True)
            self.log(nieco, "co nam naslo prehlad")
            if nieco == -1:
                nieco = self.prehladavanie(lem.x,lem.y,TileType.STONE, True)
                self.log(nieco, "co nam naslo prehlad")
                if nieco != -1:
                    dx,dy = nieco
                    if self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.STONE:
                        self.log("znicil")
                        return Turn(Command.BREAK,lem.x+dx,lem.y+dy)
                    else:
                        self.log("pohol sa")
                        return Turn(Command.MOVE,lem.x+dx,lem.y+dy)
                
            else:
                dx,dy = nieco
                if self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.IRON or self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.STONE:
                    self.log("znicil")
                    return Turn(Command.BREAK,lem.x+dx,lem.y+dy)
                else:
                    self.log("pohol sa")
                    return Turn(Command.MOVE,lem.x+dx,lem.y+dy)
            
            self.log("nic nerobi lebo sa nevie nikam dostat a nema ani noz")
            return Turn(Command.NOOP)



            '''
            vsetcimaju = True
            for i in range(len(self.myself.lemurs[:2])):
                if not 2 in self.myself.lemurs[i].tools:
                   vsetcimaju = False
                   nema = i

            if vsetcimaju:
                castovy_sys[kolklemur] = 2
            
            else:
                lemx = self.myself.lemurs[i].x
                lemy = self.myself.lemurs[i].y
                if dodavac_prenasleduje:
                    for dx,dy in D:
                        if lem.x + dx == lemx and lem.y + dy == lemy:
                            dodavac_prenasleduje = False
                            return Turn(Command.PUT, lemx, lemy, InventorySlot.PICKAXE, 1)


                    for dx,dy in D:
                        if abs(lem.x + dx - lemx) + abs(lem.y + dy - lemy) < abs(lem.y - lemy) + abs(lem.x - lemx):
                            return Turn(Command.MOVE, lem.x + dx, lem.y + dy)
                
                else:
                    if lem.read_lemur.stone >= 2:
                        dodavac_prenasleduje = True
                        return Turn(Command.CRAFT,Tool.PICKAXE)
                    
                    else:
                        for dx,dy in D:
                            if self.world.tiles[lem.y+dy][lem.x+dx].type == TileType.STONE:
                                return Turn(Command.BREAK, lem.x+dx, lem.y+dy)
        else:
            for dx,dy in D:
                if abs(lem.x + dx - beakon[0]) + abs(lem.y + dy - beakon[1]) < abs(lem.y - beakon[1]) + abs(lem.x - beakon[0]):
                    return Turn(Command.MOVE, lem.x + dx, lem.y + dy)
            '''

    def spetneprehladavanie(self,pole,zaciatok,koniec):
        self.log(pole," pole ",zaciatok," zaciatok ",koniec," koniec ")

        while True:
            for dx,dy in D:
                if (zaciatok[0] + dx,zaciatok[1] + dy) in pole:
                    if pole[(zaciatok[0] + dx,zaciatok[1] + dy)] < pole[(zaciatok[0],zaciatok[1])]:
                        if (zaciatok[0] + dx, zaciatok[1] + dy) == koniec: 
                            self.log(dx*-1, dy*-1, "vystup z spatneho")
                            return (dx*-1, dy*-1)
                        
                        else:
                            zaciatok[0] += dx
                            zaciatok[1] += dy



    def prehladavanie(self,x,y,blok,bol):
        global maxvzdialenostironu
        self.log(x," x ",y," y ",blok," blok ",bol," bol ")

        if bol:
            poleprehladanych = {}
            q = [(x,y,0)]

            while self.world.tiles[q[0][1]][q[0][0]].type != blok:
                for dx,dy in D:
                    if not (q[0][0] + dx,q[0][1] + dy) in poleprehladanych:
                        if self.isInRange(q[0][0], q[0][1]):
                            if self.world.oxygen[q[0][1]][q[0][0]] > 0 and self.world.tiles[q[0][1]][q[0][0]].type == TileType.EMPTY:
                                if q[0][2]+1 <= maxvzdialenostironu:
                                    if self.isInRange(q[0][0]+dx, q[0][1]+dy):
                                        q.append((q[0][0] + dx,q[0][1] + dy,q[0][2]+1))
                    

                nieo = q.pop(0)
                poleprehladanych[(nieo[0],nieo[1])] = nieo[2]

                if len(q) == 0:
                    self.log(-1,"vystup")
                    return -1
            
            poleprehladanych[(q[0][0],q[0][1])] = q[0][2]
            return self.spetneprehladavanie(poleprehladanych,[q[0][0],q[0][1]],(x,y))
        
        else:
            poleprehladanych = {}
            q = [(x,y,0)]
            run = True
            while run:

                for plyer in self.players:
                    if plyer != self.myself:
                        for lemur in plyer.lemurs:
                            if q[0][0] == lemur.x and q[0][1] == lemur.y:
                                poleprehladanych[q[0][0],q[0][1]] = q[0][2]+1
                                return self.spetneprehladavanie(poleprehladanych,[q[0][0],q[0][1]],(x,y))

                for dx,dy in D:
                    if not (q[0][0] + dx,q[0][1] + dy) in poleprehladanych:
                        if self.world.oxygen[q[0][1]+dx][q[0][0]+dy] > 0 and self.world.tiles[q[0][1]+dx][q[0][0]+dy].type == TileType.EMPTY:
                            q.append((q[0][0] + dx,q[0][1] + dy,q[0][2]+1))

                nieo = q.pop(0)
                poleprehladanych[(nieo[0],nieo[1])] = nieo[2]

                if len(q) == 0:
                    self.log(-1,"vystup")
                    return -1
            
            
    def make_turn(self) -> list[Turn]:

        self.log("pocet leurov:", len(self.myself.lemurs))

        #....scan teritory........
        global beakon, stromy
        if len(beakon) == 0:
            beakon = self.start_najdi_beakon(self.myself.lemurs[0].x, self.myself.lemurs[0].y)
            self.log(beakon, "beconeeeeee")

            self.start_najdi_stromy(beakon[0], beakon[1])
            self.log("stromceky:", stromy)

            if len(stromy) == 0:
                beakon = self.start_najdi_lepsi(self.myself.lemurs[0].x, self.myself.lemurs[0].y)

            self.start_casting()

        
        turns = []
        i = 0
        kolkgarden = 0
        for lemur in self.myself.lemurs:
            '''
            turn = Turn(Command.NOOP)
            for dx, dy in D:
                if self.isInRange(lemur.x + dx, lemur.y + dy) and \
                        self.world.oxygen[lemur.y + dy][lemur.x + dx] > self.world.oxygen[lemur.y][lemur.x]:
                    
                    
                    turn = Turn(Command.MOVE, lemur.x - dx, lemur.y - dy)
            '''
            turn = Turn(Command.NOOP)

            # ak je gardener
            if castovy_sys[i] == 1:
                turn = self.pohyb_zahrad(kolkgarden,i)
                kolkgarden += 1
            
            if castovy_sys[i] == 3:
                turn = self.pohyb_killerminer(i)
            
            nepriatelblizko = False
            for plyer in self.players:
                if plyer != self.myself:
                    for lemur in plyer.lemurs:
                        if beakon[0] - b_radius < lemur.x < beakon[0] + b_radius and beakon[1] - b_radius < lemur.y < beakon[1] + b_radius:
                            nepriatelblizko = True
            
            if len(castovy_sys) < 3 and nepriatelblizko:
                for i in range(len(castovy_sys)):
                    castovy_sys[0] = 3

                    
            turns.append(turn)
            i += 1

        self.log(turns)
        return turns
    





if __name__ == "__main__":
    p = MyPlayer()


    p.run()

