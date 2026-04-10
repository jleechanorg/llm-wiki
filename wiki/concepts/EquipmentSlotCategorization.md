---
title: "Equipment Slot Categorization"
type: concept
tags: [equipment, classification, game-ui]
sources: [equipment-display-module-tests]
last_updated: 2026-04-08
---

## Definition
System for categorizing equipment slots into logical groups for display in game UI. Each slot type maps to a display category.

## Categories
- **Head**: head, helmet, helm, crown
- **Armor**: armor, chest, body, torso
- **Boots**: feet, boots, footwear
- **Weapons**: weapon, main hand, main_hand
- **Off-Hand**: off hand, off_hand, offhand (shields, focuses)
- **Backpack**: backpack (inventory items)
- **Rings**: ring, ring1, ring 1
- **Other**: unknown or uncategorized slots

## Usage
Used by [[EquipmentDisplayModule]] to organize equipment for UI display, ensuring consistent categorization across different equipment naming conventions.

## Related Concepts
- [[InventoryManagement]]
- [[EquipmentQueryClassification]]
