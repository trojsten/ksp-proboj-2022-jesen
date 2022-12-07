package actions

import (
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func Build(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 3 {
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	tile := tiles.TileType(args[2])
	if tile != tiles.Turbine && tile != tiles.Wall && tile != tiles.Tree {
		return
	}

	g.Turn.TileChanges = append(g.Turn.TileChanges, structs.TileChange{
		Lemur: lemur,
		Where: c,
		To:    tile,
	})
}

func Break(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	g.Turn.TileChanges = append(g.Turn.TileChanges, structs.TileChange{
		Lemur: lemur,
		Where: c,
		To:    tiles.Empty,
	})
}
