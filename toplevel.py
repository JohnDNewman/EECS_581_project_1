'''
EECS 581 Project 1
Description: Top level file that is run to execute and play Battleship
Inputs: None
Outputs: None
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Kai Achen, Landon Pyko
Author: Landon Pyko
Creation Date: 9-10-2024
'''

from pygameloop import PyGameLoop   # import pygame

def main():
    game = PyGameLoop()             # Instantiate the pygame class 
    game.run()                      # Start the game

if __name__ == "__main__":          # run this file as main
    main()
