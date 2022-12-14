package structs

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/globals"
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/libproboj"
)

type Game struct {
	Runner  libproboj.Runner `json:"-"`
	World   World            `json:"world"`
	Turn    Turn             `json:"-"`
	Players []*Player        `json:"players"`
	Scores  libproboj.Scores `json:"scores"`
}

func (g *Game) LemurAt(coord Coordinate) (*Lemur, bool) {
	for _, lemur := range g.Lemurs() {
		if lemur.Position == coord {
			return lemur, true
		}
	}
	return nil, false
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
	if globals.TurnNumber >= constants.MaxTurns {
		return false
	}

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

		if _, ok := g.LemurAt(spawnpoint.Position); ok {
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

	anyAliveLemur := false
	for _, lemur2 := range g.Players[lemur.Player].Lemurs {
		anyAliveLemur = anyAliveLemur || lemur2.Alive
	}

	g.Players[lemur.Player].Alive = anyAliveLemur
}

func (g *Game) TickLemur(l *Lemur) {
	if !l.Alive {
		return
	}

	if l.StunnedTime > 0 {
		l.StunnedTime--
	}

	if g.World.Oxygen[l.Position.Y][l.Position.X] <= 0 {
		// The lemur is standing in the dark
		l.TimeWithoutOxygen++
		if l.TimeWithoutOxygen >= constants.MaxTimeWithoutOxygen {
			g.KillLemur(l)
		}
	} else {
		l.TimeWithoutOxygen = 0
	}
}

func (g *Game) Reject(command string, args []int, lemur *Lemur, reason string) {
	g.Runner.Log(fmt.Sprintf("Rejected '%s %v' from %s: %s", command, args, g.Players[lemur.Player].Name, reason))
}

func (g *Game) RejectSettle(command string, lemur *Lemur, reason string) {
	g.Runner.Log(fmt.Sprintf("Rejected turn '%s' while settling from %s: %s", command, g.Players[lemur.Player].Name, reason))
}
