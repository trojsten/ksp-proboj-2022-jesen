package turn

func (t Turn) SettleInventories() {
	for _, extract := range t.InventoryExtracts {
		extract.Inventory.RemoveItem(extract.Slot, extract.Quantity)
	}

	for _, insert := range t.InventoryInserts {
		insert.Inventory.AddItem(insert.Slot, insert.Quantity)
	}

}
