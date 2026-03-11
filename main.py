import pygame
from menu import main_menu_loop
from game import gameLoop

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False # track whether we're currently in fullscreen mode


def make_screen(fullscreen: bool = False):
    """Return a display surface at either windowed or native fullscreen size."""
    if fullscreen:
        # (0,0) asks SDL for the desktop resolution
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

def toggle_fullscreen(current_flag: bool):
    """Flip the fullscreen flag and recreate the screen.

    Returns: (new_screen, new_flag)
    """
    new_flag = not current_flag
    screen = make_screen(new_flag)
    return screen, new_flag


def main():
    pygame.init()
    pygame.mixer.init()

    screen = make_screen(FULLSCREEN)
    clock = pygame.time.Clock()

    current_state = "menu"

    while current_state != "quit":

        if current_state == "menu":
            current_state = main_menu_loop(screen, clock)
            # ensure our local reference matches whatever set_mode() ended up returning
            screen = pygame.display.get_surface()

        elif current_state == "game":
            current_state = gameLoop(screen)
            screen = pygame.display.get_surface()
            # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.quit()

if __name__ == "__main__":
    main()