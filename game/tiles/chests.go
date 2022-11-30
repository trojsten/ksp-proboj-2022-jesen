package tiles

import (
	"fmt"
	"ksp.sk/proboj/73/game/inventory"
)

type ChestTile struct {
	Cocos int
	Coal  int
	Stone int
	Gold  int
}

func (t *ChestTile) Type() TileType {
	return Chest
}

func (t *ChestTile) State() string {
	return fmt.Sprintf("%d %d %d %d %d", Chest, t.Cocos, t.Gold, t.Coal, t.Stone)
}

func (t *ChestTile) SeeThrough() bool {
	return false
}

func (t *ChestTile) Tick() {
	// Intentionally left unimplemented.
}

func (t *ChestTile) AddItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Cocos:
		t.Cocos += quantity
	case inventory.Gold:
		t.Gold += quantity
	case inventory.Coal:
		t.Coal += quantity
	case inventory.Stone:
		t.Stone += quantity
	}
}

func (t *ChestTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Cocos:
		if t.Cocos < quantity {
			t.Cocos = 0
		} else {
			t.Cocos -= quantity
		}
	case inventory.Gold:
		if t.Gold < quantity {
			t.Gold = 0
		} else {
			t.Gold -= quantity
		}
	case inventory.Coal:
		if t.Coal < quantity {
			t.Coal = 0
		} else {
			t.Coal -= quantity
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
	case inventory.Cocos:
		return t.Cocos
	case inventory.Gold:
		return t.Gold
	case inventory.Coal:
		return t.Coal
	case inventory.Stone:
		return t.Stone
	}
	return 0
}

func NewChest() *ChestTile {
	return &ChestTile{}
}
