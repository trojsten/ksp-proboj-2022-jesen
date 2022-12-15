from proboj import *
from utils import all_lemurs
from searching import distance, absolute_distance


def is_everyone_reachable(self: ProbojPlayer):
    for lemur in all_lemurs(self.players, self.myself):
        if absolute_distance(self.world, lemur.x, lemur.y, self.myself.lemurs[0]) == float('inf'):
            return False
    return True


def find_nearest_safe_enemy(self: ProbojPlayer, l: Lemur):
    shortest = float('inf')
    target = None
    for lemur in all_lemurs(self.players, self.myself):
        if Tool.KNIFE not in lemur.tools and lemur.alive \
                and distance(self.world, self.players, lemur.x, lemur.y, l) < shortest:
            shortest = distance(self.world, self.players, lemur.x, lemur.y, l)
            target = lemur
    return target


def find_nearest_own_lemur(self: ProbojPlayer, l, target_check=lambda x: True):
    shortest = float('inf')
    target = None
    for lemur in self.myself.lemurs:
        if lemur == l or (not target_check(lemur)):
            continue
        if distance(self.world, self.players, lemur.x, lemur.y, l) < shortest:
            shortest = distance(self.world, self.players, lemur.x, lemur.y, l)
            target = lemur
    return target
