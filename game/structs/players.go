package structs

type Player struct {
	Idx         int      `json:"-"`
	Name        string   `json:"name"`
	Color       string   `json:"color"`
	DisplayName string   `json:"display_name"`
	Alive       bool     `json:"alive"`
	Lemurs      []*Lemur `json:"lemurs"`
}

func (p *Player) Kill(g *Game) {
	// TODO: score
	p.Alive = false
	g.Runner.KillPlayer(p.Name)
}
