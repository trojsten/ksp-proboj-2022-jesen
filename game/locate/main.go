package locate

import (
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func TreeAt(g structs.Game, coord structs.Coordinate) (*tiles.TreeTile, bool) {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.TreeTile)
	return tile, ok
}

func TurbineAt(g structs.Game, coord structs.Coordinate) (*tiles.TurbineTile, bool) {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.TurbineTile)
	return tile, ok
}
