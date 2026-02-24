import pygame
import time
import pygame.freetype
from pygame.sprite import Sprite
from enum   import Enum
import os
from game_screen import game_screen


Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
Water_BG_Dir = os.path.join(Assets_Dir, "WaterBG")
Music_Dir = os.path.join(Assets_Dir, "MUSIC")

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
   """ Returns surface with text written on """
   font = pygame.freetype.SysFont("Courier", font_size, bold=True)
   surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
   return surface.convert_alpha()


class UIElement(Sprite):
   """ An user interface element that can be added to a surface """


   def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
       """
       Args:
           center_position - tuple (x, y)
           text - string of text to write
           font_size - int
           bg_rgb (background colour) - tuple (r, g, b)
           text_rgb (text colour) - tuple (r, g, b)
       """
       self.mouse_over = False  # indicates if the mouse is over the element


       # create the default image
       default_image = create_surface_with_text(
           text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
       )


       # create the image that shows when mouse is over the element
       highlighted_image = create_surface_with_text(
           text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
       )


       # add both images and their rects to lists
       self.images = [default_image, highlighted_image]
       self.rects = [
           default_image.get_rect(center=center_position),
           highlighted_image.get_rect(center=center_position),
       ]


       # calls the init method of the parent sprite class
       super().__init__()


       # store optional action callable
       self.action = action


       # properties that vary the image and its rect when the mouse is over the element
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
       """ Draws element onto a surface """
       surface.blit(self.image, self.rect)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# title constant is no longer used, but kept for reference
SCREEN_TITLE = "Parallax"

SCROLL_SPEED = 200  # pixels per second


class ParallaxLayer:
    """Pygame-based parallax layer.

    The layer loads a single image and tiles it horizontally.  Copies of the
    image are tracked with ``Rect`` objects; when one moves completely off
    the left edge it is wrapped to the right of the current rightmost copy.
    """

    def __init__(self, image_path, speed_factor):
        self.speed_factor = speed_factor
        self.image = pygame.image.load(image_path).convert_alpha()
        iw, ih = self.image.get_size()

        scale = SCREEN_HEIGHT / ih
        new_w = int(iw * scale)
        self.image = pygame.transform.scale(self.image, (new_w, SCREEN_HEIGHT))

        self.width = self.image.get_width()

        # build enough rects to fill the screen plus one extra
        self.rects = []
        num_sprites = SCREEN_WIDTH // self.width + 3
        for i in range(num_sprites):
            rect = self.image.get_rect()
            rect.x = i * self.width
            rect.y = 0
            self.rects.append(rect)

    def update(self, dt):
        movement = SCROLL_SPEED * dt * self.speed_factor
        for rect in self.rects:
            rect.x -= movement

        # wrap rectangles that have moved off-screen
        for rect in self.rects:
            if rect.right < 0:
                rightmost = max(r.right for r in self.rects)
                rect.x = rightmost

    def draw(self, surface):
        for rect in self.rects:
            surface.blit(self.image, rect)


class GameState(Enum):
   QUIT = -1
   START = 1


<<<<<<< HEAD:main-menu.py
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # create parallax layers; images should tile horizontally
    layers = [
        ParallaxLayer(os.path.join(Water_BG_Dir, "1.png"), 0.2),
        ParallaxLayer(os.path.join(Water_BG_Dir, "2.png"), 0.5),
        ParallaxLayer(os.path.join(Water_BG_Dir, "3.png"), 0.8),
        ParallaxLayer(os.path.join(Water_BG_Dir, "4.png"), 1.0),
        ParallaxLayer(os.path.join(Water_BG_Dir, "5.png"), 1.2),
    ]

    # create UI elements
    def start_action():
        print("Start button pressed")
        game_screen(screen)

    start_btn = UIElement(
        center_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=start_action,
    )

    quit_btn = UIElement(
        center_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    # main loop
    buttons = [start_btn, quit_btn]

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # draw parallax background
        screen.fill((0, 0, 0))
        for layer in layers:
            layer.update(dt)
            layer.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            action = btn.update(mouse_pos, mouse_up)
            if action is not None:
                if action == GameState.QUIT:
                    pygame.quit()
                    return
                if callable(action):
                    action()
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()


####  Music playback code  ####
# 1. Initialize the mixer
pygame.mixer.init()
=======
def main(screen=None):
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

   # try to load background image (optional). If missing, we'll use solid color.
    background = None
    asset_path = os.path.join(os.path.dirname(__file__), "assets", "4-Free-Seamless-Nature-Pixel-Backgrounds4-1536x1024.png")
    if os.path.exists(asset_path):
       try:
           background = pygame.image.load(asset_path).convert_alpha()
           background = pygame.transform.scale(background, screen.get_size())
       except Exception as e:
           print(f"Failed to load background image '{asset_path}': {e}")
           background = None
    else:
       print(f"Background image not found at: {asset_path}")


   # create UI elements
    def start_action():
       print("Start button pressed")
       game_screen(screen)


    start_btn = UIElement(
       center_position=(400, 300),
       font_size=30,
       bg_rgb=BLUE,
       text_rgb=WHITE,
       text="Start",
       action=start_action,
   )


    quit_btn = UIElement(
       center_position=(400, 400),
       font_size=30,
       bg_rgb=BLUE,
       text_rgb=WHITE,
       text="Quit",
       action=GameState.QUIT,
   )


   # main loop
    buttons = [start_btn, quit_btn]


    while True:
       mouse_up = False
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
           if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
               mouse_up = True


       if background:
           screen.blit(background, (0, 0))
       else:
           screen.fill(BLUE)


       mouse_pos = pygame.mouse.get_pos()
       for btn in buttons:
           action = btn.update(mouse_pos, mouse_up)
           if action is not None:
               if action == GameState.QUIT:
                   pygame.quit()
               if callable(action):
                   action()
       for btn in buttons:
           btn.draw(screen)


       pygame.display.flip()

>>>>>>> 80a238d114a420beee64f4ba1f62cb9598bd9ad9:main_menu.py

# 2. Load the OGG file
music_file_path = os.path.join(Music_Dir, "Main-menu.ogg")
pygame.mixer.music.load(music_file_path)
# 3. Start playing the music (loop infinitely)
pygame.mixer.music.play(-1)
# 4. Optionally, set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.5)


# call main when the script is run
if __name__ == "__main__":
    main()