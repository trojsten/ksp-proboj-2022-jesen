package tiles

import (
	"fmt"
	"ksp.sk/proboj/73/game/inventory"
)

type FurnaceTile struct {
	Coal int
}

func (f *FurnaceTile) Type() TileType {
	return Furnace
}

func (f *FurnaceTile) SeeThrough() bool {
	return false
}

func (f *FurnaceTile) State() string {
	return fmt.Sprintf("%d %d", Furnace, f.Coal)
}

func (f *FurnaceTile) AddItem(slot inventory.InventorySlot, quantity int) {
	if slot != inventory.Coal {
		return
	}
	f.Coal += quantity
}

func (f *FurnaceTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	// Intentionally not implemented.
}

func (f *FurnaceTile) CountItem(slot inventory.InventorySlot) int {
	if slot != inventory.Coal {
		return 0
	}
	return f.Coal
}

func NewFurnace() *FurnaceTile {
	return &FurnaceTile{}
}
