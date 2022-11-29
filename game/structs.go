package game

import (
	"ksp.sk/proboj/73/game/tiles"
	"ksp.sk/proboj/73/game/turn"
	"ksp.sk/proboj/73/libproboj"
)

type Game struct {
	runner  libproboj.Runner
	World   World
	Turn    turn.Turn
	Players []*Player
}

type Coordinate struct {
	X int
	Y int
}

type Player struct {
	Idx         int
	Name        string
	Color       string
	DisplayName string
	Alive       bool
	Lemurs      []*Lemur
}

type Tool int

const (
	Lantern Tool = iota
	Pickaxe
	Hammer
	Knife
	Mirror
	Gun
	NoTool
)

func (g *Game) LemurAt(coord Coordinate) *Lemur {
	for _, lemur := range g.Lemurs() {
		if lemur.Position == coord {
			return lemur
		}
	}
	return nil
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

func (p *Player) Kill(g *Game) {
	// TODO: score
	p.Alive = false
	g.runner.KillPlayer(p.Name)
}

func (g *Game) Lemurs() []*Lemur {
	lemurs := []*Lemur{}

	for _, player := range g.Players {
		if !player.Alive {
			continue
		}
		for _, lemur := range player.Lemurs {
			if !lemur.Alive {
				continue
			}
			lemurs = append(lemurs, lemur)
		}
	}

	return lemurs
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
