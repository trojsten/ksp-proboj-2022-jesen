package turn

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants/crafting"
	"ksp.sk/proboj/73/game/inventory"
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

		if move.Slot == inventory.Tool1 || move.Slot == inventory.Tool2 {
			lemur, ok := move.From.(*structs.Lemur)
			if !ok {
				t.Game.Runner.Log(fmt.Sprintf("Rejecting InventoryMove, tried to move Tool from a non-lemur inventory."))
				t.InventoryMoves[i].To = nil
				continue
			}
			if move.Slot == inventory.Tool1 {
				t.InventoryMoves[i].Tool = lemur.Tools[0]
			} else {
				t.InventoryMoves[i].Tool = lemur.Tools[1]
			}
		}

		move.From.RemoveItem(move.Slot, move.Quantity)
	}

	// Add items to inventories
	for _, move := range t.InventoryMoves {
		if move.To == nil {
			continue
		}

		if move.Slot == inventory.Tool1 || move.Slot == inventory.Tool2 {
			lemur, ok := move.To.(*structs.Lemur)
			if !ok {
				t.Game.Runner.Log(fmt.Sprintf("Rejecting InventoryMove, tried to move Tool to a non-lemur inventory."))
				continue
			}
			lemur.AddTool(move.Tool)
		} else {
			move.To.AddItem(move.Slot, move.Quantity)
		}

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
