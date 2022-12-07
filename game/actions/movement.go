package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Move(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		return
	}

	g.Turn.Movements = append(g.Turn.Movements, structs.Movement{
		Lemur: lemur,
		From:  lemur.Position,
		To:    c,
	})
}
