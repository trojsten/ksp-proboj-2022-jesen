package turn

import "ksp.sk/proboj/73/game/structs"

func Settle(t *structs.Turn) {
	SettleCombat(t)
	SettleInventories(t)
	SettleBuilding(t)
	SettleMovements(t)
	// TODO: Settle deaths
}
