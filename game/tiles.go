package game

type TileType int

const (
	Empty TileType = iota
	Stone
	Gold
	Coal
	Tree
	Furnace
	Trap
	Chest
	Unknown
)

type Tile interface {
	Type() TileType
}
