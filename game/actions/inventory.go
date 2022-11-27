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

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, turn.InventoryMove{
		From:     lemur,
		To:       nil,
		Slot:     slot,
		Quantity: quantity,
	})
}

func Put(g *game.Game, lemur *game.Lemur, args []int) {
	x, y := args[0], args[1]
	c := game.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	coords := game.Coordinate{
		X: x,
		Y: y,
	}

	var target inventory.Inventory = g.LemurAt(coords)

	// Tools cannot be stored in chests
	if target == nil && slot != inventory.Tool1 && slot != inventory.Tool2 {
		target = tiles.ChestAt(*g, coords)
	}
	if target == nil {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, turn.InventoryMove{
		From:     lemur,
		To:       target,
		Slot:     slot,
		Quantity: quantity,
	})
}

func Take(g *game.Game, lemur *game.Lemur, args []int) {
	x, y := args[0], args[1]
	c := game.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	// Tools can't be taken from chests
	if slot == inventory.Tool1 || slot == inventory.Tool2 {
		return
	}

	var chest inventory.Inventory = tiles.ChestAt(*g, game.Coordinate{
		X: x,
		Y: y,
	})

	if chest == nil {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, turn.InventoryMove{
		From:     chest,
		To:       lemur,
		Slot:     slot,
		Quantity: quantity,
	})
}
