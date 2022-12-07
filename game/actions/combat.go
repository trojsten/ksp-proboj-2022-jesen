package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Stab(g *structs.Game, lemur *structs.Lemur, args []int) {
	c := structs.Coordinate{X: args[1], Y: args[0]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		return
	}

	if !lemur.HasTool(structs.Knife) {
		return
	}

	target, ok := g.LemurAt(c)
	if !ok {
		return
	}

	g.Turn.Stabs = append(g.Turn.Stabs, structs.Stab{
		Attacker: lemur,
		Target:   target,
	})
}

func Bonk(g *structs.Game, lemur *structs.Lemur, args []int) {
	c := structs.Coordinate{X: args[1], Y: args[0]}
	if !g.World.ValidCoordinate(c) {
		return
	}

	if c.X-lemur.Position.X < -2 || c.X-lemur.Position.X > 2 {
		return
	}
	if c.Y-lemur.Position.Y < -2 || c.Y-lemur.Position.Y > 2 {
		return
	}

	if !lemur.HasTool(structs.Stick) {
		return
	}

	target, ok := g.LemurAt(c)
	if !ok {
		return
	}

	g.Turn.Bonks = append(g.Turn.Bonks, structs.Bonk{
		Attacker: lemur,
		Target:   target,
	})
}
