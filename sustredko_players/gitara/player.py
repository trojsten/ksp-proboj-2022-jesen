#!/usr/bin/python
from proboj import *
from itertools import count
from collections import deque
from random import *

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def distance_sq(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]))

def shuffled(iter):
    result = [*iter]
    shuffle(iter)
    return result

def count_pickaxes(lemur):
    result = 0
    for tool in lemur.tools:
        if tool == Tool.PICKAXE: result += 1
    return result

class MyPlayer(ProbojPlayer):
    def __init__(self):
        super().__init__()
        self.game_started = False
        self.lemur_count = None
        self.lemur_map = None

    def get_color(self) -> str:
        return "ff3665"

    def get_name(self) -> str:
        return "Gitarujeme"

    def count_lemurs(self):
        self.lemur_count = 0
        for player in self.players:
            for lemur in player.lemurs:
                self.lemur_count += 1

    def do_we_need_pickaxe(self):
        for lemur in self.myself.lemurs:
            if not lemur.have_tool(Tool.PICKAXE): return True
        return False

    def is_inside(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def is_turbine_at(self, x, y):
        return self.is_inside(x, y) and self.world.tiles[y][x].type == TileType.TURBINE

    def is_stone_at(self, x, y):
        return self.is_inside(x, y) and self.world.tiles[y][x].type == TileType.STONE

    def is_iron_at(self, x, y):
        return self.is_inside(x, y) and self.world.tiles[y][x].type == TileType.IRON

    def is_lemon_tree_at(self, x, y):
        if not self.is_inside(x, y): return
        tile = self.world.tiles[y][x]
        return tile.type == TileType.TREE and tile.has_lemon

    def map_lemur_without_pickaxe(self):
        self.lemur_without_pickaxe_map = set()
        for lemur in self.myself.lemurs:
            if not lemur.alive: continue
            if not lemur.have_tool(Tool.PICKAXE):
                self.lemur_without_pickaxe_map.add((lemur.x, lemur.y))

    def is_lemur_without_pickaxe_at(self, x, y):
        return (x, y) in self.lemur_without_pickaxe_map

    def is_enemy_at(self,x, y):
        return (x, y) in self.enemy_map

    def is_real_enemy_at(self, x, y):
        return (x, y) in self.real_enemy_map

    def supports_tree(self, x, y):
        if not self.is_walkable(x, y):return False
        count = 0
        for x1 in range(x - 1, x + 2):
            for y1 in range(y - 1, y + 2):
                if self.is_walkable(x1, y1):
                    count += 1
        return count >= 7

    def map_lemurs(self):
        self.lemur_map = set()
        self.enemy_map = set()
        self.real_enemy_map = set()
        for player in self.players:
            for lemur in player.lemurs:
                if not lemur.alive: continue
                if player != self.myself:
                    self.real_enemy_map.add((lemur.x, lemur.y))
                    square_size = 5
                    for x in range(lemur.x - square_size, lemur.x + square_size + 1):
                        for y in range(lemur.y - square_size, lemur.y + square_size + 1):
                            if lemur.have_tool(Tool.STICK):
                                if distance((x, y), (lemur.x, lemur.y)) <= 5:
                                    self.lemur_map.add((x, y))
                                    self.enemy_map.add((x, y))
                            if lemur.have_tool(Tool.KNIFE):
                                if distance((x, y), (lemur.x, lemur.y)) <= 2:
                                    self.lemur_map.add((x, y))
                                    self.enemy_map.add((x, y))
                self.lemur_map.add((lemur.x, lemur.y))

    '''def is_lemur_at(self, x, y):
        for player in self.players:
            #self.log(f'lemurs of player {player}')
            for i, lemur in enumerate(player.lemurs):
                if not lemur.alive: continue
                #self.log(f'lemur {lemur}')
                if player != self.myself:
                    if lemur.have_tool(Tool.STICK):
                        if distance((x, y), (lemur.x, lemur.y)) <= 5: return True
                    if lemur.have_tool(Tool.KNIFE):
                        self.log((x, y), (lemur.x, lemur.y), distance((x, y), (lemur.x, lemur.y)))
                        if distance((x, y), (lemur.x, lemur.y)) <= 3: return True
                if lemur.x == x and lemur.y == y: return True
        return False'''

    def is_walkable(self, x, y):
        if not 0 <= x < self.world.width or not 0 <= y < self.world.height:
            return False
        return all((
            self.world.tiles[y][x].type == TileType.EMPTY,
            not (x, y) in self.lemur_map,
            self.world.oxygen[y][x] > 0
        ))

    def count_local(self, x1, y1, what):
        queue = deque([(x1, y1)])
        seen = set()
        result = 0
        #self.log(f'searching local {x1, y2} to {x2, y2}')
        while queue:
            x, y = queue.popleft()
            if (x, y) in seen: continue
            if what(x, y):
                result += 1
            #self.log(f'seen {x, y}')
            seen.add((x, y))
            for dx, dy in shuffled(D):
                nx, ny = x + dx, y + dy
                if not (self.is_walkable(nx, ny) or what(nx, ny)): continue
                queue.append((nx, ny))
        return result

    def find_path(self, x1, y1, what):
        queue = deque([(x1, y1)])
        seen = set()
        backtrack = {}
        #self.log(f'searching {x1, y2} to {x2, y2}')
        while queue:
            x, y = queue.popleft()
            if what(x, y):
                #self.log(f'found path from {x1, y1} to {x2, y2}')
                rx, ry = x, y
                while True:
                    #self.log(f'search from {x1, y1}, backtrack {rx, ry}')
                    if backtrack[rx, ry] == (x1, y1):
                        return (x, y), (rx, ry)
                    rx, ry = backtrack[rx, ry]
            if (x, y) in seen: continue
            #self.log(f'seen {x, y}')
            seen.add((x, y))
            for dx, dy in shuffled(D):
                nx, ny = x + dx, y + dy
                if not (self.is_walkable(nx, ny) or what(nx, ny)): continue
                queue.append((nx, ny))
                if not (nx, ny) in backtrack: backtrack[nx, ny] = x, y
        return None, None

    def make_turn(self) -> list[Turn]:
        if not self.game_started:
            self.count_lemurs()
            for lemur in self.myself.lemurs:
                self.log(lemur.tools)
            self.gave_pickaxe = [False] * len(self.myself.lemurs)
        self.game_started = True
        self.map_lemurs()
        self.map_lemur_without_pickaxe()
        turns = []
        for i, lemur in enumerate(self.myself.lemurs):
            #self.log('alive'if lemur.alive else 'dead', lemur.lemon)
            turbine, _ = self.find_path(lemur.x,lemur.y, self.is_turbine_at)
            #self.log(self.world.tiles[turbine[1]][turbine[0]].lemon if turbine else 'neni turbina')
            turn = Turn(Command.NOOP)
            x, y = lemur.x, lemur.y
            if (x, y) in self.enemy_map:
                for dx, dy in shuffled(D):
                    tx, ty = x + dx, y + dy
                    if self.is_walkable(tx, ty):
                        turn = Turn(Command.MOVE, tx, ty)
                        break
            if turn.command == Command.NOOP and lemur.have_tool(Tool.PICKAXE):
                enemy, path = self.find_path(x, y, self.is_real_enemy_at)
                self.log('enemy at', enemy)
                if enemy:
                    if lemur.have_tool(Tool.KNIFE):
                        if distance(enemy, (x, y)) == 1:
                            turn = Turn(Command.STAB, *enemy)
                        else: turn = Turn(Command.MOVE, *path)
                    else:
                        if lemur.iron >= 1:
                            turn = Turn(Command.CRAFT, Tool.KNIFE)
                        else:
                            iron, path = self.find_path(x, y, self.is_iron_at)
                            if iron:
                                if distance(iron, (x, y)) == 1:
                                    turn = Turn(Command.BREAK, *iron)
                                else: turn = Turn(Command.MOVE, *path)
            if turn.command == Command.NOOP and lemur.lemon:
                turbine, path = self.find_path(x, y, self.is_turbine_at)
                if turbine:
                    if distance(turbine, (x, y)) == 1:
                        turn = Turn(Command.PUT, *turbine, InventorySlot.LEMON, lemur.lemon)
                    else: turn = Turn(Command.MOVE, *path)
            if turn.command == Command.NOOP:
                tree, path = self.find_path(x, y, self.is_lemon_tree_at)
                if tree:
                    if distance(tree, (x, y)) == 1:
                        turn = Turn(Command.TAKE, *tree, InventorySlot.LEMON, 1)
                    else: turn = Turn(Command.MOVE, *path)
            if turn.command == Command.NOOP and lemur.have_tool(Tool.PICKAXE):
                if not self.gave_pickaxe[i] and self.do_we_need_pickaxe():
                    self.log('giving pickaxe')
                    if count_pickaxes(lemur) >= 2:
                        self.log(x, y, count_pickaxes(lemur), self.lemur_without_pickaxe_map)
                        lemur2, path = self.find_path(x, y, self.is_lemur_without_pickaxe_at)
                        if lemur2:
                            if distance((x, y), lemur2) == 1:
                                turn = Turn(Command.PUT, *lemur2, InventorySlot.TOOL2, 1)
                                self.gave_pickaxe[i] = True
                            else: turn = Turn(Command.MOVE, *path)
                    else:
                        if lemur.stone >= 2:
                            turn = Turn(Command.CRAFT, Tool.PICKAXE)
                        else:
                            stone, path = self.find_path(x, y, self.is_stone_at)
                            if stone:
                                if distance((x, y), stone) == 1:
                                    turn = Turn(Command.BREAK, *stone)
                                else:
                                    turn = Turn(Command.MOVE, *path)
                else:
                    self.log('mining')
                    if lemur.stone >= 5:
                        tree, path = self.find_path(x, y, self.supports_tree)
                        self.log(tree)
                        if tree:
                            if distance(tree, (x, y)) == 1:
                                turn = Turn(Command.BUILD, *tree, TileType.TREE)
                            else:
                                turn = Turn(Command.MOVE, *path)
                    else:
                        stone, path = self.find_path(x, y, self.is_stone_at)
                        if stone:
                            if distance((x, y), stone) == 1:
                                turn = Turn(Command.BREAK, *stone)
                            else:
                                turn = Turn(Command.MOVE, *path)

            if turn.command == Command.NOOP:
                for dx, dy in shuffled(D):
                    tx, ty = x + dx, y + dy
                    if self.is_walkable(tx, ty):
                        turn = Turn(Command.MOVE, tx, ty)
                        break
            self.log(turn.command)
            turns.append(turn)
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
