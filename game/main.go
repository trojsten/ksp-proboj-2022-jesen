package game

import (
	"bufio"
	"encoding/json"
	"fmt"
	"ksp.sk/proboj/73/game/actions"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/globals"
	"ksp.sk/proboj/73/game/oxygen"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/turn"
	"ksp.sk/proboj/73/libproboj"
	"strconv"
	"strings"
	"time"
)

func New(r libproboj.Runner) structs.Game {
	g := structs.Game{Runner: r}
	g.Scores = map[string]int{}

	players, config := r.ReadConfig()
	configParts := strings.SplitN(config, " ", 2)
	lemursPerPlayer, err := strconv.Atoi(configParts[1])
	if err != nil {
		panic(err)
	}

	err = g.World.LoadMap(configParts[0])
	if err != nil {
		panic(err)
	}

	for i, player := range players {
		p := &structs.Player{
			Idx:         i,
			Name:        player,
			Color:       "",
			DisplayName: "",
			Alive:       true,
			Lemurs:      []*structs.Lemur{},
		}
		g.Players = append(g.Players, p)
		g.Scores[p.Name] = 0

		for li := 0; li < lemursPerPlayer; li++ {
			err = structs.SpawnLemur(p, &g, li == 0)
			if err != nil {
				break
			}
		}
	}

	return g
}

func GreetPlayers(g *structs.Game) {
	for i, player := range g.Players {
		g.Runner.ToPlayer(player.Name, "init", "HELLO")
		resp, data := g.Runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			g.Runner.Log(fmt.Sprintf("Player %s did not respond to HELLO. Runner response: %v", player.Name, resp))
			g.Players[i].Alive = false
			g.Runner.KillPlayer(player.Name)
			continue
		}

		parts := strings.SplitN(data, " ", 2)
		g.Players[i].DisplayName = parts[0]
		g.Players[i].Color = parts[1]
	}
}

func Run(g *structs.Game) {
	GreetPlayers(g)
	g.World.UpdateVisibility(g)
	g.World.Tick()
	oxygen.Update(g)

	for g.IsRunning() {
		g.Runner.Log(fmt.Sprintf("TURN %d", globals.TurnNumber))
		g.Turn = structs.Turn{Game: g}

		for _, player := range g.Players {
			if !player.Alive {
				continue
			}

			start := time.Now()
			// Send state to the player
			data := StateForPlayer(g, player.Idx)
			resp := g.Runner.ToPlayer(player.Name, fmt.Sprintf("TURN %d", globals.TurnNumber), data)
			if resp != libproboj.Ok {
				g.Runner.Log(fmt.Sprintf("Player %s refused to listen to me :cry: Runner response: %v", player.Name, resp))
				player.Kill(g)
				continue
			}

			// Read player's response
			resp, turnData := g.Runner.ReadPlayer(player.Name)
			if resp != libproboj.Ok {
				g.Runner.Log(fmt.Sprintf("Player %s was unable to provide any turn data. Runner response: %v", player.Name, resp))
				player.Kill(g)
				continue
			}
			duration := time.Now().Sub(start)
			g.Runner.Log(fmt.Sprintf("Player %s's turn took %d ms.", player.Name, duration.Milliseconds()))

			// Parse the response
			turnScanner := bufio.NewScanner(strings.NewReader(turnData))
			for _, lemur := range player.Lemurs {
				ok := turnScanner.Scan()
				if !ok {
					// No more lines available
					g.Runner.Log(fmt.Sprintf("Player %s ended his turn data prematurely.", player.Name))
					player.Kill(g)
					break
				}

				cmd := turnScanner.Text()
				ok = actions.ExecuteAction(g, lemur, cmd)
				if !ok {
					// Invalid command or response format
					g.Runner.Log(fmt.Sprintf("Player %s did not provide a meaningful command: '%s'.", player.Name, cmd))
					player.Kill(g)
					break
				}
			}
		}

		// Settle the turn
		turn.Settle(&g.Turn)

		g.World.UpdateVisibility(g)
		oxygen.Update(g)
		g.World.Tick()
		for _, lemur := range g.Lemurs() {
			g.TickLemur(lemur)
		}

		alive := 0
		var lastPlayer *structs.Player
		for _, player := range g.Players {
			if !player.Alive {
				continue
			}
			alive++
			lastPlayer = player
			g.Scores[player.Name] += constants.Score(globals.TurnNumber)
		}

		if alive == 1 {
			g.Scores[lastPlayer.Name] = constants.WinnerScore
		}

		data, err := json.Marshal(g)
		if err != nil {
			panic(err)
		}
		g.Runner.ToObserver(string(data))
		globals.TurnNumber++
	}

	g.Runner.Scores(g.Scores)
	g.Runner.End()
}
