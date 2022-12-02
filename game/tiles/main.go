package tiles

type TileType int

const (
	Empty TileType = iota
	Stone
	Iron
	Tree
	Turbine
	Wall
	Unknown
)

type Tile interface {
	Type() TileType
	SeeThrough() bool
	State() string
	Tick()
}

func NewTile(tile TileType) Tile {
	switch tile {
	case Turbine:
		return NewTurbine()
	case Tree:
		return NewTree()
	default:
		return NewBasic(tile)
	}
}
