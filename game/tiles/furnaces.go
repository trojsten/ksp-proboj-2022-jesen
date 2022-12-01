package tiles

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
)

type FurnaceTile struct {
	Lemon    int
	Duration int
}

func (f *FurnaceTile) Type() TileType {
	return Furnace
}

func (f *FurnaceTile) SeeThrough() bool {
	return false
}

func (f *FurnaceTile) State() string {
	return fmt.Sprintf("%d %d", Furnace, f.Lemon)
}

func (f *FurnaceTile) Tick() {
	f.Duration--
	if f.Duration <= 0 {
		if f.Lemon > 0 {
			f.Lemon--
			f.Duration = constants.FurnaceLightDuration
		}
	}
}

func (f *FurnaceTile) AddItem(slot inventory.InventorySlot, quantity int) {
	if slot != inventory.Lemon {
		return
	}
	f.Lemon += quantity
}

func (f *FurnaceTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	// Intentionally not implemented.
}

func (f *FurnaceTile) CountItem(slot inventory.InventorySlot) int {
	if slot != inventory.Lemon {
		return 0
	}
	return f.Lemon
}

func NewFurnace() *FurnaceTile {
	return &FurnaceTile{}
}
