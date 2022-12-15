#!/usr/bin/python
from collections.abc import Iterable

from proboj import *
from random import randint, choice
from timeit import default_timer as timer
from string import ascii_uppercase
from state_manager import LemurManager, LemurType, TurnWatcher
from survivalist import SurvivalistMixin
from killer import KillerMixin
from miner import MinerMixin
from crafter import CrafterMixin, RESOURCES
from safety import SafetyMixin
from searching import search, step_to, distance
from lemur_finder import find_nearest_own_lemur, find_nearest_safe_enemy, is_everyone_reachable
from utils import enum_to_str, everyone_has_item, nearest_turbine_lemons

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class LeMurPlayer(ProbojPlayer, SurvivalistMixin, KillerMixin, MinerMixin, CrafterMixin, SafetyMixin):
    def __init__(self):
        super().__init__()
        self.lemur_manager = LemurManager()
        self.turn_watcher = TurnWatcher()

    def get_color(self) -> str:
        return 'cc2c04' #hex(randint(0, 256**3))[2:].zfill(6)

    def get_name(self) -> str:
        #😘🐵🐒
        monkey = choice(("🙈", "🙊", "🙉"))
        return f"🧐Lè_ֻMûr{monkey}"# + " " + choice(ascii_uppercase)

    def make_turn(self) -> list[Turn]:
        self.init_manager()
        self.lemur_manager.rebalance(self)
        turns = []
        for i, lemur in enumerate(self.myself.lemurs):
            start = timer()
            turn = self.generic_turn(lemur) or Turn(Command.NOOP)
            end = timer()
            self.log(f"({self.lemur_manager.short_type(lemur)}{i}{'L' if lemur.alive else 'D'} @ {lemur.x},{lemur.y}) "
                     f"[{turn.command.name}: "
                     f"{tuple(enum_to_str(arg) for arg in turn.args)}]"
                     f" {{{' '.join(tool.name if tool else '-' for tool in lemur.tools)}"
                     f" | S{lemur.stone} I{lemur.iron} L{lemur.lemon}}}"
                     f" {end - start:.3f}s")
            self.turn_watcher.add_turn(i, (turn, turn.args))
            turns.append(turn)
        return turns

    def generic_turn(self, l):
        if not l.alive:
            return Turn(Command.NOOP)

        if (k := self.kill(l)) is not None:
            return k

        searched = search(l, self.world)

        if nearest_turbine_lemons(self, l, searched) <= 1:
            return self.survivalist_turn(l, searched)

        if self.turn_watcher.is_stuck(self.myself.lemurs.index(l)):
            self.log(f"[WARN]: Lemur {l.x, l.y} is stuck")
            dx, dy = choice(D)
            return Turn(Command.MOVE, l.x + dx, l.y + dy)

        # Go to the nearest oxygen
        if self.world.oxygen[l.y][l.x] == 0:
            air_tiles = searched[TileType.EMPTY]
            if air_tiles and (step := step_to(self.world, self.players, air_tiles[0][0], air_tiles[0][1], l)):
                return Turn(Command.MOVE, step[0], step[1])

        typ = self.lemur_manager.get_lemur_type(l)
        if typ == LemurType.SURVIVALIST:
            return self.survivalist_turn(l, searched)
        elif typ == LemurType.MINER:
            return self.miner_turn(l, searched)
        elif typ == LemurType.KILLER:
            return self.killer_turn(l, searched)
        elif typ == LemurType.CRAFTER:
            return self.crafter_turn(l, searched)
        else:
            return self.survivalist_turn(l, searched)

    def survivalist_turn(self, l: Lemur, searched: dict) -> Turn | None:
        if Tool.PICKAXE in l.tools:
            timeleft = min(nearest_turbine_lemons(self, l, searched) * 8, 3)
            if Tool.KNIFE not in l.tools:
                return scenario(
                    self.craft, (Tool.KNIFE, l),
                    self.mine_block, (l),
                    self.go_to_nearest_resource, (l, searched, TileType.IRON, min(100,timeleft//2-6)),
                    self.survivalist_base, (l, searched)
                )
            else:
                return scenario(
                    self.mine_block, (l),
                    self.go_to_nearest_resource, (l, searched, TileType.IRON, min(100,timeleft//2-15)),
                    self.go_to_nearest_resource, (l, searched, TileType.STONE, min(100,timeleft//2-15)),
                    self.survivalist_base, (l, searched)
                )
        else:
            return self.survivalist_base(l, searched)

        # if Tool.PICKAXE in l.tools and Tool.KNIFE not in l.tools\
        #         and searched[TileType.IRON]\
        #         and distance(self.world, self.players, searched[TileType.IRON][0][0],
        #                      searched[TileType.IRON][0][1], l) < 5:
        #     return scenario(
        #         self.craft, (Tool.KNIFE,l),
        #         self.mine_block, (l),
        #         self.go_to_nearest_resource, (l, searched, TileType.IRON),
        #     )
        #
        # # If turbine has enough lemons go scavenging
        # elif nearest_turbine_lemons(self, l, searched) >= 3:
        #     return scenario(
        #         self.mine_block, (l),
        #         self.go_to_nearest_resource, (l, searched, TileType.IRON),
        #         self.go_to_nearest_resource, (l, searched, TileType.STONE),
        #     )

    def survivalist_base(self, l: Lemur, searched: dict) -> Turn | None:
        return scenario(
            self.run_away_from_knives, (l),
            self.interact_turbine_tree, (l),
            self.go_to_lemon_tree, (l, searched),
            self.go_to_turbine, (l, searched),
        )

    def killer_turn(self, l: Lemur, searched):
        if Tool.KNIFE in l.tools:  # Knife stage
            return scenario(
                self.kill, (l),
                self.go_to_lemur, (find_nearest_safe_enemy(self, l), l),
                self.survivalist_turn, (l, searched)
            )

        # Has pickaxe but no knife - mine and craft a knife
        elif Tool.PICKAXE in l.tools:
            return scenario(
                self.craft, (Tool.KNIFE, l),
                self.mine_block, (l),
                self.go_to_nearest_resource, (l, searched, TileType.IRON),
                self.go_to_nearest_resource, (l, searched, TileType.STONE),
            )

        else:  # No tools
            return scenario(
                self.survivalist_turn, (l, searched)
            )

    def miner_turn(self: ProbojPlayer, l: Lemur, searched: dict):
        return self.survivalist_turn(l, searched)

    def crafter_turn(self, l: Lemur, searched):
        # No tree
        if len(searched[TileType.TREE]) == 0:
            nearest_turbine = step_to(self.world, self.players, searched[TileType.TURBINE][0][0], searched[TileType.TURBINE][0][1], l)
            if nearest_turbine is None:
                nearest_turbine = (None, None)
            return scenario(
                self.build, (TileType.TREE, l, nearest_turbine[0], nearest_turbine[1], self.world),
                self.mine_block, (l),
                self.go_to_nearest_resource, (l, searched, TileType.STONE)
            )

        # Has 2 pickaxes
        elif l.tools.count(Tool.PICKAXE) == 2:
            target = find_nearest_own_lemur(self, l, lambda x: x.tools.count(Tool.PICKAXE) == 0)
            return scenario(
                self.give_slot2, (l),
                self.go_to_lemur, (target, l)
            )

        elif l.tools[1] == Tool.KNIFE and (not everyone_has_item(self.myself.lemurs, Tool.KNIFE)):
            target = find_nearest_own_lemur(self, l, lambda x: x.tools.count(Tool.KNIFE) == 0)
            if target == l:
                self.log(f"[WARN]: Something really bad happened !!!!!!!!!")
            return scenario(
                self.give_slot2, (l),
                self.go_to_lemur, (target, l)
            )

        # Mine and craft pickaxes
        elif not everyone_has_item(self.myself.lemurs, Tool.PICKAXE):
            return scenario(
                self.mine_block, (l),
                self.craft, (Tool.PICKAXE, l),
                self.go_to_nearest_resource, (l, searched, TileType.STONE),
            )

        elif not everyone_has_item(self.myself.lemurs, Tool.KNIFE):
            return scenario(
                self.mine_block, (l),
                self.craft, (Tool.KNIFE, l),
                self.go_to_nearest_resource, (l, searched, TileType.IRON),
                self.go_to_nearest_resource, (l, searched, TileType.STONE)
            )

        else:
            return self.survivalist_turn(l, searched)

    def init_manager(self):
        if self.lemur_manager.initialized:
            return
        elif len(self.myself.lemurs) == 2:
            self.lemur_manager.crafters.append(self.myself.lemurs[0])
            self.lemur_manager.survivalists.append(self.myself.lemurs[1])

        elif len(self.myself.lemurs) >= 3:
            self.lemur_manager.crafters.append(self.myself.lemurs[0])
            self.lemur_manager.survivalists.append(self.myself.lemurs[1])
            self.lemur_manager.killers.extend(self.myself.lemurs[2:])
        else:
            self.lemur_manager.survivalists.extend(self.myself.lemurs)
        self.lemur_manager.initialized = True
        self.lemur_manager.everyone_reachable = is_everyone_reachable(self)


def scenario(*args) -> Turn | None:
    for func, arg in zip(args[::2], args[1::2]):
        if not isinstance(arg, Iterable):
            arg = (arg,)
        if turn := func(*arg):
            return turn

if __name__ == "__main__":
    p = LeMurPlayer()
    p.run()
