package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Stab(g *structs.Game, lemur *structs.Lemur, args []int) {
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		return
	}

	if !lemur.HasTool(structs.Knife) {
		return
	}

	target := g.LemurAt(c)
	if target == nil {
		return
	}

	g.Turn.Stabs = append(g.Turn.Stabs, structs.Stab{
		Attacker: lemur,
		Target:   target,
	})
}
