package tiles

import (
	"fmt"
	"ksp.sk/proboj/73/game/inventory"
)

type ChestTile struct {
	Lemon int
	Stone int
	Gold  int
}

func (t *ChestTile) Type() TileType {
	return Chest
}

func (t *ChestTile) State() string {
	return fmt.Sprintf("%d %d %d %d", Chest, t.Gold, t.Lemon, t.Stone)
}

func (t *ChestTile) SeeThrough() bool {
	return false
}

func (t *ChestTile) Tick() {
	// Intentionally left unimplemented.
}

func (t *ChestTile) AddItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Gold:
		t.Gold += quantity
	case inventory.Lemon:
		t.Lemon += quantity
	case inventory.Stone:
		t.Stone += quantity
	}
}

func (t *ChestTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Gold:
		if t.Gold < quantity {
			t.Gold = 0
		} else {
			t.Gold -= quantity
		}
	case inventory.Lemon:
		if t.Lemon < quantity {
			t.Lemon = 0
		} else {
			t.Lemon -= quantity
		}
	case inventory.Stone:
		if t.Stone < quantity {
			t.Stone = 0
		} else {
			t.Stone -= quantity
		}
	}
}

func (t *ChestTile) CountItem(slot inventory.InventorySlot) int {
	switch slot {
	case inventory.Gold:
		return t.Gold
	case inventory.Lemon:
		return t.Lemon
	case inventory.Stone:
		return t.Stone
	}
	return 0
}

func NewChest() *ChestTile {
	return &ChestTile{}
}
