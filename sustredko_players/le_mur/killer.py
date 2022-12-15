from proboj import *
from utils import D, inside, knife_safe, no_knife, all_lemurs
from searching import step_to, distance


class KillerMixin:
    def go_to_lemur(self: ProbojPlayer, target: Lemur, l: Lemur):
        if not target:
            return None

        if step := step_to(self.world, self.players, target.x, target.y, l):
            if knife_safe(self.world, step[0], step[1], self.players, self.myself):
                return Turn(Command.MOVE, step[0], step[1])

    def kill(self: ProbojPlayer, l: Lemur):
        if Tool.KNIFE not in l.tools:
            return
        for victim in all_lemurs(self.players, self.myself):
            if victim.alive and abs(victim.x - l.x) + abs(victim.y - l.y) <= 1:
                return Turn(Command.STAB, victim.x, victim.y)
