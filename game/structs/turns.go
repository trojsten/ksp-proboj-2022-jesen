package structs

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
)

type Turn struct {
	Game           *Game
	Movements      []Movement
	TileChanges    []TileChange
	InventoryMoves []InventoryMove
	Crafts         []Craft
	Stabs          []Stab
	Bonks          []Bonk
}

type Movement struct {
	Lemur *Lemur
	From  Coordinate
	To    Coordinate
}

type TileChange struct {
	Lemur *Lemur
	Where Coordinate
	To    tiles.TileType
}

type InventoryMove struct {
	From     inventory.Inventory
	To       inventory.Inventory
	Slot     inventory.InventorySlot
	Tool     Tool
	Quantity int
}

type Craft struct {
	Lemur *Lemur
	Tool  Tool
}

type Stab struct {
	Attacker *Lemur
	Target   *Lemur
}

type Bonk struct {
	Attacker *Lemur
	Target   *Lemur
}
