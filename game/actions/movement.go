package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Move(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		g.Reject("MOVE", args, lemur, "invalid number of arguments.")
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		g.Reject("MOVE", args, lemur, "target coordinates are unreachable.")
		return
	}

	g.Turn.Movements = append(g.Turn.Movements, structs.Movement{
		Lemur: lemur,
		From:  lemur.Position,
		To:    c,
	})
}
