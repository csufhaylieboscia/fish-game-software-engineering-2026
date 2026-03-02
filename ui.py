import pygame
import pygame.freetype


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):

<<<<<<< HEAD
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
=======
    def __init__(self, text_image, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """Create a new element.

        ``action`` can be any value returned by ``update`` when the element
        is clicked; typically this is a string identifying what should
        happen (``"quit"``, ``"resume"`` etc).
        """
        self.text_image = text_image

>>>>>>> c06ce31a8742c55a6e4d06deed0d13034855c77a
        self.mouse_over = False

        # create the default/hover images
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        highlighted_image = create_surface_with_text(
            text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [text_image, default_image, highlighted_image]
        self.rects = [
            text_image.get_rect(center=center_position),
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        super().__init__()
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
