'''
Construct involves entering how many ships you want to place
List of lists (matrix) representing coordinates
shipList [Ship, Ship, …]
Method boolean allSunk()
Method void shoot(tuple coord)
Method void setBoard()
Method boolean _placeShip()
'''
class Board:
    def __init__(self, shipList):
        # Board coordinates:
        self.coordsMatrix = []                      # Declare matrix to hold list of lists of coordinate flags
        for x in range(100):                        # 100 rows
            tempRow = []                            # Declare temp row for construction
            for y in range(100):                    # 100 columns
                tempRow.append(0)                   # Append not-fired-at flag
            self.coordsMatrix.append(tempRow)       # Append row to matrix

        # Ships:
        self.shipList = shipList                    # Take in shipList from Battleship class
        self.hitList = []                           # Indices in hitList match indices in shipList to indicate hit coords
        self.shipCount = len(shipList)              # Number of ships on board
        for ship in range(self.shipCount):          # For each ship in shipList
            tempList = []                           # Reset temporary list
            for coord in ship:                      # For each coord in ship
                tempList.append(0)                  # Append a not-hit flag to coord
            self.hitList.append(tempList)           # Append flag list for that ship to hitList
    
    # List -> Bool
    def allSunk(self.hitList):
        for ship in self.hitList:                   # For each ship
            for coord in ship:                      # For each coord in each ship
                if coord == 0:                      # If coord has not yet been hit,
                    return False                    # Return False
        return True                                 # Otherwise return True
    
    # Tuple -> Void
    # def shoot(coord):


    # 
    # def setBoard():
        

    # 
    # def _placeShip():

