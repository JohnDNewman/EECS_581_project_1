class Ship:
    def __init__(self, coords: list[tuple]):
        #create coords object based on size of ship
        self.coords = coords
        #create _hitFlag and populate list based on size of ship
        self._hitFlag = []
        for _ in range(len(self.coords)):
            self._hitFlag.append(False) #append a new flag for each space the ship would take
    
    #function to check if the ship is hit at coords coordinates.
    def isHit(self, coords: tuple):
        #for the number of elements in self coords list
        for i in range(len(self.coords)):
            if coords == self.coords[i]: #check if each element is the same as the target coords
                self._hitFlag[i] = True #if hit, change hit flag for that ship section to True
                return True #return bool true to indicate this ship was hit.
        return False #if no section is hit, return false.
    
    #funtion to check if ship has been sunk
    def isSunk(self):
        sunk = True #assume it is sunk
        for section in self._hitFlag: #iterate through ships hit flags
            if section == False: #if some flag isn't true, hasnt been hit
                return False #Ship isn't sunk, return False
        return sunk #no safe section indicates ship is sunk.
    
    #helper function to determine number of times a ship has been hit
    def numHits(self):
        numhits = 0 #assume 0 hits
        for section in self._hitFlag: #check each hit flag
            if section == True: #if hit then
                numhits += 1 #add 1 to number of hits
        return numhits #once done iterating then return number of hits