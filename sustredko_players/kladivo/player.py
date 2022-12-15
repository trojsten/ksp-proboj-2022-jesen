#!/usr/bin/python
from proboj import *
import time

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "ffffff"

    def get_name(self) -> str:
        return "KLADIVO🔨+😨=🤯"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def pohni_sa(self,x,y):
        if self.isInRange(x, y):
            self.turn = Turn(Command.MOVE,x,y)

    def viem_ist_na_policko(self,pos):#typ_viem_ist
        if self.isInRange(pos[0], pos[1]):
            if self.world.tiles[pos[1]][pos[0]].type == TileType.EMPTY and self.world.oxygen[pos[1]][pos[0]] > 0:# or self.world.tiles[pos[1]][pos[0]].type == typ_viem_ist:
                if self.mriezka_lemurov[pos[1]][pos[0]] == -1:
                    return True
        return False


    def BFS(self,zac, typy):
        A = [zac]
        B = []
        vzd = []
        prvy_krok = []
        for riadok in range(self.world.height):
            vzd.append([-1]*self.world.width)
            prvy_krok.append([-1]*self.world.width)
        vzd[zac[1]][zac[0]] = 0
        vysledok = {}
        obsadil = False
        self.pocet_stromov = 0
        stromy = set()
        while True:
            if len(A) == 0:
                return vysledok#(-1,-1)
            B = []
            for i in A:
                for dx,dy in D:
                    policko = (i[0]+dx,i[1]+dy)
                    if not self.isInRange(policko[0], policko[1]):
                        continue
                    if vzd[policko[1]][policko[0]] == -1:
                        for typ in typy:
                            if self.viem_ist_na_policko(policko):#(self.world.tiles[policko[1]][policko[0]].type == TileType.EMPTY or self.world.tiles[policko[1]][policko[0]].type == typ)
                                B.append(policko)
                                vzd[policko[1]][policko[0]] = vzd[i[1]][i[0]]+1
                                if i == zac:
                                    prvy_krok[policko[1]][policko[0]] = (dx,dy)
                                else:
                                    prvy_krok[policko[1]][policko[0]] = prvy_krok[i[1]][i[0]]
                                
                            if self.world.tiles[policko[1]][policko[0]].type == typ:#policko == kon:
                                if typ == TileType.TREE:
                                    if policko not in stromy:
                                        self.pocet_stromov += 1
                                        stromy.add(policko)
                                    if policko in self.obsadene:
                                        continue
                                    elif not obsadil:
                                        self.obsadene.append(policko)
                                        obsadil = True
                                
                                if typ not in vysledok:
                                    if i == zac:
                                        vysledok[typ] = (dx,dy)
                                    else:
                                        vysledok[typ] = prvy_krok[i[1]][i[0]]#prvy_krok[policko[1]][policko[0]]
                                    #return prvy_krok[kon[1]][kon[0]]
                                if len(vysledok) == len(typy):
                                    return vysledok
            A = [c for c in B]

    def BFS_jednoduche(self,zac,kon):
        A = [zac]
        B = []
        vzd = []
        prvy_krok = []
        zly = []
        for riadok in range(self.world.height):
            vzd.append([-1]*self.world.width)
            prvy_krok.append([-1]*self.world.width)
            zly.append([-1]*self.world.width)
        for player in self.players:
            for lemur_zly in player.lemurs:
                if lemur_zly: #not in self.myself.lemurs:
                    zly[lemur_zly.y][lemur_zly.x] = 1
        vzd[zac[1]][zac[0]] = 0
        while True:
            if len(A) == 0:
                return -1#(-1,-1)
            B = []
            for i in A:
                # self.log("noveA")
                for dx,dy in D:
                    policko = (i[0]+dx,i[1]+dy)
                    if not self.isInRange(policko[0], policko[1]):
                        continue
                    if vzd[policko[1]][policko[0]] == -1:
                        if self.viem_ist_na_policko(policko) and zly[policko[1]][policko[0]] == -1:#(self.world.tiles[policko[1]][policko[0]].type == TileType.EMPTY or self.world.tiles[policko[1]][policko[0]].type == typ)
                            B.append(policko)
                            vzd[policko[1]][policko[0]] = vzd[i[1]][i[0]]+1
                            if i == zac:
                                prvy_krok[policko[1]][policko[0]] = (dx,dy)
                                # self.log("prvykrok[",policko[1],"][",policko[0],"=",(dx,dy))
                            else:
                                prvy_krok[policko[1]][policko[0]] = prvy_krok[i[1]][i[0]]
                                # self.log("prvykrok[",policko[1],"][",policko[0],"=",prvy_krok[i[1]][i[0]],"i",i)
                    
                        if policko == kon:
                            #self.log(prvy_krok)
                            return prvy_krok[i[1]][i[0]]
            A = [c for c in B]

    def BFS_najdi_lemura(self,zac):
        A = [zac]
        B = []
        vzd = []
        prvy_krok = []
        zly = []
        for riadok in range(self.world.height):
            vzd.append([-1]*self.world.width)
            zly.append([-1]*self.world.width)
            prvy_krok.append([-1]*self.world.width)
        for player in self.players:
            for lemur_zly in player.lemurs:
                if lemur_zly: #not in self.myself.lemurs:
                    zly[lemur_zly.y][lemur_zly.x] = 1
        vzd[zac[1]][zac[0]] = 0
        while True:
            if len(A) == 0:
                return -1#(-1,-1)
            B = []
            for i in A:
                # self.log("noveA")
                for dx,dy in D:
                    policko = (i[0]+dx,i[1]+dy)
                    if not self.isInRange(policko[0], policko[1]):
                        continue
                    if vzd[policko[1]][policko[0]] == -1:
                        if self.viem_ist_na_policko(policko) and zly[policko[1]][policko[0]] == -1:#(self.world.tiles[policko[1]][policko[0]].type == TileType.EMPTY or self.world.tiles[policko[1]][policko[0]].type == typ)
                            B.append(policko)
                            vzd[policko[1]][policko[0]] = vzd[i[1]][i[0]]+1
                            if i == zac:
                                prvy_krok[policko[1]][policko[0]] = (dx,dy)
                                # self.log("prvykrok[",policko[1],"][",policko[0],"=",(dx,dy))
                            else:
                                prvy_krok[policko[1]][policko[0]] = prvy_krok[i[1]][i[0]]
                                # self.log("prvykrok[",policko[1],"][",policko[0],"=",prvy_krok[i[1]][i[0]],"i",i)
                    
                        if zly[policko[1]][policko[0]] == 1:#policko == kon:
                            #self.log(prvy_krok)
                            return prvy_krok[i[1]][i[0]]
            A = [c for c in B]

    def chod_k_policku_BFS(self,lemur,x,y,typ):
        dx,dy = self.BFS((lemur.x,lemur.y),(x,y),typ)
        if (dx,dy) == (-1,-1):
            self.turn = Turn(Command.NOOP)
            return
        self.pohni_sa(lemur.x+dx, lemur.y+dy)


    def susedi_s_tile(self,lemur,typ):
        for dx,dy in D:
            if self.isInRange(lemur.x+dx, lemur.y+dy):    
                if self.world.tiles[lemur.y+dy][lemur.x+dx].type == typ:
                    return (lemur.x+dx,lemur.y+dy)
        return False
    
    def susedi_s_lemurom0(self,lemur):
        for dx,dy in D:
            if lemur.x+dx == self.myself.lemurs[0].x and lemur.y+dy == self.myself.lemurs[0].y:
                return (lemur.x+dx,lemur.y+dy)
        return False

    def susedi_s_nepriatelom(self,lemur):
        for player in self.players:
            for lemur_zly in player.lemurs:
                if lemur_zly not in self.myself.lemurs:
                    for dx,dy in D:
                        if lemur.x+dx == lemur_zly.x and lemur.y+dy == lemur_zly.y:
                            return (lemur.x+dx,lemur.y+dy)
        return False
        
    def susedi_s_svojim(self,lemur):
        for player in self.players:
            for lemur_dobry in player.lemurs:
                if lemur_dobry in self.myself.lemurs and lemur_dobry != lemur:
                    for dx,dy in D:
                        if lemur.x+dx == lemur_dobry.x and lemur.y+dy == lemur_dobry.y:
                            return lemur_dobry
        return False
    
    def najblizsi_tile(self,lemur,typ):
        minvzd = 10000
        pos = -1
        for x in range(self.world.width):
            for y in range(self.world.height):
                if self.world.tiles[y][x].type == typ:
                    if typ == TileType.TREE and (x,y) in self.obsadene:
                        continue
                    vzd_teraz = abs(y-lemur.y) + abs(x- lemur.x)
                    if vzd_teraz < minvzd:
                        minvzd = vzd_teraz
                        pos = (x,y)
        self.obsadene.append(pos)
        return pos
    
    def TLE(self):
        while True:
            pass

    def update_lemury_pozicie(self):
        self.mriezka_lemurov = []
        for riadok in range(self.world.height):
            self.mriezka_lemurov.append([-1]*self.world.width)
        for player in self.players:
            for lemur in player.lemurs:
                if lemur in self.myself.lemurs:
                    self.mriezka_lemurov[lemur.y][lemur.x] = 1
                else:
                    self.mriezka_lemurov[lemur.y][lemur.x] = 0

    # def pocet_stromov(self):
    #     pocet = 0
    #     for x in range(self.world.width):
    #         for y in range(self.world.height):
    #             if self.world.tiles[y][x].type == TileType.TREE:
    #                 pocet += 1
    #     return pocet

    def make_turn(self) -> list[Turn]:
        cas_zac = time.time()
        try:
            self.init += 0
        except:
            #iba na zaciatku:
            self.init = 0
            # elf.log("zaciatok")
            self.cislo_tahu = 0
            self.pocet_citronovacov = 2
            self.pocet_stromov = 0
            self.pocet_zmetenych_citronovacov = 1

        self.cislo_tahu += 1
        # if self.cislo_tahu > 100:
        #     self.TLE()
        self.turns = []
        self.obsadene = []
        self.update_lemury_pozicie()
        stop = False
        i = -1
        for lemur in self.myself.lemurs:
            #self.log(time.time()-cas_zac)
            if time.time()-cas_zac > 0.3:
                stop = True
            if stop:
                self.turns.append(Turn(Command.NOOP))
                continue
            i += 1
            try:
                self.turn = Turn(Command.NOOP)
                if Tool.KNIFE in lemur.tools:
                    sused = self.susedi_s_nepriatelom(lemur)
                    if sused != False:
                        self.turns.append(Turn(Command.STAB,sused[0],sused[1]))
                        continue

                #if i < self.pocet_citronovacov:
                kam_pohnut = self.BFS((lemur.x,lemur.y), [TileType.TREE,TileType.TURBINE,TileType.STONE,TileType.IRON])
                # elf.log("kampohnut",kam_pohnut)

                if Tool.PICKAXE in lemur.tools:
                    self.turn = Turn(Command.NOOP)
                    if self.pocet_zmetenych_citronovacov > 0:#len(self.myself.lemurs)-1:
                        if TileType.STONE in kam_pohnut:
                            self.turn = Turn(Command.MOVE,lemur.x+kam_pohnut[TileType.STONE][0],lemur.y+kam_pohnut[TileType.STONE][1])
                        kamen = self.susedi_s_tile(lemur, TileType.STONE)
                        if kamen != False:
                            self.turn = Turn(Command.BREAK,kamen[0],kamen[1])
                        if lemur.stone >= 5:
                            volne_miesto = self.susedi_s_tile(lemur, TileType.EMPTY)
                            if volne_miesto != False:
                                self.turn = Turn(Command.BUILD,volne_miesto[0],volne_miesto[1],TileType.TREE)
                    else:
                        #daco pridavam
                        self.log(lemur.tools)
                        if lemur.iron > 1 and Tool.KNIFE not in lemur.tools:
                            self.turn = Turn(Command.CRAFT, Tool.KNIFE)
                            self.log('mam noyik', lemur.iron, lemur.tools)
                        elif TileType.IRON in kam_pohnut:
                            self.turn = Turn(Command.MOVE,lemur.x+kam_pohnut[TileType.IRON][0],lemur.y+kam_pohnut[TileType.IRON][1])
                        else:
                            if TileType.STONE in kam_pohnut:
                                self.turn = Turn(Command.MOVE,lemur.x+kam_pohnut[TileType.STONE][0],lemur.y+kam_pohnut[TileType.STONE][1])
                            kamen = self.susedi_s_tile(lemur, TileType.STONE)
                            if kamen != False:
                                self.turn = Turn(Command.BREAK,kamen[0],kamen[1])
                        iron = self.susedi_s_tile(lemur, TileType.IRON)
                        if iron != False:
                            self.turn = Turn(Command.BREAK,iron[0],iron[1])
                    sused = self.susedi_s_svojim(lemur)
                    if sused != False and sused.iron == 0 and Tool.KNIFE not in sused.tools:
                        self.turn = Turn(Command.PUT,sused.x,sused.y,InventorySlot.IRON,1)
                    self.turns.append(self.turn)
                    # if len(self.myself.lemurs) > 1: #aj tu
                    continue
                
                if i == 1:
                    self.pocet_zmetenych_citronovacov = 0

                if i < self.pocet_citronovacov+1:# or len(self.myself.lemurs) == 1: #tu podmienka bz Joyura
                    if lemur.lemon == 0:
                        if TileType.TREE not in kam_pohnut:
                            self.pocet_zmetenych_citronovacov += 1
                            self.turns.append(Turn(Command.NOOP))
                            continue
                        else:
                            self.turn = Turn(Command.MOVE,lemur.x+kam_pohnut[TileType.TREE][0],lemur.y+kam_pohnut[TileType.TREE][1])

                    strom = self.susedi_s_tile(lemur,TileType.TREE)
                    if strom != False and lemur.lemon == 0:
                        self.turn = Turn(Command.TAKE,strom[0],strom[1],InventorySlot.LEMON,1)
                    
                    if lemur.lemon == 1:
                        if TileType.TURBINE not in kam_pohnut:
                            self.turns.append(Turn(Command.NOOP))
                            continue
                        self.turn = Turn(Command.MOVE,lemur.x+kam_pohnut[TileType.TURBINE][0],lemur.y+kam_pohnut[TileType.TURBINE][1])

                    turbina = self.susedi_s_tile(lemur, TileType.TURBINE)
                    if turbina != False and lemur.lemon == 1:
                        self.turn = Turn(Command.PUT,turbina[0],turbina[1],InventorySlot.LEMON,1)
                    
                    self.turns.append(self.turn)
                    continue
                
                krok = self.BFS_jednoduche((lemur.x,lemur.y),(self.myself.lemurs[0].x,self.myself.lemurs[0].y))
                #self.log("lemuris",(lemur.x,lemur.y),(self.myself.lemurs[0].x,self.myself.lemurs[0].y))
                #self.log("krok",krok)
                if krok != -1:#(-1,-1):
                    self.turn = Turn(Command.MOVE,lemur.x+krok[0],lemur.y+krok[1])
                # lemur0 = self.susedi_s_lemurom0(lemur)
                # if lemur0 != False and lemur.iron == 0:
                #     self.log("berie",lemur.iron)
                #     self.turn == Turn(Command.TAKE,lemur0[0],lemur0[1],InventorySlot.IRON,1)
                if lemur.iron >= 1 and Tool.KNIFE not in lemur.tools:
                    self.turn = Turn(Command.CRAFT,Tool.KNIFE)
                    self.turns.append(self.turn)
                    continue
                if Tool.KNIFE in lemur.tools:
                    krok = self.BFS_najdi_lemura((lemur.x,lemur.y))
                    if krok != -1:
                        self.turn = Turn(Command.MOVE,lemur.x+krok[0],lemur.y+krok[1])
            except:
                pass
            self.turns.append(self.turn)
        return self.turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()

"""

# for dx, dy in D:
            #     if self.isInRange(lemur.x + dx, lemur.y + dy) and \
            #             self.world.oxygen[lemur.y + dy][lemur.x + dx] > self.world.oxygen[lemur.y][lemur.x]:
            #         turn = Turn(Command.MOVE, lemur.x + dx, lemur.y + dy)
    

def chod_k_policku(self,lemur,x,y):#returnuje true ak uz dorazil
        if lemur.x != x:
            strana = int(-(lemur.x-x)/abs(lemur.x-x))
            self.pohni_sa(lemur.x+strana, lemur.y)
            return False
        if lemur.y != y:
            strana = int(-(lemur.y-y)/abs(lemur.y-y))
            self.pohni_sa(lemur.x, lemur.y+strana)
            return False
        return True

"""