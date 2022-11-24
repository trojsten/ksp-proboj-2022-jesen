package game

import "ksp.sk/proboj/73/libproboj"

func New(r libproboj.Runner) Game {
	g := Game{runner: r}

	players, _ := r.ReadConfig()

	for i, player := range players {
		g.Players = append(g.Players, Player{
			Idx:         i,
			Name:        player,
			Color:       "",
			DisplayName: "",
			Lemurs:      []Lemur{},
		})

		/*for i := 0; i < 5; i++ {
			g.Players[i].Lemurs = append(g.Players[i].Lemurs, Lemur{})
		}*/
	}

	return g
}

func (g *Game) Run() {

}
