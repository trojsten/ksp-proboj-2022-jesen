package tiles

import (
	"encoding/json"
	"fmt"
)

type BasicTile struct {
	Tile TileType
}

func (b BasicTile) MarshalJSON() ([]byte, error) {
	return json.Marshal([]TileType{b.Tile})
}

func (b BasicTile) Type() TileType {
	return b.Tile
}

func (b BasicTile) State() string {
	return fmt.Sprintf("%d", b.Tile)
}

func (b BasicTile) SeeThrough() bool {
	if b.Tile == Empty {
		return true
	}
	return false
}

func (b BasicTile) Tick() {
	// Intentionally left unimplemented.
}

func NewBasic(tt TileType) BasicTile {
	return BasicTile{Tile: tt}
}
