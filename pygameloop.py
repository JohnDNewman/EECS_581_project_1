import pygame as pg
from battleship import Battleship


class PyGameLoop:
    def __init__(self,width,height,numShips):
        self._width = width
        self._height = height
        self.numShips = numShips
        self.battleship = Battleship()

        # ^ Just wrote these in the init so that they can be accessed through self in other methods (like run())

        # If you want to move it somewhere else thats fine too idc



    def setUpGame(self):
  
        pg.init() # Initialize pygame
            
        # Form screen
        screen = pg.display.set_mode((self._width,self._height))
        screen.fill((0,0,255)) # Just filling it with RGB for blue right now to make sure it shows up


    def run():
        running = True
        while running:  # Want to have some continuous loop that displays the stuff to the user
            pg.display.flip() # Displays the screen to the user
  
