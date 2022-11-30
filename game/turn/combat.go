package turn

import "ksp.sk/proboj/73/game/structs"

func SettleCombat(t *structs.Turn) {
	for _, stab := range t.Stabs {
		t.Game.KillLemur(stab.Target)
	}
}
