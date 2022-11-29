package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/turn"
)

func Stab(g *game.Game, lemur *game.Lemur, args []int) {
	c := game.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		return
	}

	if !lemur.HasTool(game.Knife) {
		return
	}

	target := g.LemurAt(c)
	if target == nil {
		return
	}

	g.Turn.Stabs = append(g.Turn.Stabs, turn.Stab{
		Attacker: lemur,
		Target:   target,
	})
}
