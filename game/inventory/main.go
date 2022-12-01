package inventory

type InventorySlot int

const (
	Lemon InventorySlot = iota
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
