package structs

import (
	"image/png"
	"ksp.sk/proboj/73/game/tiles"
	"math/rand"
	"os"
	"path"
)

func randStoneTile() tiles.BasicTile {
	r := rand.Intn(100)
	if r < 80 {
		return tiles.NewBasic(tiles.Stone)
	}
	if r < 95 {
		return tiles.NewBasic(tiles.Coal)
	}
	return tiles.NewBasic(tiles.Gold)
}

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

			if red == 0 && green == 0 && blue == 0 {
				// Black = stone
				w.Tiles[y][x] = randStoneTile()
			} else if red == 0xffff && green == 0xffff && blue == 0xffff {
				// White = empty
				w.Tiles[y][x] = tiles.NewBasic(tiles.Empty)
			} else if red == 0 && green == 0xffff && blue == 0 {
				// Green = tree
				t := tiles.NewTree()
				t.HasCocos = true
				w.Tiles[y][x] = t
			} else if red == 0xffff {
				// Red-ish = spawn point, green -> player ID
				w.Tiles[y][x] = tiles.NewBasic(tiles.Empty)

				playerId := green / 257
				w.Spawnpoints = append(w.Spawnpoints, Spawnpoint{
					Position: Coordinate{X: x, Y: x},
					Player:   int(playerId),
				})
			}
		}
	}

	return nil
}
