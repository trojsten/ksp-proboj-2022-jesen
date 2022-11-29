package game

import (
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
)

type World struct {
	Width   int
	Height  int
	Tiles   [][]tiles.Tile
	Visible [][]bool
	Light   [][]int
}

var Directions = [4][2]int{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}

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

type bfsEntry struct {
	Coordinate Coordinate
	Level      int
}

func (w *World) lightFrom(c Coordinate, level int) {
	var q []bfsEntry
	q = append(q, bfsEntry{
		Coordinate: c,
		Level:      level,
	})

	for len(q) > 0 {
		bfs := q[0]
		q = q[:1]

		if bfs.Level <= 0 {
			continue
		}

		if w.Light[bfs.Coordinate.Y][bfs.Coordinate.X] < bfs.Level {
			w.Light[bfs.Coordinate.Y][bfs.Coordinate.X] = bfs.Level
		}

		for _, d := range Directions {
			c2 := Coordinate{
				X: bfs.Coordinate.X + d[0],
				Y: bfs.Coordinate.Y + d[1],
			}

			if !w.ValidCoordinate(c2) {
				continue
			}

			q = append(q, bfsEntry{
				Coordinate: c2,
				Level:      bfs.Level - 1,
			})
		}
	}
}

func (w *World) UpdateLight(g *Game) {
	furnaces := []Coordinate{}

	for y := 0; y < w.Height; y++ {
		for x := 0; x < w.Width; x++ {
			w.Light[y][x] = 0
			if w.Tiles[y][x].Type() != tiles.Furnace {
				continue
			}
			c := Coordinate{X: x, Y: y}
			furnace := tiles.FurnaceAt(*g, c)
			if furnace.Duration > 0 {
				furnaces = append(furnaces, c)
			}
		}
	}

	for _, furnace := range furnaces {
		w.lightFrom(furnace, constants.FurnaceLightLevel)
	}

	for _, lemur := range g.Lemurs() {
		if lemur.LanternTime > 0 {
			// Lemur has turned on lantern
			if lemur.HasTool(Lantern) {
				lemur.LanternTime--
				w.lightFrom(lemur.Position, constants.LanternLightLevel)
			} else {
				lemur.LanternTime = 0
			}
		} else {
			// Lemur does not have a turned on lantern
			if lemur.HasTool(Lantern) && lemur.CountItem(inventory.Coal) > 0 {
				// But he has a lantern and some coal
				lemur.RemoveItem(inventory.Coal, 1)
				lemur.LanternTime = constants.FurnaceLightDuration
				w.lightFrom(lemur.Position, constants.LanternLightLevel)
			}
		}
	}
}
