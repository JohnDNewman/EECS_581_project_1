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

        self.isAnimating = False
        self.animationStartTime = 0
        self.animationDuration = 500 # ms

    def playHitAnimation(self, screen, position): # TODO: incorporate into main game loop
        if not self.isAnimating:
            self.isAnimating = True
            self.animationStartTime = pg.time.get_ticks()  # Start time of animation

            elapsedTime = pg.time.get_ticks() - self.animationStartTime

            screen.blit(self.hitAnimation, position)
            
            if elapsedTime > self.animationDuration:
                self.isAnimating = False



