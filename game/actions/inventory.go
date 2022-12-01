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
	x, y := args[0], args[1]
	c := structs.Coordinate{X: x, Y: y}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	slot := inventory.InventorySlot(args[2])
	quantity := args[3]

	coords := structs.Coordinate{
		X: x,
		Y: y,
	}

	var target inventory.Inventory = g.LemurAt(coords)

	// Tools cannot be stored in chests
	if target == nil && slot != inventory.Tool1 && slot != inventory.Tool2 {
		target = locate.ChestAt(*g, coords)
	}
	// Lemon can be put into furnace
	if target == nil && slot == inventory.Lemon {
		target = locate.FurnaceAt(*g, coords)
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

	// Tools can't be taken from chests
	if slot == inventory.Tool1 || slot == inventory.Tool2 {
		return
	}

	var chest inventory.Inventory = locate.ChestAt(*g, c)

	// Cocos can be taken from trees
	if chest == nil && slot == inventory.Cocos {
		chest = locate.TreeAt(*g, c)
	}
	if chest == nil {
		return
	}

	g.Turn.InventoryMoves = append(g.Turn.InventoryMoves, structs.InventoryMove{
		From:     chest,
		To:       lemur,
		Slot:     slot,
		Quantity: quantity,
	})
}
