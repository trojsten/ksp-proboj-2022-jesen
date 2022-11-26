package tiles

import "fmt"

type BasicTile struct {
	Tile TileType
}

func (b BasicTile) Type() TileType {
	return b.Tile
}

func (b BasicTile) State() string {
	return fmt.Sprintf("%d", b.Tile)
}

func NewBasic(tt TileType) BasicTile {
	return BasicTile{Tile: tt}
}
