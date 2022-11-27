package game

import (
	"fmt"
	"ksp.sk/proboj/73/game/tiles"
	"strings"
)

func (g *Game) StateForPlayer(player int) string {
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
				// TODO: Tools
				b.WriteString(fmt.Sprintf("1 %d %d %d %d %d %d\n", lemur.Position.X, lemur.Position.Y, lemur.Cocos, lemur.Gold, lemur.Coal, lemur.Stone))
			} else {
				b.WriteString("0\n")
			}
		}
	}

	// TODO: Section 3 - Light

	return b.String()
}
