package actions

import (
	"ksp.sk/proboj/73/game/structs"
	"strconv"
	"strings"
)

func ExecuteAction(game *structs.Game, lemur *structs.Lemur, command string) bool {
	// Stunned lemurs can't do anything
	if lemur.StunnedTime > 0 {
		return true
	}
	if !lemur.Alive {
		return true
	}

	parts := strings.Split(command, " ")
	commandName := parts[0]

	// Convert arguments to ints
	args := []int{}
	for i := 1; i < len(parts); i++ {
		num, err := strconv.Atoi(parts[i])
		if err != nil {
			return false
		}
		args = append(args, num)
	}

	fn := Get(commandName)
	fn(game, lemur, args)
	return true
}
