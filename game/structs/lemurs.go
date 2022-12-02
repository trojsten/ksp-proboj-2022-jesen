package structs

import (
	"fmt"
	"ksp.sk/proboj/73/game/inventory"
)

type Lemur struct {
	Player            int
	Position          Coordinate
	Alive             bool
	Tools             [2]Tool
	Lemon             int
	Stone             int
	Iron              int
	JuicerTime        int
	TimeWithoutOxygen int
	StunnedTime       int
}

func (l *Lemur) AddItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Iron:
		l.Iron += quantity
	case inventory.Lemon:
		l.Lemon += quantity
	case inventory.Stone:
		l.Stone += quantity
	}
}

func (l *Lemur) RemoveItem(slot inventory.InventorySlot, quantity int) {
	switch slot {
	case inventory.Iron:
		if l.Iron < quantity {
			l.Iron = 0
		} else {
			l.Iron -= quantity
		}
	case inventory.Lemon:
		if l.Lemon < quantity {
			l.Lemon = 0
		} else {
			l.Lemon -= quantity
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
	case inventory.Iron:
		return l.Iron
	case inventory.Lemon:
		return l.Lemon
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

func SpawnLemur(p *Player, g *Game, hasPickaxe bool) error {
	sp, ok := g.GetSpawnpoint(p.Idx)
	if !ok {
		return fmt.Errorf("no suitable spawnpoints for player %s", p.Name)
	}

	tools := [2]Tool{NoTool, NoTool}
	if hasPickaxe {
		tools[0] = Pickaxe
	}

	p.Lemurs = append(p.Lemurs, &Lemur{
		Player:   p.Idx,
		Position: sp,
		Alive:    true,
		Tools:    tools,
	})
	return nil
}
