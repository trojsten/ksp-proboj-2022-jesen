package turn

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants/building"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

func SettleBuilding(t *structs.Turn) {
	// First, place new tiles
	for _, change := range t.TileChanges {
		if change.To == tiles.Empty {
			continue
		}

		if t.Game.World.Tiles[change.Where.Y][change.Where.X].Type() != tiles.Empty {
			t.Game.RejectSettle(fmt.Sprintf("_PLACE %v %v", change.Where, change.To), change.Lemur, "the tile is not empty.")
			continue
		}

		if !change.Lemur.HasTool(structs.Pickaxe) {
			t.Game.RejectSettle(fmt.Sprintf("_PLACE %v %v", change.Where, change.To), change.Lemur, "the lemur does not have a pickaxe.")
			continue
		}

		if building.CanBuild(change.Lemur, change.To) {
			building.TakeItems(change.Lemur, change.To)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewTile(change.To)
		} else {
			t.Game.RejectSettle(fmt.Sprintf("_PLACE %v %v", change.Where, change.To), change.Lemur, "the lemur does not have enough material.")
		}
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To != tiles.Empty {
			continue
		}

		if !change.Lemur.HasTool(structs.Pickaxe) {
			t.Game.RejectSettle(fmt.Sprintf("_BREAK %v %v", change.Where, change.To), change.Lemur, "the lemur does not have a pickaxe.")
			continue
		}

		tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]
		building.GiveItems(change.Lemur, tile.Type())
		t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
	}
}
