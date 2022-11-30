package structs

import (
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/libproboj"
)

type Game struct {
	Runner  libproboj.Runner
	World   World
	Turn    Turn
	Players []*Player
}

func (g *Game) LemurAt(coord Coordinate) *Lemur {
	for _, lemur := range g.Lemurs() {
		if lemur.Position == coord {
			return lemur
		}
	}
	return nil
}

func (g *Game) LemursAt(coord Coordinate) int {
	n := 0
	for _, lemur := range g.Lemurs() {
		if lemur.Position == coord {
			n++
		}
	}
	return n
}

func (g *Game) IsRunning() bool {
	playersAlive := 0
	for _, player := range g.Players {
		if player.Alive {
			playersAlive++
		}
	}

	return playersAlive > 1
}

func (g *Game) Lemurs() []*Lemur {
	lemurList := []*Lemur{}

	for _, player := range g.Players {
		if !player.Alive {
			continue
		}
		for _, lemur := range player.Lemurs {
			if !lemur.Alive {
				continue
			}
			lemurList = append(lemurList, lemur)
		}
	}

	return lemurList
}

// GetSpawnpoint finds the first empty spawnpoint for a given player
// the second return value indicates if finding the spawnpoint was
// successful
func (g *Game) GetSpawnpoint(player int) (Coordinate, bool) {
	for _, spawnpoint := range g.World.Spawnpoints {
		if spawnpoint.Player != player {
			continue
		}

		if g.LemurAt(spawnpoint.Position) != nil {
			continue
		}

		if g.World.Tiles[spawnpoint.Position.Y][spawnpoint.Position.X].Type() != tiles.Empty {
			continue
		}

		return spawnpoint.Position, true
	}
	return Coordinate{}, false
}

func (g *Game) KillLemur(lemur *Lemur) {
	lemur.Alive = false
}

func (g *Game) TickLemur(l *Lemur) {
	if !l.Alive {
		return
	}

	if g.World.Light[l.Position.Y][l.Position.X] <= 0 {
		// The lemur is standing in the dark
		l.TimeInDark++
		if l.TimeInDark >= constants.MaxTimeInDark {
			l.Alive = false
		}
	} else {
		l.TimeInDark = 0
	}
}
