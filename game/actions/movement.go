package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/turn"
)

func Move(g *game.Game, lemur *game.Lemur, args []int) {
	c := game.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		return
	}

	g.Turn.Movements = append(g.Turn.Movements, turn.Movement{
		Lemur: lemur,
		From:  lemur.Position,
		To:    c,
	})
}

func Mirror(g *game.Game, lemur *game.Lemur, args []int) {
	g.Turn.MirrorTeleports = append(g.Turn.MirrorTeleports, turn.MirrorTeleport{Lemur: lemur})
}
