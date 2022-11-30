package locate

import (
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func ChestAt(g structs.Game, coord structs.Coordinate) *tiles.ChestTile {
	chest, isChest := g.World.Tiles[coord.Y][coord.X].(*tiles.ChestTile)
	if !isChest {
		return nil
	}
	return chest
}

func TreeAt(g structs.Game, coord structs.Coordinate) *tiles.TreeTile {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.TreeTile)
	if !ok {
		return nil
	}
	return tile
}

func FurnaceAt(g structs.Game, coord structs.Coordinate) *tiles.FurnaceTile {
	tile, ok := g.World.Tiles[coord.Y][coord.X].(*tiles.FurnaceTile)
	if !ok {
		return nil
	}
	return tile
}
