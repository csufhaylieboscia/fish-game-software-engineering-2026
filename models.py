import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, List, Union, Dict

@dataclass
class FishItem:
    '''Data model for a caught fish.'''
    name: str
    sprite_path: str
    rarity: int  # 1=common, 5=legendary

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'FishItem':
        return cls(**data)

class Inventory:
    '''Backend inventory: 8 slots for fish, JSON persistence (legacy).'''
    SLOT_COUNT = 8

    def __init__(self):
        self.slots: List[Optional[FishItem]] = [None] * self.SLOT_COUNT
        self.selected_slot: int = 0

    def add_fish(self, name: str, sprite_path: str, rarity: int) -> bool:
        '''Add fish to first empty slot. Returns True if added.'''
        fish = FishItem(name, sprite_path, rarity)
        for i in range(self.SLOT_COUNT):
            if self.slots[i] is None:
                self.slots[i] = fish
                self.selected_slot = i  # select newly added
                return True
        return False  # inventory full

    def get_selected(self) -> Optional[FishItem]:
        return self.slots[self.selected_slot] if 0 <= self.selected_slot < self.SLOT_COUNT else None

    def swap_selected(self, new_slot: int) -> None:
        if 0 <= new_slot < self.SLOT_COUNT:
            self.selected_slot = new_slot

    def remove_fish(self, slot_idx: int) -> Optional[FishItem]:
        if 0 <= slot_idx < self.SLOT_COUNT:
            fish = self.slots[slot_idx]
            self.slots[slot_idx] = None
            return fish
        return None

    def save(self, path: str = 'player_inventory.json') -> None:
        '''Save to JSON.'''
        data = {
            'slots': [fish.to_dict() if fish else None for fish in self.slots],
            'selected_slot': self.selected_slot
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: str = 'player_inventory.json') -> 'Inventory':
        '''Load from JSON, or new if missing.'''
        inv = cls()
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                inv.slots = [
                    FishItem.from_dict(s) if s else None for s in data.get('slots', [])
                ]
                inv.selected_slot = data.get('selected_slot', 0)
            except (json.JSONDecodeError, KeyError, TypeError):
                pass  # invalid file -> new inventory
        return inv

class FishInventory:
    '''Simplified inventory: dict of fish name -> count, JSON persistence.'''
    def __init__(self):
        self.fish_counts: Dict[str, int] = {}

    def add_fish(self, name: str, rarity: int = 1) -> bool:
        '''Increment count for fish name. Always succeeds (no slots).'''
        self.fish_counts[name] = self.fish_counts.get(name, 0) + 1
        print(f'Added {name} (rarity {rarity}) to inventory. Total: {self.fish_counts[name]}')
        return True

    def get_count(self, name: str) -> int:
        return self.fish_counts.get(name, 0)

    def get_total_fish(self) -> int:
        return sum(self.fish_counts.values())

    def save(self, path: str = 'player_fish.json') -> None:
        '''Save dict to JSON.'''
        data = {'fish_counts': self.fish_counts}
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: str = 'player_fish.json') -> 'FishInventory':
        '''Load from JSON, or new empty dict.'''
        inv = cls()
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    inv.fish_counts = data.get('fish_counts', {})
            except (json.JSONDecodeError, TypeError):
                pass  # invalid -> empty
        return inv

# Legacy test (keep)
if __name__ == '__main__':
    inv = Inventory()
    inv.add_fish('Goldfish', 'assets/Sprites/FishSprites/goldfish.png', 1)
    inv.save()
    inv2 = Inventory.load()
    print('Legacy Loaded:', [s.name if s else 'Empty' for s in inv2.slots])

    # New test
    finv = FishInventory()
    finv.add_fish('Octopus', 4)
    finv.save()
    finv2 = FishInventory.load()
    print('Simple Loaded:', finv2.fish_counts)
