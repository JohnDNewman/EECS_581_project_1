class Ship:
    def __init__(self, size: int):
        #create coords object based on size of ship
        self.coords = ["?"]
        #create _hitFlag and populate list based on size of ship
        self._hitFlag = []
        for _ in range(size):
            self._hitFlag.append(False) #append a new flag for each space the ship would take
    
    #function to check if the ship is hit at coords coordinates.
    def isHit(self, coords: tuple):
        #for the number of elements in self coords list
        for i in range(len(self.coords)):
            if coords == self.coords[i]: #check if each element is the same as the target coords
                self._hitFlag[i] = True #if hit, change hit flag for that ship section to True
                return True #return bool true to indicate this ship was hit.
        return False #if no section is hit, return false.
    
    def isSunk(self):
        sunk = True
        for section in self._hitFlag:
            if section == False:
                return False
        return sunk