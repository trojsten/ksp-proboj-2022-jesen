package actions

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/locate"
	"ksp.sk/proboj/73/game/structs"
)

func Discard(g *structs.Game, lemur *structs.Lemur, args []int) {
	slot := inventory.InventorySlot(args[0])
	quantity := args[1]

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     lemur,
		To:       nil,
		Slot:     slot,
		Quantity: quantity,
	})
}

func Put(g *structs.Game, lemur *structs.Lemur, args []int) {
	x, y := args[1], args[0]
	c := structs.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	if quantity < 0 {
		return
	}

	coords := structs.Coordinate{
		X: x,
		Y: y,
	}

	var target inventory.Inventory
	target, ok := g.LemurAt(coords)

	// Lemon can be put into turbines
	if !ok && slot == inventory.Lemon {
		target, ok = locate.TurbineAt(*g, coords)
	}
	if !ok {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     lemur,
		To:       target,
		Slot:     slot,
		Quantity: quantity,
	})
}

func Take(g *structs.Game, lemur *structs.Lemur, args []int) {
	x, y := args[1], args[0]
	c := structs.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	if quantity < 0 {
		return
	}

	if slot != inventory.Lemon {
		return
	}

	tree, ok := locate.TreeAt(*g, c)
	if !ok {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     tree,
		To:       lemur,
		Slot:     slot,
		Quantity: quantity,
	})
}
