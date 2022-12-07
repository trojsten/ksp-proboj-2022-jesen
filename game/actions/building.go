package actions

import (
	"fmt"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func Build(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 3 {
		g.Reject("BUILD", args, lemur, "invalid number of arguments.")
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		g.Reject("BUILD", args, lemur, "target coordinates are unreachable.")
		return
	}

	tile := tiles.TileType(args[2])
	if tile != tiles.Turbine && tile != tiles.Wall && tile != tiles.Tree {
		g.Reject("BUILD", args, lemur, fmt.Sprintf("tile type %v is not buildable.", tile))
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
		g.Reject("BREAK", args, lemur, "invalid number of arguments.")
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
