import pygame
import os
from models import Inventory, FishItem
from typing import Optional

SLOT_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]

def handle_key_event(self, event) -> Optional[str]:
        """Handle slot select keys (1-8), return selected item name or None."""
        if event.type == pygame.KEYDOWN:
            for i, key in enumerate(SLOT_KEYS):
                if event.key == key:
                    self.selected_slot = i
                    item = self.backend.get_selected()
                    return item.name if item else None
        return None

def draw_panel(self, screen: pygame.Surface, screen_w: int, screen_h: int) -> None:
        """Draw inventory panel bottom-right."""
        px = screen_w - self.panel_width - 10
        py = screen_h - self.panel_height - 10
        
        # Panel bg (semi-transparent wood/Pixel style)
        panel_rect = pygame.Rect(px, py, self.panel_width, self.panel_height)
        bg_surf = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 120))  # dark overlay
        pygame.draw.rect(bg_surf, (60, 40, 20), bg_surf.get_rect(), 4)  # border
        screen.blit(bg_surf, panel_rect.topleft)
        
        # Slots
        for i in range(min(self.visible_slots, self.num_slots)):
            slot_x = px + 10 + i * self.slot_width
            slot_y = py + 20
            
            # Slot bg
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)
            pygame.draw.rect(screen, (40, 30, 20), slot_rect, 2)
            
            # Highlight selected
            if i == self.selected_slot:
                pygame.draw.rect(screen, (255, 255, 0), slot_rect, 3)
            
            # Fish sprite if present
            fish = self.backend.slots[i]
            if fish:
                try:
                    fish_img = pygame.image.load(fish.sprite_path).convert_alpha()
                    fish_img = pygame.transform.scale(fish_img, (self.slot_width - 4, self.slot_height - 4))
                    screen.blit(fish_img, (slot_x + 2, slot_y + 2))
                except:
                    # Fallback text
                    font = pygame.font.SysFont(None, 20)
                    text = font.render(fish.name[:3], True, (255, 255, 255))
                    screen.blit(text, (slot_x + 2, slot_y + 2))
            
            # Slot overlay img
            slot_scaled = pygame.transform.scale(self.slot_img, (self.slot_width, self.slot_height))
            screen.blit(slot_scaled, (slot_x, slot_y))

def draw_selected_item_label(self, screen: pygame.Surface, screen_w: int, screen_h: int) -> None:
        """Draw selected fish name/rarity above slots."""
        item = self.backend.get_selected()
        if item:
            font = pygame.font.SysFont(None, 24)
            label = font.render(f"{item.name} (Rarity {item.rarity})", True, (255, 255, 255))
            
            # Position above panel
            label_rect = label.get_rect(center=(screen_w - self.panel_width // 2 - 10, screen_h - self.panel_height - 30))
            pygame.draw.rect(screen, (0, 0, 0, 180), label_rect.inflate(10, 5))
            screen.blit(label, label_rect)

def save(self):
        """Proxy save."""
        self.backend.save()

# Alias for game.py compatibility
Inventory = InventoryUI

