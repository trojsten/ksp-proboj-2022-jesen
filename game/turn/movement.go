package turn

import (
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
	"math/rand"
)

func SettleMovements(t *structs.Turn) {
	targets := map[structs.Coordinate][]*structs.Lemur{}
	for _, movement := range t.Movements {
		if t.Game.World.Tiles[movement.To.Y][movement.To.X].Type() != tiles.Empty {
			continue
		}

		targets[movement.To] = append(targets[movement.To], movement.Lemur)
	}

	rollback := map[*structs.Lemur]structs.Coordinate{}
	for coordinate, lemurs := range targets {
		luckyLemur := lemurs[0]
		if len(lemurs) > 1 {
			luckyLemur = lemurs[rand.Intn(len(lemurs))]
		}
		rollback[luckyLemur] = luckyLemur.Position
		luckyLemur.Position = coordinate
	}

	settled := false
	for !settled {
		settled = true
		for lemur, coordinate := range rollback {
			if lemur.Position == coordinate {
				continue
			}

			if t.Game.LemursAt(lemur.Position) > 1 {
				settled = false
				lemur.Position = coordinate
			}
		}
	}

	for _, teleport := range t.MirrorTeleports {
		if !teleport.Lemur.HasTool(structs.Mirror) {
			continue
		}

		sp, ok := t.Game.GetSpawnpoint(teleport.Lemur.Player)
		if !ok {
			continue
		}

		teleport.Lemur.Position = sp
	}
}
