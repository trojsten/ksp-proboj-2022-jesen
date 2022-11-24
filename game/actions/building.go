package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/game/turn"
)

func Build(g *game.Game, lemur *game.Lemur, args []int) {
	// TODO: Check tool, building type and material
	// TODO: Check coordinates
	g.Turn.TileChanges = append(g.Turn.TileChanges, turn.TileChange{
		Lemur: lemur,
		Where: game.Coordinate{X: args[0], Y: args[1]},
		To:    tiles.TileType(args[2]),
	})
}

func Break(g *game.Game, lemur *game.Lemur, args []int) {
	// TODO: Check tool
	// TODO: Check coordinates
	g.Turn.TileChanges = append(g.Turn.TileChanges, turn.TileChange{
		Lemur: lemur,
		Where: game.Coordinate{X: args[0], Y: args[1]},
		To:    tiles.Empty,
	})
}
