from enum import Enum

from proboj import ProbojPlayer, Tool, TileType
from utils import everyone_has_item


class LemurType(Enum):
    SURVIVALIST = 0
    CRAFTER = 1
    MINER = 2
    KILLER = 3
    NONE = 4


class LemurManager:
    def __init__(self):
        self.survivalists = []
        self.crafters = []
        self.miners = []
        self.killers = []
        self.initialized = False
        self.open_map = False

    def rebalance(self, player: ProbojPlayer):
        # If everyone alive has knife and pickaxe, become miner
        if everyone_has_item(player.myself.lemurs, Tool.PICKAXE) and everyone_has_item(player.myself.lemurs, Tool.KNIFE):
            self.survivalists.extend(self.crafters)
            self.crafters = []

    def get_lemur_type(self, lemur):
        if lemur in self.survivalists:
            return LemurType.SURVIVALIST
        elif lemur in self.crafters:
            return LemurType.CRAFTER
        elif lemur in self.miners:
            return LemurType.MINER
        elif lemur in self.killers:
            return LemurType.KILLER
        else:
            return LemurType.NONE

    def short_type(self, lemur):
        return self.get_lemur_type(lemur).name[0].upper()


class TurnWatcher:
    def __init__(self):
        self.turns_by_lemur = {}

    def add_turn(self, lemur_id, turn):
        return
        if lemur_id not in self.turns_by_lemur:
            self.turns_by_lemur[lemur_id] = []

        self.turns_by_lemur[lemur_id].append(turn)
        if len(self.turns_by_lemur[lemur_id]) > 3:
            self.turns_by_lemur[lemur_id].pop(0)

    def is_stuck(self, lemur_id):
        return False
        turns = self.turns_by_lemur.get(lemur_id, [])
        if len(turns) < 3:
            return False
        return turns[-1] == turns[-2] == turns[-3]
