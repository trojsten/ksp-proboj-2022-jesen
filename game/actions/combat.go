package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Stab(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		g.Reject("STAB", args, lemur, "invalid number of arguments.")
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) || !lemur.CanReach(c) {
		g.Reject("STAB", args, lemur, "target coordinates are unreachable.")
		return
	}

	if !lemur.HasTool(structs.Knife) {
		g.Reject("STAB", args, lemur, "lemur does not have a knife.")
		return
	}

	target, ok := g.LemurAt(c)
	if !ok {
		g.Reject("STAB", args, lemur, "there is no lemur at target coordinates.")
		return
	}

	g.Turn.Stabs = append(g.Turn.Stabs, structs.Stab{
		Attacker: lemur,
		Target:   target,
	})
}

func Bonk(g *structs.Game, lemur *structs.Lemur, args []int) {
	if len(args) != 2 {
		g.Reject("BONK", args, lemur, "invalid number of arguments.")
		return
	}
	c := structs.Coordinate{X: args[0], Y: args[1]}
	if !g.World.ValidCoordinate(c) {
		g.Reject("BONK", args, lemur, "target coordinates are unreachable.")
		return
	}

	if c.X-lemur.Position.X < -2 || c.X-lemur.Position.X > 2 {
		g.Reject("BONK", args, lemur, "target coordinates are unreachable.")
		return
	}
	if c.Y-lemur.Position.Y < -2 || c.Y-lemur.Position.Y > 2 {
		g.Reject("BONK", args, lemur, "target coordinates are unreachable.")
		return
	}

	if !lemur.HasTool(structs.Stick) {
		g.Reject("BONK", args, lemur, "lemur does not have a stick.")
		return
	}

	target, ok := g.LemurAt(c)
	if !ok {
		g.Reject("BONK", args, lemur, "there is no lemur at target coordinates.")
		return
	}

	g.Turn.Bonks = append(g.Turn.Bonks, structs.Bonk{
		Attacker: lemur,
		Target:   target,
	})
}
