package turn

import (
	"ksp.sk/proboj/73/game/constants/building"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func SettleBuilding(t *structs.Turn) {
	// First, place new tiles
	for _, change := range t.TileChanges {
		if t.Game.World.Tiles[change.Where.Y][change.Where.X].Type() != tiles.Empty {
			continue
		}

		if !change.Lemur.HasTool(structs.Pickaxe) {
			continue
		}

		if building.CanBuild(change.Lemur, change.To) {
			building.TakeItems(change.Lemur, change.To)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewTile(change.To)
		}
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To != tiles.Empty {
			continue
		}

		if !change.Lemur.HasTool(structs.Pickaxe) {
			continue
		}

		tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]
		building.GiveItems(change.Lemur, tile.Type())
		t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
	}
}
