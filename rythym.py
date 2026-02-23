import pygame

surface = pygame.display.set_mode((1000, 600))
Auqua = (0,255,225)


def rythymGameStart():

    slider = rythymSliderMov(30,40,30,10,60)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space was pressed!")
                    # handle space press

        surface.fill(Auqua)
        slider.update()

        pygame.display.flip()
        pygame.display.update()

        


def spacePressed():
    '''might want to add return type
        0 is success caught fish can exit this rythym game run loop on line 18
        1 is failure no fish caught so try again. Dont stop the loop'''


class rythymSliderMov (pygame.sprite.Sprite):
    def __init__(self, x, y, speed, min_x, max_x):
        super().__init__()
        self.image = pygame.Surface([x,y])
        self.image.fill((255, 0, 0))
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 1 #start moving right
        self.min_x = min_x
        self.max_x = max_x

        self.rect = self.image.get_rect()
    
    def update(self):
        # move horizontally
        self.rect.x += self.speed *self.direction

        if self.rect.right >= self.max_x or self.rect.left <= self.min_x:
            self.direction *= -1 