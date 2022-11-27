package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/game/turn"
)

func Build(g *game.Game, lemur *game.Lemur, args []int) {
	c := game.Coordinate{X: args[0], Y: args[1]}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	tile := tiles.TileType(args[2])
	if tile != tiles.Chest && tile != tiles.Furnace && tile != tiles.Trap && tile != tiles.Tree {
		return
	}

	g.Turn.TileChanges = append(g.Turn.TileChanges, turn.TileChange{
		Lemur: lemur,
		Where: c,
		To:    tile,
	})
}

func Break(g *game.Game, lemur *game.Lemur, args []int) {
	c := game.Coordinate{X: args[0], Y: args[1]}
	if !lemur.CanReach(c) || !g.World.ValidCoordinate(c) {
		return
	}

	g.Turn.TileChanges = append(g.Turn.TileChanges, turn.TileChange{
		Lemur: lemur,
		Where: c,
		To:    tiles.Empty,
	})
}
