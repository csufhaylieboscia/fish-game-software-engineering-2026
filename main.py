import pygame
from menu import main_menu_loop
from game import gameLoop

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False # toggle this to go into fullscreen

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    current_state = "menu"

    while current_state != "quit":

        if current_state == "menu":
            current_state = main_menu_loop(screen, clock)

        elif current_state == "game":
            current_state = gameLoop(screen)
            # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.quit()

if __name__ == "__main__":
    main()