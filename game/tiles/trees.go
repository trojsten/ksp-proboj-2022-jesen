package tiles

import (
	"fmt"
	"ksp.sk/proboj/73/game/inventory"
)

type TreeTile struct {
	HasCocos bool
}

func (t *TreeTile) Type() TileType {
	return Tree
}

func (t *TreeTile) SeeThrough() bool {
	return false
}

func (t *TreeTile) State() string {
	if t.HasCocos {
		return fmt.Sprintf("%d 1", Tree)
	}
	return fmt.Sprintf("%d 0", Tree)
}

func (t *TreeTile) AddItem(slot inventory.InventorySlot, quantity int) {
	// Intentionally not implemented.
}

func (t *TreeTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	if slot != inventory.Cocos {
		return
	}
	t.HasCocos = false
}

func (t *TreeTile) CountItem(slot inventory.InventorySlot) int {
	if slot != inventory.Cocos {
		return 0
	}

	if t.HasCocos {
		return 1
	} else {
		return 0
	}
}

func NewTree() *TreeTile {
	return &TreeTile{}
}