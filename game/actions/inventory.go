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

	var target inventory.Inventory = g.LemurAt(coords)

	// Lemon can be put into turbines
	if target == nil && slot == inventory.Lemon {
		target = locate.TurbineAt(*g, coords)
	}
	if target == nil {
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
	x, y := args[0], args[1]
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

	var tree inventory.Inventory = locate.TreeAt(*g, c)
	if tree == nil {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     tree,
		To:       lemur,
		Slot:     slot,
		Quantity: quantity,
	})
}
