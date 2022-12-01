package inventory

type InventorySlot int

const (
	Cocos InventorySlot = iota
	Lemon
	Stone
	Gold
	Tool1
	Tool2
)

type Inventory interface {
	AddItem(slot InventorySlot, quantity int)
	RemoveItem(slot InventorySlot, quantity int)
	CountItem(slot InventorySlot) int
}
