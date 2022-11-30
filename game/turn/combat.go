package turn

func (t *Turn) SettleCombat() {
	for _, stab := range t.Stabs {
		t.Game.KillLemur(stab.Target)
	}
}
