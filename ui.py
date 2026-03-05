import pygame
import pygame.freetype


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, center_position, text, font_size=None, bg_rgb=None, text_rgb=None, image_path=None, action=None):
        super().__init__()
        self.mouse_over = False
        self.action = action

        # Handle both text-based and image-based buttons
        if image_path:
            # Image-based buttons
            text_image = pygame.image.load(image_path).convert_alpha()
            bigger_image = pygame.transform.scale2x(text_image)
            self.images = [text_image, bigger_image]
        else:
            # Text-based buttons
            text_surface = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
            bigger_image = pygame.transform.scale2x(text_surface)
            self.images = [text_surface, bigger_image]

        self.rects = [
            self.images[0].get_rect(center=center_position),
            self.images[1].get_rect(center=center_position),
        ]

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_center(self, center_position):
        self.rects = [img.get_rect(center=center_position) for img in self.images]
