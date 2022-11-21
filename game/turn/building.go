package turn

import "ksp.sk/proboj/73/game"

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
			continue
		}

		// TODO
		// t.Game.World.Tiles[change.Where.Y][change.Where.X]

		// TODO: AddItem material to lemur's inventory
	}
}
