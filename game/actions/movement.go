package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/turn"
)

func Move(g *game.Game, lemur *game.Lemur, args []int) {
	// TODO: Validate X, Y
	g.Turn.Movements = append(g.Turn.Movements, turn.Movement{
		Lemur: lemur,
		From:  lemur.Position,
		To:    game.Coordinate{X: args[0], Y: args[1]},
	})
}

func Mirror(g *game.Game, lemur *game.Lemur, args []int) {
	// TODO: Check if lemur has mirror
	g.Turn.Movements = append(g.Turn.Movements, turn.Movement{
		Lemur: lemur,
		From:  lemur.Position,
		To:    game.Coordinate{X: 0, Y: 0}, // TODO: Real spawnpoint
	})
}
