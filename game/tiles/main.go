package tiles

type TileType int

const (
	Empty TileType = iota
	Stone
	Gold
	Tree
	Furnace
	Trap
	Chest
	Unknown
)

type Tile interface {
	Type() TileType
	SeeThrough() bool
	State() string
	Tick()
}
