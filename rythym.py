import pygame

AUQUA = (0, 123, 173)
RED = (255, 0, 0)
NAVY = (0, 0, 128)
GREEN = (102, 255, 0)
BLACK = (0, 0, 0)

surface = pygame.display.set_mode((800, 600))
allObjectsList = pygame.sprite.Group()

def rythymGameStart():

    initializeRythymBar()

    slider = GameObject(BLACK, 10, 50, 100, 500, 2) 
    allObjectsList.add(slider)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_SPACE:
                    print("Space was pressed!")
                    result = spacePressed()
                    if (result == 0): 
                        print("display fish")
                        #kill all sprites
                        killAllGameObjects()
                        run = False         #Probably go to fish caught scene
    
        surface.fill(AUQUA)
        allObjectsList.draw(surface)
        slider.update()

        pygame.display.flip()
        pygame.display.update()

        
def initializeRythymBar():
    # GameObject(color, width, height, xpos, ypos, speed)
    outsideL = GameObject(NAVY, 300, 25, 50, 510, 0)
    outsideR = GameObject(NAVY, 300, 25, 450, 510, 0)
    target = GameObject(GREEN, 100, 25, 350, 510, 0)

    allObjectsList.add(outsideL)
    allObjectsList.add(outsideR)
    allObjectsList.add(target)

def spacePressed():
    barList = allObjectsList.sprites()
    outsideL = barList[0]
    outsideR = barList[1]
    target = barList[2]
    slider = barList[3]

    if (pygame.sprite.collide_rect(target, slider)): 
        print("Target was hit!")
        return 0
    elif (pygame.sprite.collide_rect(outsideL, slider) or pygame.sprite.collide_rect(outsideR, slider)):
        print("outside of range! Try again")
        return 1

def killAllGameObjects():
    for obj in allObjectsList:
        obj.kill()


class GameObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, speed):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 1
        self.min_x = 50
        self.max_x = 750

    def update(self):
        # move horizontally
        self.rect.x += self.speed *self.direction

        if self.rect.right >= self.max_x or self.rect.left <= self.min_x:
            self.direction *= -1 