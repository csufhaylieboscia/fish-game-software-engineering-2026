import pygame
from main_menu import main_menu_loop
from game_screen import game_screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
            current_state = game_screen(screen)

    pygame.quit()

if __name__ == "__main__":
    main()