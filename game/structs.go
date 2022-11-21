package game

import (
	"ksp.sk/proboj/73/game/turn"
	"ksp.sk/proboj/73/libproboj"
)

type Game struct {
	runner  libproboj.Runner
	World   World
	Turn    turn.Turn
	Players []Player
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
	Lemurs      []Lemur
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

type Tool interface {
}

type World struct {
	Width  int
	Height int
	Tiles  [][]Tile
}

func (g Game) LemurAt(coord Coordinate) *Lemur {
	for _, player := range g.Players {
		for _, lemur := range player.Lemurs {
			if lemur.Position == coord {
				return &lemur
			}
		}
	}
	return nil
}
