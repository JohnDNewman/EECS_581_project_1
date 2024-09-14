from board import Board

class Battleship:                                           #
    def __init__(self, shipList0, shipList1):        # Init class with board along with where all ships are
          self.boardZero = Board(shipList0)                 # Positions of all ships for player 1
          self.boardOne = Board(shipList1)                  # Positions of all ships for player 2
          self.turn = 0                                     # Initialize the the turn as player 1's turn
          self._curBoard = self.boardZero                   # Initialize the board for player 1's board


    def takeTurn(self, coords):                         # This function is called when a player starts their turn
        # if self.turn == 0:
        if self._curBoard.shoot(coords):                # Pass the coordinates that were shot at to Board and check if they are valid
            if self._curBoard.allSunk():                    # If so, check if that shot sunk the last ship on the board
                return self.turn                        # Returns the current player number to indicate the winner
            else:                                       # If no one won, then the shot was either a miss or hit that did not win the game
                self._switchTurn()                        # Switch the turn
                return 2                                # Returns 2 to indicate valid shot but not game over
        else:                                           # If the selection was not valid, go here
            return 3                                    # If so, return 3- which means the hit was not valid
        # elif self.turn == 1:
        #     if self.boardOne.shoot(coords) == True:    # Pass the coordinates that were shot at to Board and check if they are valid
        #         if self._checkWin() == True:            # If so, check if that shot sunk the last ship on the board
        #             return self.turn
        #         else:                                       # If no one won, then the shot was either a miss or hit that did not win the game
        #             self._switchTurn()                        # Switch the turn
        #             return 2
        #     else:                                           # If the selection was not valid, go here
        #         return 3                                    # If so, return 3- which means the hit was not valid
        # if Board.shoot(coords, self.curBoard) == True:  
        #     if self._checkWin == True:                 
        #         if self.turn == 0:                      # If so, check if its player 1's turn
        #             return 0                            # If so, return 0- meaning player 1 won
        #         else:                                   # If it is not player 1's turn, it is player 2's turn
        #             return 1                            # Return 1- meaing player 2 has won
        #     else:                                       # If no one won, then the shot was either a miss or hit that did not win the game
        #         self._switchTurn                        # Switch the turn
        #         return 2                                # Return 2- which means it was a valid hit, but no one won
        # else:                                           # If the selection was not valid, go here
        #     return 3                                    # If so, return 3- which means the hit was not valid

        
    def _switchTurn(self):                  # This function is called by the previous function to switch the players turn after a move
        if self.turn == 0:                       # Check if it is player 1's turn
            self._curBoard = self.boardOne   # If so, switch the board to player 2's board
            self.turn = 1                        # Additionally switch to player 2's turn
        else:                               # If not, then it is player 2's turn and needs to be switched to player 1
            self._curBoard = self.boardZero   # Switch board to player 1's board
            self.turn = 0                        # Switch to player 1's turn
 
          
    # def _checkWin(self):                # Function that will check if the win condition has been met
    #      if self._curBoard.allSunk():   # Call the allSunk method from board to return true (win), or false (no win)
    #         return True                 # If it returns true, return true again
    #      else:                          # Go here if allSunk returns false
    #         return False                # Return false again
    