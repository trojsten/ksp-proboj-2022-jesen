package actions

import (
	"ksp.sk/proboj/73/game/structs"
)

func Craft(g *structs.Game, lemur *structs.Lemur, args []int) {
	tool := structs.Tool(args[0])

	g.Turn.Crafts = append(g.Turn.Crafts, structs.Craft{
		Lemur: lemur,
		Tool:  tool,
	})
}
