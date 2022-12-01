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

func lightFrom(w *structs.World, c structs.Coordinate, level int) {
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

		if w.Light[bfs.Coordinate.Y][bfs.Coordinate.X] < bfs.Level {
			w.Light[bfs.Coordinate.Y][bfs.Coordinate.X] = bfs.Level
		}

		for _, d := range structs.Directions {
			c2 := structs.Coordinate{
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

func Update(g *structs.Game) {
	w := &g.World
	furnaces := []structs.Coordinate{}

	for y := 0; y < w.Height; y++ {
		for x := 0; x < w.Width; x++ {
			w.Light[y][x] = 0
			if w.Tiles[y][x].Type() != tiles.Furnace {
				continue
			}
			c := structs.Coordinate{X: x, Y: y}
			furnace := locate.FurnaceAt(*g, c)
			if furnace.Duration > 0 {
				furnaces = append(furnaces, c)
			}
		}
	}

	for _, furnace := range furnaces {
		lightFrom(w, furnace, constants.FurnaceLightLevel)
	}

	for _, lemur := range g.Lemurs() {
		if lemur.JuicerTime > 0 {
			// Lemur has turned on juicer
			if lemur.HasTool(structs.Juicer) {
				lemur.JuicerTime--
				lightFrom(w, lemur.Position, constants.JuicerOxygenLevel)
			} else {
				lemur.JuicerTime = 0
			}
		} else {
			// Lemur does not have a turned on juicer
			if lemur.HasTool(structs.Juicer) && lemur.CountItem(inventory.Lemon) > 0 && w.Light[lemur.Position.Y][lemur.Position.X] <= 0 {
				// But he has a juicer and some lemons
				lemur.RemoveItem(inventory.Lemon, 1)
				lemur.JuicerTime = constants.JuicerOxygenDuration
				lightFrom(w, lemur.Position, constants.JuicerOxygenLevel)
			}
		}
	}
}