package main

import (
	"fmt"
	"ksp.sk/proboj/73/game"
	"ksp.sk/proboj/73/libproboj"
	"math/rand"
	"time"
)

func main() {
	runner := libproboj.NewRunner()
	seed := time.Now().UnixMilli()
	rand.Seed(seed)
	runner.Log(fmt.Sprintf("starting with seed %d", seed))

	g := game.New(runner)
	g.Run()
}
