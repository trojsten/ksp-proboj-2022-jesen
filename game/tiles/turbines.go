package tiles

import (
	"encoding/json"
	"fmt"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
)

type TurbineTile struct {
	Lemon    int
	Duration int
}

func (f *TurbineTile) MarshalJSON() ([]byte, error) {
	return json.Marshal([]any{Turbine, f.Lemon})
}

func (f *TurbineTile) Type() TileType {
	return Turbine
}

func (f *TurbineTile) SeeThrough() bool {
	return false
}

func (f *TurbineTile) State() string {
	return fmt.Sprintf("%d %d", Turbine, f.Lemon)
}

func (f *TurbineTile) Tick() {
	f.Duration--
	if f.Duration <= 0 {
		if f.Lemon > 0 {
			f.Lemon--
			f.Duration = constants.TurbineOxygenDuration
		}
	}
}

func (f *TurbineTile) AddItem(slot inventory.InventorySlot, quantity int) {
	if slot != inventory.Lemon {
		return
	}
	f.Lemon += quantity
}

func (f *TurbineTile) RemoveItem(slot inventory.InventorySlot, quantity int) {
	// Intentionally not implemented.
}

func (f *TurbineTile) CountItem(slot inventory.InventorySlot) int {
	if slot != inventory.Lemon {
		return 0
	}
	return f.Lemon
}

func NewTurbine() *TurbineTile {
	return &TurbineTile{}
}
