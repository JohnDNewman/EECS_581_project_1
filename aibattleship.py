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
    def __init__ (self, board, difficulty): #initialize battleship board 
        self.board = board
        self.difficulty = difficulty
        self.last_hit = None
        self.possible_targets = []

    # should return a list of Ship objects, which can be passed to the setup phase in run() (line ~719 pygameloop.py)
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
    
    def add_adjacent_targets(self, hit):
        row, col = hit
        # add orthogonal neighbors if they are within bounds and unhit
        if row > 0:
            self.possible_targets.append((row - 1, col))  # above
        if row < 9:
            self.possible_targets.append((row + 1, col))  # below
        if col > 0:
            self.possible_targets.append((row, col - 1))  # left
        if col < 9:
            self.possible_targets.append((row, col + 1))  # right

    def aiTurn(self, board):
        # returns coordinates based on difficulty level
        if self.difficulty == 1:
            return self.aiEasyTurn(board)
        elif self.difficulty == 2:
            return self.aiMediumTurn(board)
        elif self.difficulty == 3:
            return self.aiHardTurn(board)

    def aiEasyTurn(self, board):
        coords = (random.randint(0, 9), random.randint(0, 9))                   # creates a random coordinate tuple within bounds
        valid_spaces = [0, 2]                                                   # 0: unhit and empty, 2: unhit and occupied
        while board.coordsMatrix[coords[0]][coords[1]] not in valid_spaces:     # checks if the current coords is in an unhit space
            coords = (random.randint(0, 9), random.randint(0, 9))               # generates a new random tuple
        return coords

    # AI turns should return a coordinate tuple
    # passed player's board to aiTurn if you need to use it
    def aiMediumTurn(self, board):
        # if we have potential targets (adjacent cells to a hit), try those first
        if self.possible_targets:
            target = self.possible_targets.pop(0)
            if board.coordsMatrix[target[0]][target[1]] in [0, 2]:  # valid hit
                if board.coordsMatrix[target[0]][target[1]] == 2:  # hit ship
                    self.last_hit = target
                    self.add_adjacent_targets(target)
                return target
        # otherwise fire randomly
        target = self.aiEasyTurn(board)
        if board.coordsMatrix[target[0]][target[1]] == 2:  # hit ship
            self.last_hit = target
            self.add_adjacent_targets(target)
        return target

    def aiHardTurn(self, board):
        # target the first unhit ship part (value 2) directly
        for row in range(10):
            for col in range(10):
                if board.coordsMatrix[row][col] == 2:  # unhit ship
                    return (row, col)
