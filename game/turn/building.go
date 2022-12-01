package turn

import (
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
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

		switch change.To {
		case tiles.Turbine:
			if change.Lemur.CountItem(inventory.Iron) < constants.TurbineCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Iron, constants.TurbineCost)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewTurbine()
		case tiles.Tree:
			if change.Lemur.CountItem(inventory.Lemon) < constants.TreeCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Lemon, constants.TreeCost)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewTree()
		case tiles.Trap:
			if change.Lemur.CountItem(inventory.Stone) < constants.TrapCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Stone, constants.TrapCost)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Trap)
		}
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To != tiles.Empty {
			continue
		}

		tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]

		if !change.Lemur.HasTool(structs.Pickaxe) {
			continue
		}

		switch tile.Type() {
		case tiles.Stone:
			change.Lemur.AddItem(inventory.Stone, 1)
		case tiles.Iron:
			change.Lemur.AddItem(inventory.Iron, 1)
		//case tiles.Tree:
		//	change.Lemur.AddItem(inventory.Lemon, constants.TreeCost)
		case tiles.Trap:
			change.Lemur.AddItem(inventory.Stone, constants.TrapCost)
		case tiles.Turbine:
			change.Lemur.AddItem(inventory.Iron, constants.TurbineCost)
		}
		t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
	}
}
