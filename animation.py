'''
EECS 581 Project 2
Description: AnimationManager class for storing and playing animations
Inputs: png files with animation images
Outputs: Play animations during gameplay
Author: Anakha Krishna
Creation Date: 9-26-2024
Last Modified: 9-29-2024
Sources: Images from clipsafari.com
'''
# all code and comments written by Anakha Krishna

import pygame as pg         # import for image scaling and displaying
import os                   # import for image upload

class AnimationManager:
    # Input: None
    # Output: AnimationManager object
    # Description: AnimationManager constructor
    def __init__(self):
        self.hitAnimation = pg.image.load(os.path.join('assets', 'animations','hit.png')).convert_alpha()           # load hit image from assets, use convert_alpha() for img transparency
        self.missAnimation = pg.image.load(os.path.join('assets', 'animations','miss.png')).convert_alpha()         # load miss image from assets
        self.sinkAnimation = pg.image.load(os.path.join('assets', 'animations','sink.png')).convert_alpha()         # load sink image from assets

        self.hitAnimation = pg.transform.scale(self.hitAnimation, (100,100))                                        # scale hit image to be 100x100 pixels
        self.missAnimation = pg.transform.scale(self.missAnimation, (100,100))                                      # scale miss image to be 100x100 pixels
        self.sinkAnimation = pg.transform.scale(self.sinkAnimation, (100,100))                                      # scale sink image to be 100x100 pixels

        self.currentCoords = (0,0)                                                                                  # initialize img coordinates
        self.animationType = None                                                                                   # initialize animation type
    
    # Input: screen, mouseCoords, animationType
    # Output: animation image on board
    # Description: places desired animation on given coordinates on the board during the attack phase of the game
    def playAnimation(self, screen, mouseCoords, animationType):
        self.currentCoords = mouseCoords                                                                            # mouse position of where user clicked
        self.animationType = animationType                                                                          # animation type ('hit','miss', 'sink'), manually entered in game loop

        position = (self.currentCoords[0] - 50, self.currentCoords[1] - 50)                                         # adjust image position to be at the center of the mouse click

        if self.animationType == 'hit':                                                                             # conditional block to display hit, miss, or sink image at the
            screen.blit(self.hitAnimation, position)                                                                # adjusted position based on animation type
        elif self.animationType == 'miss':
            screen.blit(self.missAnimation, position)
        elif self.animationType == 'sink':
            screen.blit(self.sinkAnimation, position)
        else:
            print(f"Unrecognized animation type '{self.animationType}'")                                            # "handle" any error. should not ever reach this unless the game loop is modified