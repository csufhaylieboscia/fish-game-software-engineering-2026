import pygame
from enum import Enum
import os
from game import gameLoop
from ui import create_surface_with_text, UIElement


Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
Water_BG_Dir = os.path.join(Assets_Dir, "WaterBG")
Music_Dir = os.path.join(Assets_Dir, "MUSIC")

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def set_center(self, center_position):
       """Re-centre the UI element when the window size changes.

       This updates both the normal and highlighted rects so that the
       button stays aligned after toggling fullscreen or resizing.
       """
       self.rects = [img.get_rect(center=center_position) for img in self.images]


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# title constant is no longer used, but kept for reference
SCREEN_TITLE = "Parallax"

SCROLL_SPEED = 200  # pixels per second


class ParallaxLayer:

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

def main_menu_loop(screen, clock):
    pygame.mixer.init() # MOVED THIS - cali
    music_file_path = os.path.join(Music_Dir, "Main-menu.ogg")
    pygame.mixer.init()
    pygame.mixer.music.load(music_file_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    layers = [
        ParallaxLayer(os.path.join(Water_BG_Dir, "1.png"), 0.2),
        ParallaxLayer(os.path.join(Water_BG_Dir, "2.png"), 0.5),
        ParallaxLayer(os.path.join(Water_BG_Dir, "3.png"), 0.8),
        ParallaxLayer(os.path.join(Water_BG_Dir, "4.png"), 1.0),
        ParallaxLayer(os.path.join(Water_BG_Dir, "5.png"), 1.2),
    ]

    def start_action():
        return "game"   # CHANGED - cali

    # initial button positions; will be updated each frame based on
    # the current window size so that fullscreen keeps them centred.
    start_btn = UIElement(
        center_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action="game",
    )

    quit_btn = UIElement(
        center_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action="quit",
    )

    # main loop
    buttons = [start_btn, quit_btn]
    offsets = [0, 100]  # vertical offsets from centre for each button

    while True:
        # recalc button centres every iteration in case the window size changed
        screen_w, screen_h = screen.get_size()
        for btn, off in zip(buttons, offsets):
            btn.set_center((screen_w // 2, screen_h // 2 + off))

        dt = clock.tick(60) / 1000.0
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            # ESC toggles fullscreen/resolution
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.toggle_fullscreen()

        # draw parallax background
        screen.fill((0, 0, 0))
        for layer in layers:
            layer.update(dt)
            layer.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            action = btn.update(mouse_pos, mouse_up)
            if action == "quit":
                pygame.quit()
                return "quit"       # CHANGED - cali
            if action == "game":
                return "game"

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
