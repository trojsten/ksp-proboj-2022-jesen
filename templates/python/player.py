#!/usr/bin/python
from proboj import *

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "042069"

    def get_name(self) -> str:
        return "Example.py"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def make_turn(self) -> list[Turn]:
        turns = []
        for lemur in self.myself.lemurs:
            turn = Turn(Command.NOOP)
            for dx, dy in D:
                if self.isInRange(lemur.x + dx, lemur.y + dy) and \
                        self.world.oxygen[lemur.y + dy][lemur.x + dx] > self.world.oxygen[lemur.y][lemur.x]:
                    turn = Turn(Command.MOVE, lemur.x + dx, lemur.y + dy)
            turns.append(turn)
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
