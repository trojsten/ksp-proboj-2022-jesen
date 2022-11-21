package turn

import "ksp.sk/proboj/73/game"

func (t Turn) SettleMovements() {
	// TODO: Fix collisions
	for _, movement := range t.Movements {
		if t.Game.World.Tiles[movement.To.Y][movement.To.X].Type() != game.Empty {
			continue
		}

		movement.Lemur.Position = movement.To
	}
}
