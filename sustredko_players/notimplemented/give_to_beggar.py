from proboj import *
from util import *


def give_to_poor(self: ProbojPlayer, lemur: Lemur):
    for i in self.myself.lemurs:
        if (
            lemur.iron >= KNIFE_COST
            and i.role == LemurRoles.BEGGAR
            and i.iron < KNIFE_COST
        ):
            if abs(lemur.x - i.x) + abs(lemur.y - i.y) == 1:
                return Turn(Command.PUT, i.x, i.y, InventorySlot.IRON, KNIFE_COST)

        if lemur.stone >= PICKAXE_COST and i.role == LemurRoles.BROKE:
            if abs(lemur.x - i.x) + abs(lemur.y - i.y) == 1 and i.stone < PICKAXE_COST:
                return Turn(Command.PUT, i.x, i.y, InventorySlot.STONE, PICKAXE_COST)

        if i.role == LemurRoles.TRADER:
            if abs(lemur.x - i.x) + abs(lemur.y - i.y) == 1:
                iron_to_give = (
                    lemur.iron if Tool.KNIFE in lemur.tools else lemur.iron - KNIFE_COST
                )

                if iron_to_give > 0:
                    return Turn(Command.PUT, i.x, i.y, InventorySlot.IRON, iron_to_give)

    return STRATEGYFAIL
