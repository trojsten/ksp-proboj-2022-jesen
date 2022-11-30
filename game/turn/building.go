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

		if !change.Lemur.HasTool(structs.Hammer) {
			continue
		}

		switch change.To {
		case tiles.Furnace:
			if change.Lemur.CountItem(inventory.Gold) < constants.FurnaceCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Gold, constants.FurnaceCost)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewFurnace()
		case tiles.Chest:
			if change.Lemur.CountItem(inventory.Coal) < constants.ChestCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Coal, constants.ChestCost)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewChest()
		case tiles.Tree:
			if change.Lemur.CountItem(inventory.Cocos) < constants.TreeCost {
				continue
			}
			change.Lemur.RemoveItem(inventory.Cocos, constants.TreeCost)
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
		tool := structs.Pickaxe
		if tile.Type() == tiles.Tree || tile.Type() == tiles.Furnace || tile.Type() == tiles.Trap || tile.Type() == tiles.Chest {
			tool = structs.Hammer
		}

		if !change.Lemur.HasTool(tool) {
			continue
		}

		switch tile.Type() {
		case tiles.Stone:
			change.Lemur.AddItem(inventory.Stone, 1)
		case tiles.Coal:
			change.Lemur.AddItem(inventory.Coal, 1)
		case tiles.Gold:
			change.Lemur.AddItem(inventory.Gold, 1)
		case tiles.Tree:
			change.Lemur.AddItem(inventory.Cocos, constants.TreeCost)
		case tiles.Trap:
			change.Lemur.AddItem(inventory.Stone, constants.TrapCost)
		case tiles.Chest:
			change.Lemur.AddItem(inventory.Coal, constants.ChestCost)
		case tiles.Furnace:
			change.Lemur.AddItem(inventory.Gold, constants.FurnaceCost)
		}
		t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
	}
}
