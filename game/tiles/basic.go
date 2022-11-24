package tiles

type BasicTile struct {
	Tile TileType
}

func (b BasicTile) Type() TileType {
	return b.Tile
}

func NewBasic(tt TileType) BasicTile {
	return BasicTile{Tile: tt}
}
