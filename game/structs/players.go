package structs

type Player struct {
	Idx         int
	Name        string
	Color       string
	DisplayName string
	Alive       bool
	Lemurs      []*Lemur
}

func (p *Player) Kill(g *Game) {
	// TODO: score
	p.Alive = false
	g.Runner.KillPlayer(p.Name)
}
