package turn

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/tiles"
)

func (t *Turn) SettleBuilding() {
	// First, place new tiles
	for _, change := range t.TileChanges {
		switch change.To {
		case tiles.Furnace:
			change.Lemur.RemoveItem(inventory.Gold, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Furnace
		case tiles.Chest:
			change.Lemur.RemoveItem(inventory.Coal, 1)
			t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewChest()
		case tiles.Tree:
			change.Lemur.RemoveItem(inventory.Cocos, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Tree
		case tiles.Trap:
			change.Lemur.RemoveItem(inventory.Stone, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Trap
		}
		// TODO treba budovu postavit
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To == tiles.Empty {
			tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]
			switch tile.Type() {
			case tiles.Stone:
				change.Lemur.AddItem(inventory.Stone, 1)
				t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
			case tiles.Coal:
				change.Lemur.AddItem(inventory.Coal, 1)
				t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
			case tiles.Gold:
				change.Lemur.AddItem(inventory.Gold, 1)
				t.Game.World.Tiles[change.Where.Y][change.Where.X] = tiles.NewBasic(tiles.Empty)
			}
		}
	}
}
