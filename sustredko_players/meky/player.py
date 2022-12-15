#!/usr/bin/python
from proboj import *


D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "DD7D11"

    def get_name(self) -> str:
        return "meky"

    def isPossible(self, y, x):
        if (y,x) in self.lemurs_pos:
            return 0
        if 0 <= x < self.world.width and 0 <= y < self.world.height:
            if self.world.tiles[y][x].type.value == 0:
                return 1
        return 0
    
    def budovy(self,lemur,obj):
        bud = []
        for y in range(max(0,lemur.y-self.RANGE),min(self.world.height,lemur.y+self.RANGE)):
            for x in range(max(0,lemur.x-self.RANGE),min(self.world.width,lemur.x+self.RANGE)):
                if self.world.tiles[y][x].type.value == obj:
                    vzd = []
                    for dy,dx in D:
                        if self.isPossible(y+dy,x+dx) and (y+dy,x+dx) in self.svet:
                            vzd.append(self.svet[(y+dy,x+dx)])
                    if len(vzd)>0:
                        vzd = min(vzd)
                        bud.append((vzd ,y,x))
                    
        bud.sort()
        return bud
    
    def hraci(self,arr):
        bud = []
        for y, x in arr:
            vzd = []
            for dy,dx in D:
                if self.isPossible(y+dy,x+dx) and (y+dy,x+dx) in self.svet:
                    vzd.append(self.svet[(y+dy,x+dx)])
            vzd = [e for e in vzd if e!=-1]
            if len(vzd)>0:
                vzd = min(vzd)
                bud.append((vzd ,y,x))

        bud.sort()
        return [(y,x) for v,y,x in bud]
    
    def shortest(self, lemur, obj):
        best_vzd = 99999999
        best_y=-1
        best_x =-1
        my_tree=()
        ##self.log(self.budovy(lemur,obj))
        for vzd,y,x in self.budovy(lemur,obj):
            for dy,dx in D:
                if self.isPossible(y+dy,x+dx) and (y+dy,x+dx) in self.svet:

                        if best_vzd>self.svet[(y+dy,x+dx)]:
                            my_tree = (y,x)
                            best_vzd=self.svet[(y+dy,x+dx)]
                            best_y,best_x=(y+dy,x+dx)

        return best_vzd,best_y,best_x,my_tree

    def path(self,lemur,obj,best_vzd=None,best_y=None,best_x=None,my_tree=None):
        ##self.log("path",lemur,obj,best_vzd,best_y,best_x,my_tree)
        if best_vzd is None:
            best_vzd,best_y,best_x,my_tree = self.shortest(lemur,obj)
        
        if best_y == -1:
            ##self.log("obj error ", obj)
            return (None, 0, 0)
        


        while True:
            if (best_y,best_x) not in self.parrs:
                ##self.log("no path found path")
                return None,-1,-1
                
            if self.parrs[(best_y,best_x)] == (lemur.y, lemur.x):
                return ("move",best_y,best_x)
        
            best_y,best_x = self.parrs[(best_y,best_x)]


    def get_lemons(self,lemur):
        if lemur.lemon > 0:
            for dy,dx in D:
                try:
                    if self.world.tiles[lemur.y+dy][lemur.x+dx].type.value == 4:
                        return ("put",lemur.y+dy,lemur.x+dx)
                
                except Exception as ex:
                    ##self.log("Exception v [get_lemons], error: {ex}")
                    pass

            com, y, x = self.path(lemur, 4)
            if com is not None:
                if (y,x) in self.moji_lemury_pos:
                    return ("put", y, x)
                    
                return ("move", y, x)
        
        for dy,dx in D:
            try:
                if self.world.tiles[lemur.y+dy][lemur.x+dx].type.value == 3 and (lemur.y+dy,lemur.x+dx) :
                    return ("take",lemur.y+dy,lemur.x+dx)
            except Exception as ex:
                ##self.log(f"Exception v [get_lemons]: {ex}")
                pass
                
        return self.path(lemur, 3)

    def expand(self,lemur):
        for dy,dx in D:
            try:
                if self.world.tiles[lemur.y+dy][lemur.x+dx].type.value in self.mineable:
                    return ("break",lemur.y+dy,lemur.x+dx)
            except:pass
        
        
        best_vzd,best_y,best_x = 999999999, -1, -1
        for obj in self.mineable:
            vzd, y, x, _ = self.shortest(lemur,obj)
            if 2 * vzd < best_vzd:
                best_vzd, best_y,best_x = vzd,y,x 
        return self.path(lemur, 1, best_vzd, best_y, best_x)
    
    def mine_mode(self, i, lemur):
        turbiny = self.budovy(lemur,4)
        ok_turbine = 0
        for vzd,y,x in turbiny[:1]:
            if self.world.tiles[y][x].lemon > 3:
                ok_turbine = 1 
                break
        if ok_turbine == 0:
            return 0
            
        # ##self.log("dosazitelne bloky",[len(self.budovy(lemur,e)) for e in self.mineable])
        if all([len(self.budovy(lemur,e)) == 0 for e in self.mineable]):
            return 0
        
        for item in lemur.tools:
            if item is not None:
                if item.value == 1: #pickaxe
                    return 1
            
        return 0 


    def determine_attack(self, lemur_id: int, lemur: Lemur):
        # if invenitory has items that could kill enemy lemur use it else stun
        
        action = None
        y, x = lemur.y, lemur.x
        tools = lemur.tools
        
        for item in tools:
            if item is not None:
                if item.value == 2: # knife
                    action = 'stab'

                elif item.value == 3: # stick
                    action = 'bonk'
        if action is None:
            return None, x, y
        
        for dy,dx in D:
            # vedla je 
            if (y+dy, x+dx) in self.lemurs_pos and (y+dy,x+dx) not in self.moji_lemury_pos:
                return action, y+dy, x+dx

        # Dostatok paliva        
        turbiny = self.budovy(lemur,4)
        ok_turbine = 0
        for vzd,y,x in turbiny[:1]:
            if self.world.tiles[y][x].lemon > 3:
                ok_turbine = 1 
                break
        if ok_turbine == 0:
            return None,0,0

        
        cudzi = self.lemurs_pos.difference(self.moji_lemury_pos)
        hraci = set()
        for y,x in cudzi:
            for dy,dx in D:
                if self.isPossible(y+dy,x+dx):
                    hraci.add((y+dy,x+dx))
                
        hraci = self.hraci(list(hraci))
        if len(hraci) > 0:
            hrac_y,hrac_x = hraci[0]
        else:
            return None,0,0

        return self.path(lemur,50,50,hrac_y,hrac_x)



    def bfs(self, lemur):
        self.svet = {}
        self.parrs = {}
        
        isNotO2 = 1
        if self.world.oxygen[lemur.y][lemur.x]>0:
            isNotO2 = 0

            

        curr = [(lemur.y,lemur.x)]
        vzd=0
        while curr:
            new = []
            for y,x in curr:
                if (y,x) not in self.svet:
                    self.svet[(y,x)] = vzd
                    for dy,dx in D:
                        
                        if (y+dy,x+dx) not in self.svet:
                            try:
                                if self.world.tiles[y+dy][x+dx].type.value == 3:
                                    self.stromy += 1
                            except Exception as ex:
                                ##self.log(f"error bfs tree out of range: {ex}")
                                pass
                            if  self.isPossible(y+dy, x+dx):
                                
                                if isNotO2 or self.world.oxygen[y+dy][x+dx]:
                                    self.parrs[(y+dy, x+dx)] = (y, x)
                                    new.append((y+dy, x+dx))
            curr = new
            vzd += 1
                
        

    def in_inventory(self,lemur,id):
        tools = lemur.tools
        none_count = 0
        
        for item in tools:
            if item is not None:
                if item.value == id: # knife
                    return 1

        return 0
    
    def get_nones(self,lemur):
        tools = lemur.tools
        return sum(item is None for item in tools)
    
    def give(self, lemur):
        if sum([self.get_nones(kamos) == 2 for kamos in self.myself.lemurs]) >= len(self.moji_lemury_pos) // 2:
            return self.give_route(lemur)[0] != None  
        return 0
    
    def give_route(self,lemur):
        best_vzd,best_y,best_x = 99999999,-1,-1
        for kamos in self.myself.lemurs:
            if kamos!=lemur and self.get_nones != 0 and kamos.stone == 0:
                for dy,dx in D:
                    if (kamos.y+dy,kamos.x+dx) == (lemur.y,lemur.x):
                        return "put pick",kamos.y, kamos.x
                    
                    if (kamos.y+dy, kamos.x + dx) in self.svet and self.isPossible(kamos.y+dy, kamos.x + dx):
                        if best_vzd > self.svet[(kamos.y+dy,kamos.x+dx)]:
                            best_vzd = self.svet[(kamos.y+dy,kamos.x+dx)]
                            best_y,best_x = (kamos.y+dy,kamos.x+dx)

        # for dy,dx in D:
        #     try:
        #         if self.svet[(best_y + dy, best_x + dx)] < best_vzd :
        #             return "move",best_y + dy, best_x + dx
            
        #     except Exception as ex:
        #         #self.log(f"Give route error: {ex}")
        #self.log(best_vzd,best_y,best_x)

        return self.path(lemur, 65, 500, best_y, best_x)
            




    def make_turn(self) -> list[Turn]:
        turns = []
        lemons = []
        self.RANGE = 20
        
        # self.occupied_trees = set()
        self.mineable = [2, 1, 5]

        self.lemurs_pos = set() 
        self.moji_lemury_pos = set()
        for player in self.players:
            for lemur in player.lemurs:
                if lemur.alive:
                    self.lemurs_pos.add((lemur.y,lemur.x))
        for lemur in self.myself.lemurs:
            if lemur.alive:
                self.moji_lemury_pos.add((lemur.y,lemur.x))
        
        for i,lemur in enumerate(self.myself.lemurs):
            turn = Turn(Command.NOOP)
            if i>10:
                turns.append(turn)
                continue
            try:
            # for _ in range(1):
                self.stromy = 0
                self.bfs(lemur)
                lemons.append(lemur.lemon)
                
                com, y, x = self.determine_attack(i,lemur)
                
                #self.log(self.mine_mode(i,lemur),"mine mode")
                #self.log("iron",lemur.iron,"stone",lemur.stone,"stromy",self.stromy)
                
                if lemur.stone>=4 and self.stromy >= 1 and self.give(lemur):
                    com,y,x = self.give_route(lemur)
                    #self.log("give lemur ",com)
                    
                elif com is not None and self.stromy >= 1:
                    #self.log("attack - kill 'em all ", com)
                    pass
                elif self.stromy < 1 and lemur.stone >=5:
                    for dy,dx in D:
                        if self.isPossible(lemur.y+dy,lemur.x+dx):
                            com,y,x = "build",lemur.y+dy,lemur.x+dx
                            break
                    
                elif lemur.iron >= 1 and not self.in_inventory(lemur, 2) and self.stromy >= 1 and self.get_nones!=0:
                    com,y,x,item = "craft",-1,-1,"knife"
                elif lemur.stone >= 2 and not self.in_inventory(lemur, 1) and self.stromy >= 1 and self.get_nones!=0:
                    com,y,x,item = "craft",-1,-1,"pickaxe"
                
                elif lemur.stone >= 3 and not self.in_inventory(lemur, 0) and self.stromy >= 1 and i%2 and self.get_nones!=0:
                    com,y,x,item = "craft", -1, -1, "juicer"

                            
                elif self.mine_mode(i,lemur):
                    com,y,x = self.expand(lemur)

                else:
                    com, y, x = self.get_lemons(lemur)
                    #self.log("get lemmons", com, y, x)
                    # except Exception as ex:
                    #     ##self.log(f"Exception v [make_turn]: {ex}")
                    #     com,y,x="er",0,0

                if com == "move":
                    turn = Turn(Command.MOVE, x, y)
                
                elif com == "take":
                    turn = Turn(Command.TAKE, x, y, InventorySlot.LEMON, 10000)
                
                elif com == "put":
                    turn = Turn(Command.PUT, x, y, InventorySlot.LEMON, 10000)
                elif com=="put pick":
                    turn = Turn(Command.PUT, x, y, InventorySlot.STONE, 2) 
                
                elif com == "break":
                    turn = Turn(Command.BREAK, x, y)
                
                elif com == "stab":
                    turn = Turn(Command.STAB, x, y)
                    
                elif com == "bonk":
                    turn = Turn(Command.BONK, x, y)
                
                elif com == "craft":
                    if item == "knife":
                        turn = Turn(Command.CRAFT, Tool.KNIFE)
                        ##self.log("craft ",item)
                    elif item == "pickaxe":
                        turn = Turn(Command.CRAFT, Tool.PICKAXE)
                        ##self.log("craft ",item)
                    elif item == "juicer":
                        turn = Turn(Command.CRAFT, Tool.JUICER)
                        ##self.log("craft ",item)
                        
                elif com == "build":
                    turn = Turn(Command.BUILD,x,y, TileType.TREE)
                else:
                    #self.log(f"error '{com}'")
                    for dy,dx in D:
                        if self.isPossible(lemur.y+dy,lemur.x+dx):
                            turn = Turn(Command.MOVE, lemur.y+dy,lemur.x+dx)
                    #todo
                    pass
                #self.log(f"command '{com}'")

            except Exception as ex:
                
                #self.log("error volaco sa posralo v main",ex)
                pass

            turns.append(turn)

        ##self.log(f"{lemons=}")
        return turns



if __name__ == "__main__":
    p = MyPlayer()
    p.run()
