'''
EECS 581 Project 1
Description: Board class that handles placing and shooting ships and checking if coordinates shot/sunk
Inputs: List of ships from Battleship class
Outputs: Boolean values
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Landon Pyko
Author: Kai Achen
Creation Date: 9-11-2024

Coord integer meanings:
    - 0 = empty, unshot
    - 1 = empty, shot
    - 2 = occupied, unhit
    - 3 = occupied, hit
    - 4 = occupied, sunk
'''
class Board:
    def __init__(self, shipList):                               # Assumes good inputs
        # Board coordinates:
        self.coordsMatrix = []                                  # Declare matrix to hold list of lists of coordinate flags
        for row in range(100):                                  # 100 rows
            tempRow = []                                        # Declare temp row for construction
            for column in range(100):                           # 100 columns
                tempRow.append(0)                               # Append empty flag
            self.coordsMatrix.append(tempRow)                   # Append row to matrix

        # Ships:
        self.shipList = shipList                                # Take in shipList from Battleship class
        self.hitList = []                                       # Indices in hitList match indices in shipList to indicate hit coords
        self.shipCount = len(shipList)                          # Number of ships on board
        for ship in range(self.shipCount):                      # For each ship in shipList
            tempList = []                                       # Reset temporary list
            for coord in ship:                                  # For each coord in ship
                tempList.append(0)                              # Append a not-hit flag to coord
            self.hitList.append(tempList)                       # Append flag list for that ship to hitList
    
    # Index, List -> Boolean
    def isSunk(self):                                           # Assumes good inputs
        for ship in self.hitList:                               # For each ship in hitList
            if ship == self.shipIndex:                          # If it's the ship queried
                for coord in ship:                              # For each coord in ship
                    if coord == 2:                              # If the coord is unhit,
                        return False                            # Return False
                    else:                                       # Else,
                        return True                             # Return True
    
    # List -> Boolean
    def allSunk(self):                                          # Assumes good inputs
        for ship in self.hitList:                               # For each ship
            if self.isSunk(ship) == False:                      # If not sunk,
                return False                                    # Return False
            else:                                               # Else,
                return True                                     # Return True

    # Tuple, Matrix -> Boolean
    def shoot(self, coordsTuple):                               # Assumes good inputs
        for row in (self.coordsMatrix):                         # For each row in coordsMatrix
            for column in row:                                  # For each column in coordsMatrix
                                                                # If correct coordinates based on coordsTuple,
                if (row == coordsTuple[0]) and (column == coordsTuple[1]):
                    if self.coordsMatrix[row][column] == 2:     # If occupied and unhit,
                        self.coordsMatrix[row][column] = 3      # Mark as occupied and hit
                        return True                             # Return True
                    elif self.coordsMatrix[row][column] == 0:   # If empty and unhit,
                        self.coordsMatrix[row][column] = 1      # Mark as empty and hit
                        return False                            # Return False
                    else:                                       # Else,
                        return False                            # Return False

    # Tuple, Matrix -> Boolean
    def wasShot(self, coordsTuple):                             # Assumes good inputs
        for row in self.coordsMatrix:                           # For each row in coordsMatrix
            for column in row:                                  # For each column in coordsMatrix
                                                                # If correct coordinates based on coordsTuple,
                if (row == coordsTuple[0]) and (column == coordsTuple[1]):
                                                                # If this coordinate has previously been shot
                    if (self.coordsMatrix[row][column] == 1) or (self.coordsMatrix[row][column] == 3) or (self.coordsMatrix[row][column] == 4):
                        return True                             # Return True
                    else:                                       # Else,
                        return False                            # Return False

    # Matrix -> Boolean
    def setBoard(self, shipList):                               # Assumes good inputs
        for ship in shipList:                                   # For each ship in shipList
                                                                # Call place ship and if unable,
            if self._placeShip(shipList[ship], self.coordsMatrix) == False:
                return False                                    # Return False
            else:                                               # Else,
                return True                                     # Return True

    # Tuple, Matrix -> Boolean
    def _placeShip(self, coordsTuple):                          # Assumes good inputs
        for row in self.coordsMatrix:                           # For each row in coordsMatrix
            for column in row:                                  # For each column in coordsMatrix
                                                                # If correct coordinates based on coordsTuple,
                if (row == coordsTuple[0]) and (column == coordsTuple[1]):
                                                                # If coordinates are empty,
                    if (self.coordsMatrix[row][column] == 0) or (self.coordsMatrix[row][column] == 1):
                        self.coordsMatrix[row][column] = 2      # Mark coords as occupied and unhit
                        return True                             # Return True for valid placement
                    else:                                       # Else,
                        return False                            # Return False for invalid placement
