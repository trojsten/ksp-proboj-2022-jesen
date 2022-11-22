package turn

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/inventory"
)

func (t Turn) SettleBuilding() {
	// First, place new tiles
	for _, change := range t.TileChanges {
		switch change.To {
		case game.Furnace:
			change.Lemur.RemoveItem(inventory.Gold, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Furnace
		case game.Chest:
			change.Lemur.RemoveItem(inventory.Coal, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Chest
		case game.Tree:
			change.Lemur.RemoveItem(inventory.Cocos, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Tree
		case game.Trap:
			change.Lemur.RemoveItem(inventory.Stone, 1)
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Trap
		}
		// TODO treba budovu postavit
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To == game.Empty {
			tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]
			switch tile.Type() {
			case game.Stone:
				change.Lemur.AddItem(inventory.Stone, 1)
				// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Empty
			case game.Coal:
				change.Lemur.AddItem(inventory.Coal, 1)
				// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Empty
			case game.Gold:
				change.Lemur.AddItem(inventory.Gold, 1)
				// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Empty
			}
			// TODO treba to oznacit ako Empty
		}
	}
}
