import pygame
from enum import Enum

# Add each feature/file we contribute here so main() can call them
from main_menu import main as main_menu     # shows the start/quit menu
from game_screen import game_screen     # the main overworld map

class GameState(Enum):
    QUIT       = -1
    MAIN_MENU  = 0
    PLAYING    = 1
    FISHING    = 2
    # add more as we continue building out the game (e.g. INVENTORY, CRAFTING, etc)

FULLSCREEN = False   # switch depending on whether you're testing or want to play in fullscreen

# orchestrates the different screens and game states
def main():
    pygame.init()

    # Set up the screen
    if FULLSCREEN:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Fish Game")

    # Start at the main menu
    state = GameState.MAIN_MENU

    # Main game loop: keep running until the state changes to QUIT
    while state != GameState.QUIT:

        if state == GameState.MAIN_MENU:
            # main_menu() returns PLAYING when Start is clicked, QUIT when Quit
            state = main_menu(screen)

        elif state == GameState.PLAYING:
            # game_screen() returns MAIN_MENU when ESC is pressed,
            # or FISHING when the player triggers a fishing spot
            state = game_screen(screen)

        # Add more elif blocks here as you add screens

    pygame.quit()


if __name__ == "__main__":
    main()