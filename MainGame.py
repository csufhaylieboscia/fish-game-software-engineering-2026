import pygame
from SpriteClass import Sprite
from rythym import rythymGameStart

# Global Variables
surface = pygame.display.set_mode((1000, 600))
Auqua = (0,255,225)
DockBrown = (193, 154, 107)
Purple = (160, 32, 240)
all_sprites_list = pygame.sprite.Group()

def mainScene(surface):

    #intialize Sprite
    player = Sprite(Purple, 40, 30)
    player.rect.x = 600
    player.rect.y = 500

    all_sprites_list.add(player)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space was pressed!")
                    rythymGameStart()
                    # handle space press
            

        all_sprites_list.update()
        surface.fill(Auqua)
        pygame.draw.rect(surface, DockBrown, pygame.Rect(100, 400, 1500, 1000))
        all_sprites_list.draw(surface)
        pygame.display.flip()

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rytthym Test – ESC to quit")
    mainScene(screen)
    pygame.quit()