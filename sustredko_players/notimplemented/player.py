#!/usr/bin/python
#


from proboj import *
from miner import *
from oberac import *
from lemur_with_nothing import *
from give_to_beggar import *
from beggar import *
from defender import *
from kamikadze import *
from trader import *


D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyPlayer(ProbojPlayer):
    def init(self):
        self.roles = {}
        self.observer = StructObserver(self.world)

        for i in self.myself.lemurs:
            i.role = LemurRoles.BROKE
            i.prevrole = None
        if len(self.myself.lemurs) == 1:
            self.myself.lemurs[0].role = LemurRoles.GARDENER
        else:
            self.myself.lemurs[0].role = LemurRoles.MINER
            self.myself.lemurs[1].role = LemurRoles.GARDENER

    def get_color(self) -> str:
        return "00ff00"

    def get_name(self) -> str:
        return "MV"

    def isInRange(self, x, y):
        return 0 <= x < self.world.width and 0 <= y < self.world.height

    def recover_roles(self):
        for i in self.roles:
            self.myself.lemurs[i].role = self.roles[i][0]
            self.myself.lemurs[i].prevrole = self.roles[i][1]

    def save_roles(self):
        self.roles = {}
        for i in range(len(self.myself.lemurs)):
            x = self.myself.lemurs[i]
            if hasattr(x, "role"):
                self.roles[i] = (x.role, x.prevrole)

    def move_lemur(self, id):
        lemur = self.myself.lemurs[id]

        lemur.id = id

        # quick triggers

        move = self_defence(self, lemur)
        if move != STRATEGYFAIL:
            return move

        move = give_to_poor(self, lemur)
        if move != STRATEGYFAIL:
            return move

        # normal moves
        if lemur.role == LemurRoles.BEGGAR:
            move = beggar(self, lemur)
        elif LemurRoles.MINER == lemur.role:
            move = miner(self, lemur)
        elif LemurRoles.BROKE == lemur.role:
            move = lemur_with_nothing(self, lemur)
        elif LemurRoles.GARDENER == lemur.role:
            move = harvest(self, lemur, self.observer)

        self.log(move)
        if move != STRATEGYFAIL and (
            move.command != Command.MOVE
            or (move.args[1], move.args[0]) not in self.used_fields
        ):
            if move.command == Command.MOVE:
                self.used_fields.add((move.args[1], move.args[0]))
            return move

        self.log("fuck", id)
        move = Turn(Command.NOOP)
        for dx, dy in D:
            if (
                self.isInRange(lemur.x + dx, lemur.y + dy)
                and self.world.oxygen[lemur.y + dy][lemur.x + dx]
                > self.world.oxygen[lemur.y][lemur.x]
            ):
                move = Turn(Command.MOVE, lemur.x + dx, lemur.y + dy)
        if move != STRATEGYFAIL and (
            move.command != Command.MOVE
            or (move.args[1], move.args[0]) not in self.used_fields
        ):
            if move.command == Command.MOVE:
                self.used_fields.add((move.args[1], move.args[0]))
            return move

        return Turn(Command.NOOP)

    def make_turn(self) -> list[Turn]:
        if not hasattr(self, "roles"):
            self.init()

        self.dangerlevels = dangerlevels(self)

        self.used_fields = set()

        self.observer.update_timers(self.world)

        self.recover_roles()

        self.log(self.roles)

        lemurs = [i for i in range(len(self.myself.lemurs))]

        lemurs.sort(key=lambda x: self.myself.lemurs[x].role)

        turns = [None] * len(lemurs)
        for i in lemurs:
            turns[i] = self.move_lemur(i)

        self.save_roles()

        self.log(self.roles)

        self.log(turns)
        return turns


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
