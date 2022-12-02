package turn

import (
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
	"math"
)

func canReach(c1, c2 structs.Coordinate, w *structs.World) bool {
	if c1.X-c2.X >= -1 && c1.X-c2.X <= 1 && c1.Y-c2.Y >= -1 && c1.Y-c2.Y <= 1 {
		return true
	}

	avgX := float64(c1.X+c2.X) / 2
	avgY := float64(c1.Y+c2.Y) / 2

	// Only one of avgX, avgY can be decimal
	var toCheck []structs.Coordinate
	if math.Mod(avgX, 1) != 0 {
		toCheck = append(toCheck, structs.Coordinate{
			X: int(math.Ceil(avgX)),
			Y: int(avgY),
		}, structs.Coordinate{
			X: int(math.Floor(avgX)),
			Y: int(avgY),
		})
	} else if math.Mod(avgY, 1) != 0 {
		toCheck = append(toCheck, structs.Coordinate{
			X: int(avgX),
			Y: int(math.Ceil(avgY)),
		}, structs.Coordinate{
			X: int(avgX),
			Y: int(math.Floor(avgY)),
		})
	} else {
		toCheck = append(toCheck, structs.Coordinate{
			X: int(avgX),
			Y: int(avgY),
		})
	}

	for _, coordinate := range toCheck {
		if w.Tiles[coordinate.Y][coordinate.X].Type() == tiles.Empty {
			return true
		}
	}

	return false
}

func SettleCombat(t *structs.Turn) {
	for _, stab := range t.Stabs {
		t.Game.KillLemur(stab.Target)
	}

	for _, bonk := range t.Bonks {
		attacker := bonk.Attacker
		target := bonk.Target

		if !canReach(attacker.Position, target.Position, &t.Game.World) {
			continue
		}

		target.StunnedTime = constants.StickStunTime
	}
}
