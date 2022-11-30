package structs

type Coordinate struct {
	X int
	Y int
}

var Directions = [4][2]int{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
