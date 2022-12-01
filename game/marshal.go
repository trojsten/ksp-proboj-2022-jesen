package game

import (
	"fmt"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
	"strconv"
	"strings"
)

func StateForPlayer(g *structs.Game, player int) string {
	b := strings.Builder{}

	// Section 1 - WORLD
	b.WriteString(fmt.Sprintf("%d %d\n", g.World.Width, g.World.Height))
	for y := 0; y < g.World.Height; y++ {
		line := []string{}
		for x := 0; x < g.World.Width; x++ {
			if g.World.Visible[y][x] {
				line = append(line, g.World.Tiles[y][x].State())
			} else {
				line = append(line, tiles.BasicTile{Tile: tiles.Unknown}.State())
			}
		}
		b.WriteString(fmt.Sprintf("%s\n", strings.Join(line, " ")))
	}

	// Section 2 - PLAYERS
	b.WriteString(fmt.Sprintf("%d %d\n", len(g.Players), player))
	for _, p := range g.Players {
		b.WriteString(fmt.Sprintf("%d\n", len(p.Lemurs)))
		for _, lemur := range p.Lemurs {
			if lemur.Alive {
				tools := []string{}
				for _, tool := range lemur.Tools {
					tools = append(tools, strconv.Itoa(int(tool)))
				}
				b.WriteString(fmt.Sprintf("1 %d %d %d %d %d %s\n", lemur.Position.X, lemur.Position.Y, lemur.Gold, lemur.Lemon, lemur.Stone, strings.Join(tools, " ")))
			} else {
				b.WriteString("0\n")
			}
		}
	}

	// Section 3 - LIGHT
	for y := 0; y < g.World.Height; y++ {
		line := []string{}
		for x := 0; x < g.World.Width; x++ {
			line = append(line, strconv.Itoa(g.World.Light[y][x]))
		}
		b.WriteString(fmt.Sprintf("%s\n", strings.Join(line, " ")))
	}

	return b.String()
}
