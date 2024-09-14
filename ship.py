'''
EECS 581 Project 1
Description: Ship class that holds coords and can check if shot, how many times its been hit, how long it is
Inputs: list of tuples for coords, direction for ship to face to help with display
Outputs: Boolean values, ints for numhits and get length
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Landon Pyko
Author: John Newman
Creation Date: 9-11-2024
'''

class Ship:
    def __init__(self, coords: list[tuple[int,int]], direction="none"):
        #create coords object based on size of ship
        self.coords = coords
        #create a direction var to help imaging
        self._direction = direction
        #create a private size attribute for convenience/debugging
        self._size = len(self.coords)
        #create _hitFlag and populate list based on size of ship
        self._hitFlag = []
        for _ in range(len(self.coords)):
            self._hitFlag.append(False) #append a new flag for each space the ship would take
    
    #function to check if the ship is hit at coords coordinates.
    def isHit(self, coords: tuple):
        #for the number of elements in self coords list
        for i in range(len(self.coords)):
            if coords == self.coords[i]: #check if each element is the same as the target coords
                if (self._hitFlag[i] == False): # check if coordinate has already been shot
                    self._hitFlag[i] = True #if hit, change hit flag for that ship section to True
                    return True #return bool true to indicate this ship was hit.
                else:
                    return False # if section has previously already been hit, return False
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
    
    #create function to return size of ship
    def get_length(self):
        return self._size