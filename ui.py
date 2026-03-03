import pygame
import pygame.freetype


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, center_position, text, image_path, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()
        self.mouse_over = False

        # render the text and create hover/normal images
        text_image = pygame.image.load(image_path).convert_alpha()
        bigger_image = pygame.transform.scale2x(text_image)

        self.images = [text_image, bigger_image]
        self.rects = [
            text_image.get_rect(center=center_position),
            bigger_image.get_rect(center=center_position),
        ]

        self.action = action

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
