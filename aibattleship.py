'''
EECS 581 Project 2
Description: 
Inputs: 
Outputs: 
Authors: Jackson Wunderlich, Dylan Sailors, Ginny Ke
Creation Date: 9-26-2024
Last Modified: 9-26-2024
Sources: 
'''

import random
class BattleshipAI:
    def __init__ (self, board): #initialize battleship board 
        self.board = board 

    def randomPlaceShip(self):
        for ship in self.board.shipList:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])  # Randomly choose orientation

                # Choose random row and column within bounds to fit the ship
                if orientation == 'horizontal':
                    row = random.randint(0, 9)
                    col = random.randint(0, 9 - ship.size)
                    ship_coordinates = [(row, col + i) for i in range(ship.size)]
                else:
                    row = random.randint(0, 9 - ship.size)
                    col = random.randint(0, 9)
                    ship_coordinates = [(row + i, col) for i in range(ship.size)]

                # Check if all ship coordinates are valid
                if all(self.board.coordsMatrix[coord[0]][coord[1]] == 0 for coord in ship_coordinates):
                    ship.coords = ship_coordinates
                    for coord in ship_coordinates:
                        self.board.coordsMatrix[coord[0]][coord[1]] = 2  # Mark as taken
                    placed = True
    def aiTurn(self):
        pass

    def aiEasyTurn(self):
        pass

    def aiMediumTurn(self):
        pass

    def aiHardTurn(self):
        pass
