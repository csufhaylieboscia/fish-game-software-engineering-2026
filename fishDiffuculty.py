import pygame
import os
import math
import random
from pygame import mixer

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