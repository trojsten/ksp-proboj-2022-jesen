package game

import (
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

type Lemur struct {
	Position Coordinate
	Alive    bool
	Tools    [2]Tool
	Cocos    int
	Coal     int
	Stone    int
	Gold     int
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
	for _, player := range g.Players {
		for _, lemur := range player.Lemurs {
			if lemur.Position == coord {
				return lemur
			}
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
		for _, lemur := range player.Lemurs {
			lemurs = append(lemurs, lemur)
		}
	}

	return lemurs
}
