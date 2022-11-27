package actions

import (
	"ksp.sk/proboj/73/game"
	"strconv"
	"strings"
)

func ExecuteAction(game *game.Game, lemur *game.Lemur, command string) bool {
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
