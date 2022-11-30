package main

// https://docs.google.com/document/d/1nLr4imrEPbikm79oXAVeL_KB2VZVavPHdXckPMhw_is/edit

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
	game.Run(&g)
}
