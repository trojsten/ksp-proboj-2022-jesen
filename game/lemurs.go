package game

import (
	"fmt"
	"ksp.sk/proboj/73/game/constants"
	"ksp.sk/proboj/73/game/inventory"
)

type Lemur struct {
	Player      int
	Position    Coordinate
	Alive       bool
	Tools       [2]Tool
	Cocos       int
	Coal        int
	Stone       int
	Gold        int
	LanternTime int
	TimeInDark  int
}

func (l *Lemur) AddItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Cocos:
		l.Cocos += quantity
	case inventory.Gold:
		l.Gold += quantity
	case inventory.Coal:
		l.Coal += quantity
	case inventory.Stone:
		l.Stone += quantity
	}
}

func (l *Lemur) RemoveItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Cocos:
		if l.Cocos < quantity {
			l.Cocos = 0
		} else {
			l.Cocos -= quantity
		}
	case inventory.Gold:
		if l.Gold < quantity {
			l.Gold = 0
		} else {
			l.Gold -= quantity
		}
	case inventory.Coal:
		if l.Coal < quantity {
			l.Coal = 0
		} else {
			l.Coal -= quantity
		}
	case inventory.Stone:
		if l.Stone < quantity {
			l.Stone = 0
		} else {
			l.Stone -= quantity
		}
	case inventory.Tool1:
		l.Tools[0] = NoTool
	case inventory.Tool2:
		l.Tools[1] = NoTool
	}
}

func (l *Lemur) CountItem(slot inventory.InventorySlot) int {
	switch slot {
	case inventory.Cocos:
		return l.Cocos
	case inventory.Gold:
		return l.Gold
	case inventory.Coal:
		return l.Coal
	case inventory.Stone:
		return l.Stone
	case inventory.Tool1:
		if l.Tools[0] == NoTool {
			return 0
		} else {
			return 1
		}
	case inventory.Tool2:
		if l.Tools[1] == NoTool {
			return 0
		} else {
			return 1
		}
	}
	return 0
}

func (l *Lemur) CanReach(c Coordinate) bool {
	for _, d := range Directions {
		if c.X == l.Position.X+d[0] && c.Y == l.Position.Y+d[1] {
			return true
		}
	}
	return false
}

func (l *Lemur) HasTool(tool Tool) bool {
	for _, t := range l.Tools {
		if t == tool {
			return true
		}
	}
	return false
}

func (l *Lemur) AddTool(tool Tool) bool {
	for i, t := range l.Tools {
		if t == NoTool {
			l.Tools[i] = tool
			return true
		}
	}
	return false
}

func SpawnLemur(p *Player, g *Game) error {
	sp, ok := g.GetSpawnpoint(p.Idx)
	if !ok {
		return fmt.Errorf("no suitable spawnpoints for player %s", p.Name)
	}

	p.Lemurs = append(p.Lemurs, &Lemur{
		Player:   p.Idx,
		Position: sp,
		Alive:    true,
		Tools:    [2]Tool{Pickaxe, NoTool},
	})
	return nil
}

func (l *Lemur) Tick(g *Game) {
	if !l.Alive {
		return
	}

	if g.World.Light[l.Position.Y][l.Position.X] <= 0 {
		// The lemur is standing in the dark
		l.TimeInDark++
		if l.TimeInDark >= constants.MaxTimeInDark {
			l.Alive = false
		}
	} else {
		l.TimeInDark = 0
	}
}
