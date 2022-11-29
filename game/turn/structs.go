package turn

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
)

type Turn struct {
	Game            *game.Game
	Movements       []Movement
	TileChanges     []TileChange
	InventoryMoves  []InventoryMove
	MirrorTeleports []MirrorTeleport
	Crafts          []Craft
}

func (t *Turn) Settle() {
	// TODO: Settle combat
	t.SettleInventories()
	t.SettleBuilding()
	t.SettleMovements()
	// TODO: Settle deaths
}

type Movement struct {
	Lemur *game.Lemur
	From  game.Coordinate
	To    game.Coordinate
}

type MirrorTeleport struct {
	Lemur *game.Lemur
}

type TileChange struct {
	Lemur *game.Lemur
	Where game.Coordinate
	To    tiles.TileType
}

type InventoryMove struct {
	From     inventory.Inventory
	To       inventory.Inventory
	Slot     inventory.InventorySlot
	Quantity int
}

type Craft struct {
	Lemur *game.Lemur
	Tool  game.Tool
}
