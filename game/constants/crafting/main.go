package crafting

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/structs"
)

var Recipes = map[structs.Tool]Recipe{
	structs.Lantern: {Cocos: 1, Coal: 1},
	structs.Pickaxe: {Stone: 1, Coal: 1},
	structs.Hammer:  {Cocos: 1, Stone: 1},
	structs.Knife:   {Gold: 1, Stone: 1},
	structs.Mirror:  {Gold: 1, Coal: 1},
	structs.Gun:     {Gold: 1, Cocos: 1},
}

type Recipe struct {
	Tool  structs.Tool
	Cocos int
	Coal  int
	Stone int
	Gold  int
}

func (r Recipe) CanCraft(inv inventory.Inventory) bool {
	if inv.CountItem(inventory.Cocos) < r.Cocos {
		return false
	}
	if inv.CountItem(inventory.Coal) < r.Coal {
		return false
	}
	if inv.CountItem(inventory.Stone) < r.Stone {
		return false
	}
	if inv.CountItem(inventory.Gold) < r.Gold {
		return false
	}
	return true
}

func (r Recipe) Craft(lemur *structs.Lemur) {
	lemur.RemoveItem(inventory.Cocos, r.Cocos)
	lemur.RemoveItem(inventory.Coal, r.Coal)
	lemur.RemoveItem(inventory.Stone, r.Stone)
	lemur.RemoveItem(inventory.Gold, r.Gold)

	lemur.AddTool(r.Tool)
}