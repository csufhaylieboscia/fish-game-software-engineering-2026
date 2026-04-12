import pygame
import os
import math
import random
from pygame import mixer

from rhythm import *
from fish import fishObjectList

'''
Planning:

* when first enter randomly choose what object/ fish to get
    * implement a random choice picker function

* receive difficulty from get function

* based in what we recieve send to each difficulty section
    (each difficulty might need to be a differnt function call? 
        * should include outside L R boundaries (size will be changable)
        * inside/goal boundary (size will change) (also might move around)
        * slider speed will change on difficulty

    Maybe instead of it being a differnt function call each time we create one big slider/fish game object that changes?

    * need to make the Create Slider bar more dynamic
        * have location on screen (x and y scale to fullscreen)
        * have size of bar (width and height scale to fullscreen)
    
        * change the size of bar based on difficulty
            * maybe for this I need to implement like a ratio/ scaler

    * slider bar speed
        goals:
          * dont want it to be too "choppy" need it to look smooth on screen
          * higher difficulty slider goes faster
            
    * have the goal needs to be hit x number of times before it can be caught
        * add a new progress bar that will be colored in with the progress completed 
        * if the goal is missed possibly it starts dectecting?
            * maybe for difficulty 3 and 4 
        * maybe the goal section also moves around (for higher difficulty?)

'''

def fishingStart():
    fish2catch = random.choice(fishObjectList)
    diffcultyObject = DifficultyMethod(fish2catch.getDifficulty())

    initializeRhythmBar(diffcultyObject)

class DifficultyMethod():
    def __init__(self, level):
        self.level = level

        if (self.level == 1):
            self.targetScale = 1/8
            self.sliderSpeed = 12
            self.targetSpeed = 0

            self.hitNeed = 1
            self.hitCount = 0

     
        elif (self.level == 2):
            self.targetScale = 5/80
            self.sliderSpeed = 17
            self.targetSpeed = 0

            self.hitNeed = 2
            self.hitCount = 0

        elif (self.level == 3):
            self.targetScale = 25/800
            self.sliderSpeed = 17
            self.targetSpeed = 5

            self.hitNeed = 2
            self.hitCount = 0

        elif (self.level == 4):
            self.targetScale = 15/800
            self.sliderSpeed = 20
            self.targetSpeed = 5

            self.hitNeed = 3
            self.hitCount = 0
    
    @property
    def gettargetScale(self):
        return self.targetScale
    
    @property
    def getTargetSpeed(self):
        return self.targetSpeed
    
    @property
    def getSliderSpeed(self):
        return self.sliderSpeedSpeed
    
    @property
    def getHitsNeeded(self):
        return self.hitNeed
    
    @property
    def getHitCount(self):
        return self.hitCount

def initializeRhythmBar(difObject):
    outOfBounds = GameObject(NAVY, 7/8, 25/600, 50, 510, 0)
    target   = GameObject(GREEN, difObject.getTargetScale(), 25/600, 350, 510, difObject.getTargetSpeed())
    slider = GameObject(BLACK, 1/80, 5/60, 100, 500, difObject.getSliderSpeed(), sprite_path=os.path.join(Backgroun_Dir, "orangefish.png"))

    allObjectsList.add(outOfBounds)
    allObjectsList.add(target)
    allObjectsList.add(slider)

def spacePressed():
    outOfBounds = barList[0]
    target   = barList[1]
    slider   = barList[2]

    if pygame.sprite.collide_rect(target, slider):
        print("Target was hit!")
        return 0
    elif pygame.sprite.collide_rect(outOfBounds, slider):
        print("outside of range! Try again")
        return 1

def killAllGameObjects():
    for obj in allObjectsList:
        obj.kill()

class GameObject(pygame.sprite.Sprite):
    def __init__(self, color, widthScaler, heightScaler, x, y, speed, sprite_path=None):
        super().__init__()

        self.width = widthScaler * SCREEN_WIDTH
        self.height = heightScaler * SCREEN_HEIGHT

        if sprite_path is None:
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(color)
        else:
            self.image = pygame.image.load(sprite_path).convert_alpha()
            tw, th = self.image.get_size()
            ratio = tw / th
            self.image = pygame.transform.scale(self.image, (50 * ratio, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 1
        self.min_x = 5/80 * self.width
        self.max_x = 750/800 *self.width

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.max_x or self.rect.left <= self.min_x:
            self.direction *= -1
'''
Current Workflow in Rhythm:

RhythmGameStart() called
    initialize:
        Frames per second
        background time run interval
        slider time run interval
        counters for both the slider and background

        Background image load
        loop to scale each background image adds it to new list

        set clock
        counter for background index

initalizeRythmBar() called:
    
    set an outside L R gameobject for failure
    set a target game object for wins
        
Calls: GameObject() Class
    recieves:
        color, 
        width: the length of the section
        height: even height set for all objects to make an even bar 
        x: where it is located on screen x-axis (left, right, center)
        y: where it is located on screen y-axis (upper, middle, lower)
        speed: how fast the slider moves 

    Make the block an image w/ width and height and color
    set the x and y location of where the object is
    set speed, direction
    set min and max x value (boundary where the slider will "bounce off of")

back in initalizeRythmBar():

    add the objects created to a allObjects list so that they can be drawn to screen durring run time

Back in RhythmGameStart():
    intialize slider and add to list (same as initialize rythm bar) (can probably be moved in there)

    load in sound effect for caught fish sound

    RUN MODE:
        space pressed:

SpacePressed():

    get the object list and split it out to get non hit zones, hit zones and the slider
    return 0 if target was hit
    and 1 if outside of range

back in rhythmgamestart:

    RUN MODE:
    if 0:
        play caught music, kill all game objects 
        show celbration screen

    run back ground: dont need if going to do overlay

    check slider counter updates every 3 secs. This is the current speed controller
    slider.update()

slider.update(): in gameobjects

    moves slider left or right depending on current direction -1 or 1
    and speed set at 10 right now. (if set slower can have it move everyframe at like 2)

    also changes direction if at or passes min or max x

back in rhythmgamestart:

    RUN MODE:

        call display to write to screen
        have clock tick and counters increment for background and slider
'''