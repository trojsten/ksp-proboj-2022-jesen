package turn

import (
	"ksp.sk/proboj/73/game/constants"
)

func (t *Turn) SettleInventories() {
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
		recipe, ok := constants.Recipes[craft.Tool]
		if !ok {
			continue
		}

		if recipe.CanCraft(lemur) {
			recipe.Craft(lemur)
		}
	}
}
