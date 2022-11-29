package turn

import (
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/game/tiles"
)

func (t *Turn) SettleMovements() {
	// TODO: Fix collisions
	for _, movement := range t.Movements {
		if t.Game.World.Tiles[movement.To.Y][movement.To.X].Type() != tiles.Empty {
			continue
		}

		movement.Lemur.Position = movement.To
	}

	for _, teleport := range t.MirrorTeleports {
		if !teleport.Lemur.HasTool(game.Mirror) {
			continue
		}

		sp, ok := t.Game.GetSpawnpoint(teleport.Lemur.Player)
		if !ok {
			continue
		}

		teleport.Lemur.Position = sp
	}
}
