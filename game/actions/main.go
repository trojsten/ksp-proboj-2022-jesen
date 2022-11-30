package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

type ActionHandler func(g *structs.Game, lemur *structs.Lemur, args []int)

func Get(action string) ActionHandler {
	switch action {
	case "NOOP":
		return Noop

	case "STAB":
		return Stab

	case "BUILD":
		return Build
	case "BREAK":
		return Break

	case "DISCARD":
		return Discard
	case "PUT":
		return Put
	case "TAKE":
		return Take
	case "CRAFT":
		return Craft

	case "MOVE":
		return Move
	case "MIRROR":
		return Mirror
	}

	return Noop
}
