package turn

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
)

type Turn struct {
	Game              *game.Game
	Movements         []Movement
	TileChanges       []TileChange
	InventoryExtracts []InventoryExtract
	InventoryInserts  []InventoryInsert
}

func (t Turn) Settle() {
	// TODO: Settle combat
	// TODO: Settle inventories
	t.SettleBuilding()
	t.SettleMovements()
	// TODO: Settle deaths
}

type Movement struct {
	Lemur *game.Lemur
	From  game.Coordinate
	To    game.Coordinate
}

type TileChange struct {
	Lemur *game.Lemur
	Where game.Coordinate
	To    tiles.TileType
}

type InventoryExtract struct {
	Inventory inventory.Inventory
	Slot      inventory.InventorySlot
	Quantity  int
}

type InventoryInsert struct {
	Inventory inventory.Inventory
	Slot      inventory.InventorySlot
	Quantity  int
}
