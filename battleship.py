'''
EECS 581 Project 1
Description: Battleship class that stores both boards and takes turns
Inputs: List of ships from PyGameLoop class, coordinates when taking turns
Outputs: Updated board values and win checking
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Kai Achen, Landon Pyko
Author: Andrew McFerrin
Creation Date: 9-10-2024
'''
#import board as battship has two baords
from board import Board
from ship import Ship #import ship to clarify what gets passed into constructor

class Battleship:
    def __init__(self, shipList0: list[Ship], shipList1: list[Ship]):   # Init class with board along with where all ships are
          self.boardZero = Board(shipList0)                             # Positions of all ships for player 1
          self.boardOne = Board(shipList1)                              # Positions of all ships for player 2
          self.turn = 0                                                 # Initialize the the turn as player 0's turn
          self._curBoard = self.boardOne                                # Initialize the board for player 1's board as we shoot at the other players board


    def takeTurn(self, coords):                         # This function is called when a player starts their turn
        if self._curBoard.shoot(coords):                # Pass the coordinates that were shot at to Board and check if they are valid
            if self._curBoard.allSunk():                    # If so, check if that shot sunk the last ship on the board
                return self.turn                        # Returns the current player number to indicate the winner
            else:                                       # If no one won, then the shot was either a miss or hit that did not win the game
                self._switchTurn()                        # Switch the turn
                return 2                                # Returns 2 to indicate valid shot but not game over
        else:                                           # If the selection was not valid, go here
            return 3                                    # If so, return 3- which means the hit was not valid
        
    def _switchTurn(self):                  # This function is called by the previous function to switch the players turn after a move
        if self.turn == 0:                       # Check if it is player 1's turn
            self._curBoard = self.boardZero   # If so, switch the board to player 2's board
            self.turn = 1                        # Additionally switch to player 2's turn
        else:                               # If not, then it is player 2's turn and needs to be switched to player 1
            self._curBoard = self.boardOne   # Switch board to player 1's board
            self.turn = 0                        # Switch to player 1's turn
    