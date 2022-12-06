package oxygen

import (
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/locate"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

type bfsEntry struct {
	Coordinate structs.Coordinate
	Level      int
}

func oxygenFrom(w *structs.World, c structs.Coordinate, level int) {
	var q []bfsEntry
	q = append(q, bfsEntry{
		Coordinate: c,
		Level:      level,
	})

	for len(q) > 0 {
		bfs := q[0]
		q = q[1:]

		if bfs.Level <= 0 {
			continue
		}

		if w.Oxygen[bfs.Coordinate.Y][bfs.Coordinate.X] < bfs.Level {
			w.Oxygen[bfs.Coordinate.Y][bfs.Coordinate.X] = bfs.Level
		}

		for _, d := range structs.Directions {
			c2 := structs.Coordinate{
				X: bfs.Coordinate.X + d[0],
				Y: bfs.Coordinate.Y + d[1],
			}

			if !w.ValidCoordinate(c2) {
				continue
			}

			if w.Oxygen[c2.Y][c2.X] >= w.Oxygen[bfs.Coordinate.Y][bfs.Coordinate.X] {
				continue
			}

			if !w.Visible[c2.Y][c2.X] {
				continue
			}

			q = append(q, bfsEntry{
				Coordinate: c2,
				Level:      bfs.Level - 1,
			})
		}
	}
}

func Update(g *structs.Game) {
	w := &g.World
	turbines := []structs.Coordinate{}

	for y := 0; y < w.Height; y++ {
		for x := 0; x < w.Width; x++ {
			w.Oxygen[y][x] = 0
			if w.Tiles[y][x].Type() != tiles.Turbine {
				continue
			}
			c := structs.Coordinate{X: x, Y: y}
			turbine := locate.TurbineAt(*g, c)
			if turbine.Duration > 0 {
				turbines = append(turbines, c)
			}
		}
	}

	for _, turbine := range turbines {
		oxygenFrom(w, turbine, constants.TurbineOxygenLevel)
	}

	for _, lemur := range g.Lemurs() {
		if lemur.JuicerTime > 0 {
			// Lemur has turned on juicer
			if lemur.HasTool(structs.Juicer) {
				lemur.JuicerTime--
				oxygenFrom(w, lemur.Position, constants.JuicerOxygenLevel)
			} else {
				lemur.JuicerTime = 0
			}
		} else {
			// Lemur does not have a turned on juicer
			if lemur.HasTool(structs.Juicer) && lemur.CountItem(inventory.Lemon) > 0 && w.Oxygen[lemur.Position.Y][lemur.Position.X] <= 0 {
				// But he has a juicer and some lemons
				lemur.RemoveItem(inventory.Lemon, 1)
				lemur.JuicerTime = constants.JuicerOxygenDuration
				oxygenFrom(w, lemur.Position, constants.JuicerOxygenLevel)
			}
		}
	}
}
