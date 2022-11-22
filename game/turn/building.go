package turn

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/inventory"
)

func (t Turn) SettleBuilding() {
	// First, place new tiles
	for _, change := range t.TileChanges {
		if change.To == game.Empty {
			continue
		}

		// TODO
		// t.Game.World.Tiles[change.Where.Y][change.Where.X]

		// TODO: RemoveItem material from lemur's inventory
	}

	// Then, break old tiles
	for _, change := range t.TileChanges {
		if change.To == game.Empty {
			tile := t.Game.World.Tiles[change.Where.Y][change.Where.X]
			switch tile.Type() {
			case game.Stone:
				change.Lemur.AddItem(inventory.Stone, 1)
			case game.Coal:
				change.Lemur.AddItem(inventory.Coal, 1)
			case game.Gold:
				change.Lemur.AddItem(inventory.Gold, 1)
			case game.Furnace:
				change.Lemur.AddItem(inventory.Gold, 1)
			case game.Chest:
				change.Lemur.AddItem(inventory.Coal, 1)
			case game.Tree:
				change.Lemur.AddItem(inventory.Cocos, 1)
			case game.Trap:
				change.Lemur.AddItem(inventory.Stone, 1)
			}
			// TODO treba to oznacit ako Empty
			// t.Game.World.Tiles[change.Where.Y][change.Where.X] = game.Empty
		}
	}
}
