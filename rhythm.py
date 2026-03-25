import pygame
import os
from pygame import mixer

AUQUA = (0, 123, 173)
RED = (255, 0, 0)
NAVY = (0, 0, 128)
GREEN = (102, 255, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
Backgroun_Dir = os.path.join(Assets_Dir, "UnderWater")
caught_fish_sound = os.path.join(Assets_Dir, "MUSIC/SoundEffects/getItemLOZ.mp3")

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
allObjectsList = pygame.sprite.Group()

def rhythmGameStart():

    FPS = 60
    run_background_time = 15
    run_slider_time = 3

    run_background = 0
    run_slider = 0

    background = [pygame.image.load(os.path.join(Backgroun_Dir, "bg1.png")).convert_alpha(),
                  pygame.image.load(os.path.join(Backgroun_Dir, "bg2.png")).convert_alpha(),
                  pygame.image.load(os.path.join(Backgroun_Dir, "bg3.png")).convert_alpha(),
                  pygame.image.load(os.path.join(Backgroun_Dir, "bg4.png")).convert_alpha()]
    scaled_bg = []

    for layer in background:
        scaled_image = pygame.transform.scale(layer, (SCREEN_WIDTH, SCREEN_HEIGHT))
        scaled_bg.append(scaled_image)
    clock = pygame.time.Clock()
    bg_index = 0

    # load the centered minigame background image
    minigame_bg_path = os.path.join(Assets_Dir, "InGameBG", "minigame_bg.png")
    minigame_bg = pygame.image.load(minigame_bg_path).convert_alpha()
    # calculate coordinates to center it on screen
    bg_w, bg_h = minigame_bg.get_size()
    bg_x = SCREEN_WIDTH // 2 - bg_w // 2
    bg_y = SCREEN_HEIGHT // 2 - bg_h // 2

    initializeRhythmBar()

    slider = GameObject(BLACK, 10, 50, 100, 500, 10, sprite_path = os.path.join(Backgroun_Dir, "orangefish.png")) 
    allObjectsList.add(slider)

    #load in sound effect
    mixer.music.load(caught_fish_sound)
    mixer.music.set_volume(0.7)


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
                        #mixer.music.play()
                        print("display fish")
                        #kill all sprites
                        killAllGameObjects()
                        run = False         #Probably go to fish caught scene

        if (run_background == run_background_time):
            run_background = 0
            bg_index =runBackgroundAnimation(bg_index, scaled_bg)

        surface.blit(scaled_bg[bg_index], (0,0))
        # draw centered minigame background on top of scrolling layers
        surface.blit(minigame_bg, (bg_x, bg_y))
        allObjectsList.draw(surface)
        #slider.draw(surface)
        if (run_slider == run_slider_time):
            run_slider = 0
            slider.update()
        

        pygame.display.flip()
        pygame.display.update()

        clock.tick(60)
        run_background += 1
        run_slider += 1

        
def initializeRhythmBar():
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

def runBackgroundAnimation(bg_index, scaled_bg):
    bg_index += 1
    if bg_index >= len(scaled_bg):
        bg_index = 0
    return bg_index


class GameObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, speed, sprite_path = None):
        super().__init__()

        
        if (sprite_path == None):
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        else:
            self.image = pygame.image.load(sprite_path).convert_alpha()
            tw, th = self.image.get_size()
            ratio = tw/th
            self.image = pygame.transform.scale(self.image, (50*ratio,50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 1
        self.min_x = 50
        self.max_x = 750

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        # move horizontally
        self.rect.x += self.speed *self.direction

        if self.rect.right >= self.max_x or self.rect.left <= self.min_x:
            self.direction *= -1 

    #pygane.time.set_timer
    #custom time 