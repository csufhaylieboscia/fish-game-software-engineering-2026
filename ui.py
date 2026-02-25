import pygame
import pygame.freetype


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """Return a surface containing *text* at given colour and size.

    This duplicates the helper that was previously defined inside
    ``menu.py`` so both menus and the game can share it without
    circular imports.
    """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):
    """An interactive button-like element that can be drawn to a surface.

    The element maintains two images (normal/highlighted) along with
    corresponding rects.  ``set_center`` can be used when the window size
    changes so that the element stays centred.
    """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """Create a new element.

        ``action`` can be any value returned by ``update`` when the element
        is clicked; typically this is a string identifying what should
        happen (``"quit"``, ``"resume"`` etc).
        """
        self.mouse_over = False

        # create the default/hover images
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        highlighted_image = create_surface_with_text(
            text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]
        self.rects = [
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
        """Move the element to a new centre coordinate.

        Both the normal and highlighted rects are updated so the button
        stays aligned if the window size changes.
        """
        self.rects = [img.get_rect(center=center_position) for img in self.images]
