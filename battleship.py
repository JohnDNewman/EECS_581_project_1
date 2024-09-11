from board import Board

class Battleship:
    def __init__(self, Board, shipList1, shipList2):
          self.boardZero = Board(shipList1)
          self.boardOne = Board(shipList2)
          self.turn = 0
          
          self.curBoard = self.boardZero


    def takeTurn(self, coords):
        if Board.shoot(self.curBoard, coords) == True:
            if self._checkWin == True:
                if self.turn == 0:
                    return 0
                else: 
                    return 1
            else: 
                if self.turn == 0:
                    self._switchTurn
                    return 2
                else:
                    self._switchTurn
                    return 2
        else:
            return 3

        
    def _switchTurn(self):
        if turn == 0:
            self.curBoard = self.boardOne
            turn = 1
        else:
            self.curBoard = self.boarZero
            turn = 0
 
          
    def _checkWin(self):
         if Board.allSunk:
            return True
         else:
            return False
    