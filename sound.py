'''
EECS 581 Project 2
Description: SoundManager class for storing and playing sound effects
Inputs: audio files with sfx
Outputs: Play sfx during gameplay
Author: Isabel Loney
Creation Date: 9-25-2024
Last Modified: 9-26-2024
Sources: Sound effects provided by Pixabay
'''

import pygame as pg                                    # Import pygame
import os

class SoundManager:
    def __init__(self):
        pg.mixer.init() # initialize pygame mixer
        # load sfx files
        self.hitSound = pg.mixer.Sound(os.path.join('assets', 'sfx', 'hit.mp3'))
        self.missSound = pg.mixer.Sound(os.path.join('assets', 'sfx', 'miss.mp3'))
        self.sinkSound = pg.mixer.Sound(os.path.join('assets', 'sfx', 'sink.mp3'))
        # self.music = pygame.mixer.music.load('music.mp3')

    # Input: None
    # Output: Play hit.mp3 sound effect
    def playHit(self):
        pg.mixer.Sound.play(self.hitSound)
    # Input: None
    # Output: Play miss.mp3 sound effect
    def playMiss(self):
        pg.mixer.Sound.play(self.missSound)

    # Input: None
    # Output: Play sink.mp3 sound effect
    def playSink(self):
        pg.mixer.Sound.play(self.sinkSound)
