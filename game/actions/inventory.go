package actions

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/locate"
	"ksp.sk/proboj/73/game/structs"
)

func Discard(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		g.Reject("DISCARD", args, lemur, "invalid number of arguments.")
		return
	}
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
	if len(args) != 4 {
		g.Reject("PUT", args, lemur, "invalid number of arguments.")
		return
	}
	x, y := args[0], args[1]
	c := structs.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		g.Reject("PUT", args, lemur, "target coordinates are unreachable.")
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	if quantity < 0 {
		g.Reject("PUT", args, lemur, "quantity must be a non-negative number.")
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
		g.Reject("PUT", args, lemur, "there is no inventory at the coordinates.")
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
	if len(args) != 4 {
		g.Reject("TAKE", args, lemur, "invalid number of arguments.")
		return
	}
	x, y := args[0], args[1]
	c := structs.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		g.Reject("TAKE", args, lemur, "target coordinates are unreachable.")
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	if quantity < 0 {
		g.Reject("TAKE", args, lemur, "quantity must be a non-negative number.")
		return
	}

	if slot != inventory.Lemon {
		g.Reject("TAKE", args, lemur, "slot must be lemon.")
		return
	}

	tree, ok := locate.TreeAt(*g, c)
	if !ok {
		g.Reject("TAKE", args, lemur, "no tree found at coordinates.")
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     tree,
		To:       lemur,
		Slot:     slot,
		Quantity: quantity,
	})
}
