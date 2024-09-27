'''
EECS 581 Project 2
Description: AnimationManager class for storing and playing animations
Inputs: png files with animation images
Outputs: Play animations during gameplay
Author: Anakha Krishna
Creation Date: 9-26-2024
Last Modified: 9-26-2024
Sources: to be listed
'''
import pygame as pg
import os

class AnimationManager:
    def __init__(self):
        self.hitAnimation = pg.image.load(os.path.join('assets', 'animations','hit.png')).convert_alpha()
        self.missAnimation = pg.image.load(os.path.join('assets', 'animations','miss.png')).convert_alpha()
        self.sinkAnimation = pg.image.load(os.path.join('assets', 'animations','sink.png')).convert_alpha()

        self.hitAnimation = pg.transform.scale(self.hitAnimation, (100,100))
        self.missAnimation = pg.transform.scale(self.missAnimation, (100,100))
        self.sinkAnimation = pg.transform.scale(self.sinkAnimation, (100,100))

        self.currentCoords = (0,0)
        self.animationType = None
    
    def playAnimation(self, screen, mouseCoords, animationType):
        self.currentCoords = mouseCoords
        self.animationType = animationType

        position = (self.currentCoords[0] - 50, self.currentCoords[1] - 50)

        if self.animationType == 'hit':
            screen.blit(self.hitAnimation, position)
        elif self.animationType == 'miss':
            screen.blit(self.missAnimation, position)
        elif self.animationType == 'sink':
            screen.blit(self.sinkAnimation, position)
        else:
            print(f"Unrecognized animation type '{self.animationType}'")