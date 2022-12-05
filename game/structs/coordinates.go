package structs

type Coordinate struct {
	X int `json:"x"`
	Y int `json:"y"`
}

var Directions = [4][2]int{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
