import pygame


class Inventory:
    SLOT_KEYS = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_6: 5,
        pygame.K_7: 6,
        pygame.K_8: 7,
    }

    def __init__(self, panel_path, num_slots=8, visible_slot_count=8, initial_items=None):
        self.panel_image = pygame.image.load(panel_path).convert_alpha()
        self.visible_slot_count = visible_slot_count
        self.num_slots = num_slots
        self.slots = [None] * num_slots

        if initial_items:
            for index, item in enumerate(initial_items):
                if index < num_slots:
                    self.slots[index] = item

        self.selected_slot = 0

        # Fine-tuning values
        self.highlight_width_ratio = 0.50
        self.highlight_height_ratio = 0.45

        # Adjust these by a few pixels if needed
        self.highlight_x_nudge = 22.5
        self.highlight_y_nudge = 2

    def handle_key_event(self, event):
        if event.key in self.SLOT_KEYS:
            slot = self.SLOT_KEYS[event.key]
            if slot < self.num_slots:
                self.selected_slot = slot
                return self.slots[slot]
        return None

    def selected_item(self):
        return self.slots[self.selected_slot]

    def use_selected_item(self):
        return self.selected_item()

    def get_slot_rect(self, panel_rect, slot_index):
        # Full slot cell spacing across the bar
        cell_width = self.panel_image.get_width() / self.visible_slot_count

        # Highlight size based on your tested values
        highlight_width = int(cell_width * self.highlight_width_ratio)
        highlight_height = int(panel_rect.height * self.highlight_height_ratio)

        # Center inside each slot cell, then nudge
        x = int(
            panel_rect.left
            + slot_index * cell_width
            + (cell_width - highlight_width) / 2
            + self.highlight_x_nudge
        )
        y = int(
            panel_rect.top
            + (panel_rect.height - highlight_height) / 2
            + self.highlight_y_nudge
        )

        return pygame.Rect(x, y, highlight_width, highlight_height)

    def draw_panel(self, screen, screen_w, screen_h, padding=10):
        panel_rect = self.panel_image.get_rect(
            midbottom=(screen_w // 2, screen_h - padding)
        )
        screen.blit(self.panel_image, panel_rect)

        if 0 <= self.selected_slot < self.visible_slot_count:
            highlight_rect = self.get_slot_rect(panel_rect, self.selected_slot)
            pygame.draw.rect(screen, (255, 255, 255), highlight_rect, 3)

        # Debug all slot boxes
        # for i in range(self.visible_slot_count):
        #     pygame.draw.rect(screen, (255, 0, 0), self.get_slot_rect(panel_rect, i), 1)

    def draw_selected_item_label(self, screen, screen_w, screen_h, padding=12):
        label_font = pygame.font.SysFont("Arial", 18, bold=True)
        item_name = self.selected_item() or "Empty"
        label_text = f"Selected slot {self.selected_slot + 1}: {item_name}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_rect = label_surface.get_rect(
            midbottom=(
                screen_w // 2,
                screen_h - self.panel_image.get_height() - padding - 10
            )
        )
        screen.blit(label_surface, label_rect)