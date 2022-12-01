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
