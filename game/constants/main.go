package constants

import "math"

const (
	StickStunTime = 5

	TreeGrowthRate         = 10
	TurbineOxygenDuration  = 10
	TurbineGeneratedLemons = 10
	JuicerOxygenDuration   = 10

	TurbineOxygenLevel = 15
	JuicerOxygenLevel  = 10

	MaxTimeWithoutOxygen = 4

	WinnerScore = 50000
)

func Score(turn int) int {
	return int(1000 * math.Pow(0.99, float64(turn)))
}
