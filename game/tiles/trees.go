package tiles

import (
	"encoding/json"
	"fmt"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
)

type TreeTile struct {
	HasLemon bool
	Growth   int
}

func (t *TreeTile) Type() TileType {
	return Tree
}

func (t *TreeTile) MarshalJSON() ([]byte, error) {
	return json.Marshal([]any{Tree, t.HasLemon})
}

func (t *TreeTile) SeeThrough() bool {
	return false
}

func (t *TreeTile) State() string {
	if t.HasLemon {
		return fmt.Sprintf("%d 1", Tree)
	}
	return fmt.Sprintf("%d 0", Tree)
}

func (t *TreeTile) Tick() {
	if t.HasLemon {
		return
	}

	t.Growth--
	if t.Growth <= 0 {
		t.HasLemon = true
		t.Growth = constants.TreeGrowthRate
	}
}

func (t *TreeTile) AddItem(slot inventory.InventorySlot, quantity int) {
	// Intentionally not implemented.
}

func (t *TreeTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	if slot != inventory.Lemon {
		return
	}
	t.HasLemon = false
}

func (t *TreeTile) CountItem(slot inventory.InventorySlot) int {
	if slot != inventory.Lemon {
		return 0
	}

	if t.HasLemon {
		return 1
	} else {
		return 0
	}
}

func NewTree() *TreeTile {
	return &TreeTile{Growth: constants.TreeGrowthRate}
}
