package game

import (
	"bufio"
	"fmt"
	"ksp.sk/proboj/73/game/actions"
	"ksp.sk/proboj/73/game/turn"
	"ksp.sk/proboj/73/libproboj"
	"strings"
)

func New(r libproboj.Runner) Game {
	g := Game{runner: r}

	players, _ := r.ReadConfig()

	for i, player := range players {
		g.Players = append(g.Players, &Player{
			Idx:         i,
			Name:        player,
			Color:       "",
			DisplayName: "",
			Alive:       true,
			Lemurs:      []*Lemur{},
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
	g.World.UpdateVisibility(g)

	turnNumber := 0
	for g.IsRunning() {
		g.Turn = turn.Turn{Game: g}

		for _, player := range g.Players {
			if !player.Alive {
				continue
			}

			// Send state to the player
			data := g.StateForPlayer(player.Idx)
			resp := g.runner.ToPlayer(player.Name, fmt.Sprintf("TURN %d", turnNumber), data)
			if resp != libproboj.Ok {
				g.runner.Log(fmt.Sprintf("Player %s refused to listen to me :cry:", player.Name))
				player.Kill(g)
				continue
			}

			// Read player's response
			resp, turnData := g.runner.ReadPlayer(player.Name)
			if resp != libproboj.Ok {
				g.runner.Log(fmt.Sprintf("Player %s was unable to provide any turn data.", player.Name))
				player.Kill(g)
				continue
			}

			// Parse the response
			turnScanner := bufio.NewScanner(strings.NewReader(turnData))
			for _, lemur := range player.Lemurs {
				ok := turnScanner.Scan()
				if !ok {
					// No more lines available
					g.runner.Log(fmt.Sprintf("Player %s ended his turn data prematurely.", player.Name))
					player.Kill(g)
					break
				}

				cmd := turnScanner.Text()
				ok = actions.ExecuteAction(g, lemur, cmd)
				if !ok {
					// Invalid command or response format
					g.runner.Log(fmt.Sprintf("Player %s did not provide a meaningful command: '%s'.", player.Name, cmd))
					player.Kill(g)
					break
				}
			}
		}

		// Settle the turn
		g.Turn.Settle()

		// TODO: Observer
		g.World.UpdateVisibility(g)
	}

	// TODO: Scores
}
