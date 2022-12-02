package building

import (
	"ksp.sk/proboj/73/game/inventory"
	"ksp.sk/proboj/73/game/structs"
	"ksp.sk/proboj/73/game/tiles"
)

type Cost struct {
	Lemon     int
	Stone     int
	Iron      int
	Buildable bool
}

var cost = map[tiles.TileType]Cost{
	tiles.Stone:   {0, 1, 0, false},
	tiles.Iron:    {0, 0, 1, false},
	tiles.Tree:    {0, 5, 0, true},
	tiles.Wall:    {0, 2, 0, true},
	tiles.Turbine: {0, 20, 1, true},
}

func CanBuild(l *structs.Lemur, tile tiles.TileType) bool {
	cost, ok := cost[tile]
	if !ok {
		return false
	}

	return l.CountItem(inventory.Lemon) >= cost.Lemon && l.CountItem(inventory.Stone) >= cost.Stone && l.CountItem(inventory.Iron) >= cost.Lemon
}

func TakeItems(l *structs.Lemur, tile tiles.TileType) {
	cost := cost[tile]
	l.RemoveItem(inventory.Lemon, cost.Lemon)
	l.RemoveItem(inventory.Stone, cost.Stone)
	l.RemoveItem(inventory.Iron, cost.Iron)
}

func GiveItems(l *structs.Lemur, tile tiles.TileType) {
	cost := cost[tile]
	l.AddItem(inventory.Lemon, cost.Lemon)
	l.AddItem(inventory.Stone, cost.Stone)
	l.AddItem(inventory.Iron, cost.Iron)
}
