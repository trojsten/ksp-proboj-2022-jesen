package tiles

type TileType int

const (
	Empty TileType = iota
	Stone
	Iron
	Tree
	Furnace
	Trap
	Unknown
)

type Tile interface {
	Type() TileType
	SeeThrough() bool
	State() string
	Tick()
}
