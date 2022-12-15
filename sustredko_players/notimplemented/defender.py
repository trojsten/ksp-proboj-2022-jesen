from proboj import *
from util import *

DANGER_CEIL = 5


def self_defence(self, lemur: Lemur):
    if lemur.role==LemurRoles.KAMIKADZE:
        return STRATEGYFAIL
    y, x = lemur.y, lemur.x
    if y == 0 or y == self.world.height - 1 or x == 0 or x == x == self.world.width - 1:
        return STRATEGYFAIL

    if Tool.KNIFE in lemur.tools:
        for player in self.players:
            if player == self.myself:
                continue
            for e_lemur in player.lemurs:
                if abs(e_lemur.x - x) + abs(e_lemur.y - y) == 1:
                    return Turn(Command.STAB, e_lemur.y, e_lemur.x)

    if self.dangerlevels[y][x] < DANGER_CEIL:
        if (
            lemur.role != LemurRoles.BEGGAR
            and Tool.KNIFE not in lemur.tools
            and Tool.STICK not in lemur.tools
        ):
            lemur.prevrole = lemur.role
            lemur.role = LemurRoles.BEGGAR

    return STRATEGYFAIL
