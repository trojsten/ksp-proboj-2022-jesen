package structs

import (
	"image/png"
	"ksp.sk/proboj/73/game/tiles"
	"os"
	"path"
)

func (w *World) LoadMap(filename string) error {
	f, err := os.OpenFile(path.Join("maps", filename), os.O_RDONLY, os.ModePerm)
	if err != nil {
		return err
	}
	defer f.Close()

	im, err := png.Decode(f)
	if err != nil {
		return err
	}
	size := im.Bounds().Size()
	w.Width = size.X
	w.Height = size.Y

	w.Tiles = make([][]tiles.Tile, w.Height)
	w.Visible = make([][]bool, w.Height)
	w.Light = make([][]int, w.Height)
	for y := 0; y < w.Height; y++ {
		w.Tiles[y] = make([]tiles.Tile, w.Width)
		w.Visible[y] = make([]bool, w.Width)
		w.Light[y] = make([]int, w.Width)

		for x := 0; x < w.Width; x++ {
			color := im.At(im.Bounds().Min.X+x, im.Bounds().Min.Y+y)
			red, green, blue, _ := color.RGBA()
			red &= 255
			green &= 255
			blue &= 255

			if red == 0 && green == 0 && blue == 0 {
				// Black = stone
				w.Tiles[y][x] = tiles.NewBasic(tiles.Stone)
			} else if red == 255 && green == 255 && blue == 255 {
				// White = empty
				w.Tiles[y][x] = tiles.NewBasic(tiles.Empty)
			} else if red == 0 && green == 255 && blue == 0 {
				// Green = tree
				t := tiles.NewTree()
				t.HasLemon = true
				w.Tiles[y][x] = t
			} else if red == 0 && green == 0 && blue == 255 {
				// Blue = turbine
				t := tiles.NewTurbine()
				t.Lemon = 1
				w.Tiles[y][x] = t
			} else if red == 128 && green == 128 && blue == 128 {
				// Gray = Iron
				w.Tiles[y][x] = tiles.NewBasic(tiles.Iron)
			} else if red == 255 {
				// Red-ish = spawn point, green -> player ID
				w.Tiles[y][x] = tiles.NewBasic(tiles.Empty)

				w.Spawnpoints = append(w.Spawnpoints, Spawnpoint{
					Position: Coordinate{X: x, Y: y},
					Player:   int(green),
				})
			}
		}
	}

	return nil
}
