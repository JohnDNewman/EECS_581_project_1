'''
EECS 581 Project 1
Description: Board class that handles placing and shooting ships and checking if coordinates shot/sunk
Inputs: List of ships from Battleship class
Outputs: Boolean values
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Kai Achen, Landon Pyko
Author: Kai Achen, Aiden Patel
Creation Date: 9-11-2024

Coord integer meanings:
    - 0 = empty, unshot
    - 1 = empty, shot
    - 2 = occupied, unhit
    - 3 = occupied, hit
    - 4 = occupied, sunk
'''
from ship import Ship

class Board:
    def __init__(self, shipList):                               # Assumes good inputs
        # Board coordinates:
        self.coordsMatrix = []                                  # Declare matrix to hold list of lists of coordinate flags
        for row in range(10):                                   # 10 rows
            tempRow = []                                        # Declare temp row for construction
            for column in range(10):                            # 10 columns
                tempRow.append(0)                               # Append empty flag
            self.coordsMatrix.append(tempRow)                   # Append row to matrix

        # Ships:
        self.shipList = shipList                                # Take in shipList from Battleship class
        for ship in self.shipList:                              # Iterates through ships
            for coord in ship.coords:                           # Iterates through each coordinate of a ship
                self.coordsMatrix[coord[0]][coord[1]] = 2       # Marks each coordinate with occupied, unhit flag
    
    # List -> Boolean
    def allSunk(self):                                          # Assumes good inputs
        for ship in self.shipList:                              # For each ship
            if ship.isSunk() == False:                          # If ship is not sunk
                return False                                    # Return False since there is an unsunk ship
        return True                                             # Return True since all ships are sunk

    # Tuple, Matrix -> Boolean
    def shoot(self, coordsTuple):                               # Assumes good inputs
        for ship in self.shipList:
            if ship.isHit(coordsTuple):
                if ship.isSunk():                            #is sunk does not take in any values
                    for coord in ship.coords:                               # Iterate through sunken ship coords
                        self.coordsMatrix[coord[0]][coord[1]] = 4           # Mark as sunk
                else:
                    self.coordsMatrix[coordsTuple[0]][coordsTuple[1]] = 3   # Mark as occupied and hit
                return True
        
        if (self.coordsMatrix[coordsTuple[0]][coordsTuple[1]] == 0):    # If empty and unhit,
            self.coordsMatrix[coordsTuple[0]][coordsTuple[1]] = 1       # Mark as empty and hit
            return True                                                 # Return True, valid hit
        
        else:                                                           # Coordinate already shot
            return False                                                # Return False