package locate

import (
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func TreeAt(g structs.Game, coord structs.Coordinate) *tiles.TreeTile {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.TreeTile)
	if !ok {
		return nil
	}
	return tile
}

func TurbineAt(g structs.Game, coord structs.Coordinate) *tiles.TurbineTile {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.TurbineTile)
	if !ok {
		return nil
	}
	return tile
}
