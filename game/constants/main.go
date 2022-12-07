package constants

import "math"

const (
	BonkTime = 5

	TreeGrowthRate         = 10
	TurbineOxygenDuration  = 8
	TurbineGeneratedLemons = 10
	JuicerOxygenDuration   = 5

	TurbineOxygenLevel = 15
	JuicerOxygenLevel  = 5

	MaxTimeWithoutOxygen = 3

	WinnerScore = 50000

	MaxTurns = 500
)

func Score(turn int) int {
	return int(1000 * math.Pow(0.99, float64(turn)))
}
