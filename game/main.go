package game

import (
	"fmt"
	"ksp.sk/proboj/73/libproboj"
	"strings"
)

func New(r libproboj.Runner) Game {
	g := Game{runner: r}

	players, _ := r.ReadConfig()

	for i, player := range players {
		g.Players = append(g.Players, Player{
			Idx:         i,
			Name:        player,
			Color:       "",
			DisplayName: "",
			Alive:       true,
			Lemurs:      []Lemur{},
		})

		/*for i := 0; i < 5; i++ {
			g.Players[i].Lemurs = append(g.Players[i].Lemurs, Lemur{})
		}*/
	}

	return g
}

func (g *Game) GreetPlayers() {
	for i, player := range g.Players {
		g.runner.ToPlayer(player.Name, "init", "HELLO")
		resp, data := g.runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			g.runner.Log(fmt.Sprintf("Player %s did not respond to HELLO.", player.Name))
			g.Players[i].Alive = false
			g.runner.KillPlayer(player.Name)
			continue
		}

		parts := strings.SplitN(data, " ", 2)
		g.Players[i].DisplayName = parts[0]
		g.Players[i].Color = parts[1]
	}
}

func (g *Game) Run() {
	g.GreetPlayers()
}
