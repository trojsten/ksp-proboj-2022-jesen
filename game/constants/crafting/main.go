package crafting

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/structs"
)

var Recipes = map[structs.Tool]Recipe{
	structs.Juicer:  {Stone: 3},
	structs.Pickaxe: {Stone: 2},
	structs.Knife:   {Iron: 1},
	structs.Stick:   {Iron: 5},
}

type Recipe struct {
	Tool  structs.Tool
	Lemon int
	Stone int
	Iron  int
}

func (r Recipe) CanCraft(inv inventory.Inventory) bool {
	if inv.CountItem(inventory.Lemon) < r.Lemon {
		return false
	}
	if inv.CountItem(inventory.Stone) < r.Stone {
		return false
	}
	if inv.CountItem(inventory.Iron) < r.Iron {
		return false
	}
	return true
}

func (r Recipe) Craft(lemur *structs.Lemur) {
	lemur.RemoveItem(inventory.Lemon, r.Lemon)
	lemur.RemoveItem(inventory.Stone, r.Stone)
	lemur.RemoveItem(inventory.Iron, r.Iron)

	lemur.AddTool(r.Tool)
}
