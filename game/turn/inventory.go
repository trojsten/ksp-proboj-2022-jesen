package turn

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants/crafting"
	"ksp.sk/proboj/73/game/structs"
)

func SettleInventories(t *structs.Turn) {
	// Remove items from inventories
	for i, move := range t.InventoryMoves {
		if move.From == nil {
			continue
		}

		count := move.From.CountItem(move.Slot)
		if count < move.Quantity {
			t.InventoryMoves[i].Quantity = count
		}

		move.From.RemoveItem(move.Slot, move.Quantity)
	}

	// Add items to inventories
	for _, move := range t.InventoryMoves {
		if move.To == nil {
			continue
		}
		move.To.AddItem(move.Slot, move.Quantity)
	}

	// Craft items
	for _, craft := range t.Crafts {
		lemur := craft.Lemur
		recipe, ok := crafting.Recipes[craft.Tool]
		if !ok {
			t.Game.RejectSettle(fmt.Sprintf("_CRAFT %v", craft.Tool), craft.Lemur, "crafting recipe not found.")
			continue
		}

		if recipe.CanCraft(lemur) {
			recipe.Craft(lemur)
		}
	}
}
