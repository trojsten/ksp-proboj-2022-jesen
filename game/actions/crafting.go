package actions

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/turn"
)

func Craft(g *game.Game, lemur *game.Lemur, args []int) {
	tool := game.Tool(args[0])

	g.Turn.Crafts = append(g.Turn.Crafts, turn.Craft{
		Lemur: lemur,
		Tool:  tool,
	})
}
