package turn

import (
	"fmt"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
	"math/rand"
)

func SettleMovements(t *structs.Turn) {
	targets := map[structs.Coordinate][]*structs.Lemur{}
	for _, movement := range t.Movements {
		if t.Game.World.Tiles[movement.To.Y][movement.To.X].Type() != tiles.Empty {
			t.Game.RejectSettle(fmt.Sprintf("_MOVE %v -> %v", movement.From, movement.To), movement.Lemur, "the target tile is not empty.")
			continue
		}

		targets[movement.To] = append(targets[movement.To], movement.Lemur)
	}

	rollback := map[*structs.Lemur]structs.Coordinate{}
	for coordinate, lemurs := range targets {
		luckyLemur := lemurs[0]
		if len(lemurs) > 1 {
			luckyLemur = lemurs[rand.Intn(len(lemurs))]
			t.Game.Runner.Log(fmt.Sprintf("Movement conflict at %v between %d lemurs, choosing %s.", coordinate, len(lemurs), t.Game.Players[luckyLemur.Player].Name))
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
				t.Game.Runner.Log(fmt.Sprintf("Movement conflict at %v after settling. Rollbacking move of lemur %s (back to %v).", lemur.Position, t.Game.Players[lemur.Player].Name, coordinate))
			}
		}
	}
}
