package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/game/turn"
)

func Discard(g *game.Game, lemur *game.Lemur, args []int) {
	slot := inventory.InventorySlot(args[0])
	quantity := args[1]

	g.Turn.InventoryExtracts = append(g.Turn.InventoryExtracts, turn.InventoryExtract{
		Inventory: lemur,
		Slot:      slot,
		Quantity:  quantity,
	})
}

func Put(g *game.Game, lemur *game.Lemur, args []int) {
	x, y := args[0], args[1]
	slot := inventory.InventorySlot(args[2])
	quantity := args[3]
	realCount := lemur.CountItem(slot)
	if realCount < quantity {
		quantity = realCount
	}

	coords := game.Coordinate{
		X: x,
		Y: y,
	}

	var target inventory.Inventory = g.LemurAt(coords)

	if target == nil {
		target = tiles.ChestAt(*g, coords)
	}
	if target == nil {
		return
	}

	g.Turn.InventoryExtracts = append(g.Turn.InventoryExtracts, turn.InventoryExtract{
		Inventory: lemur,
		Slot:      slot,
		Quantity:  quantity,
	})

	g.Turn.InventoryInserts = append(g.Turn.InventoryInserts, turn.InventoryInsert{
		Inventory: target,
		Slot:      slot,
		Quantity:  quantity,
	})
}

func Take(g *game.Game, lemur *game.Lemur, args []int) {
	x, y := args[0], args[1]
	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	var chest inventory.Inventory = g.ChestAt(game.Coordinate{
		X: x,
		Y: y,
	})

	if chest == nil {
		return
	}

	realCount := chest.CountItem(slot)

	if realCount < quantity {
		quantity = realCount
	}

	//TODO co ak si zoberie vela lemurov naraz z jednej chestky?
	g.Turn.InventoryExtracts = append(g.Turn.InventoryExtracts, turn.InventoryExtract{
		Inventory: chest,
		Slot:      slot,
		Quantity:  quantity,
	})

	g.Turn.InventoryInserts = append(g.Turn.InventoryInserts, turn.InventoryInsert{
		Inventory: lemur,
		Slot:      slot,
		Quantity:  quantity,
	})
}
