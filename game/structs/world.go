package structs

import (
	"ksp.sk/proboj/73/game/tiles"
)

type World struct {
	Width       int
	Height      int
	Tiles       [][]tiles.Tile
	Visible     [][]bool
	Light       [][]int
	Spawnpoints []Spawnpoint
}

type Spawnpoint struct {
	Position Coordinate
	Player   int
}

func (w *World) visibleFrom(coord Coordinate) {
	if w.Visible[coord.Y][coord.X] {
		return
	}

	q := []Coordinate{coord}
	for len(q) > 0 {
		c := q[0]
		q = q[1:]

		for _, d := range Directions {
			nx, ny := c.X+d[0], c.Y+d[1]
			if !w.ValidCoordinate(c) || w.Visible[ny][nx] {
				continue
			}

			w.Visible[ny][nx] = true

			if w.Tiles[ny][nx].SeeThrough() {
				q = append(q, Coordinate{X: nx, Y: ny})
			}
		}
	}
}

func (w *World) ValidCoordinate(c Coordinate) bool {
	if c.X < 0 || c.Y < 0 {
		return false
	}

	if c.X >= w.Width || c.Y >= w.Height {
		return false
	}

	return true
}

func (w *World) UpdateVisibility(g *Game) {
	for y := 0; y < w.Height; y++ {
		for x := 0; x < w.Width; x++ {
			w.Visible[y][x] = false
		}
	}

	for _, lemur := range g.Lemurs() {
		w.visibleFrom(lemur.Position)
	}
}

func (w *World) Tick() {
	for y := 0; y < w.Height; y++ {
		for x := 0; x < w.Width; x++ {
			w.Tiles[y][x].Tick()
		}
	}
}