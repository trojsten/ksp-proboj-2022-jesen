package game

import "ksp.sk/proboj/73/libproboj"

func New(r libproboj.Runner) Game {
	g := Game{runner: r}
	return g
}

func (g *Game) Run() {

}
