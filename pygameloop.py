'''
EECS 581 Project 1
Description: PyGameLoop class that stores all the logic for visualizing and running the Battleship game
Inputs: User input through mouse clicks and key presses
Outputs: Visualized game
Team Members: Aiden Patel, Andrew McFerrin, John Newman, Kai Achen, Landon Pyko
Author: Aiden Patel, Landon Pyko, John Newman
Creation Date: 9-10-2024
'''

import pygame as pg                                    # Import pygame
import os                                              # Import os to access images in file system
#Importing classes we made
from battleship import Battleship                      # Import Battleship to create battleship
from ship import Ship                                  # Import Ship to clarify fuction inputs
from sound import SoundManager                         # Import SoundManager to play sfx
from animation import AnimationManager                 # Import AnimationManager to use animations
import sys
from aibattleship import BattleshipAI

#starts the window in the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Image helper class to make displaying easier
class Image:
    def __init__(self, picture,x,y):                   # Create image with picture and top left x,y coordinates
        self.picture = picture
        self.x = x
        self.y = y

#Define class of Pygameloop in which the game runs
class PyGameLoop:
    def __init__(self):
        '''
        Each board is 1004x1004 and displayed side by side
        100x100 pixels for each box with a 2 pixel outside border
        50 pixel gap between the boards when displayed
        100 pixel gap on the left and top to show labels
        Left board is where PlayerZero (Red) places ships
        Right board is where PlayerOne (Green) places ships
        '''
        self._scale = 2                                                     # Create a scale value to shrink window as most monitors aren't 2158 pixels wide or 1104 pixels tall.
        singleBoardWidth  = 1004                                            # Width of game board from image in pixels
        self._width       = 2 * singleBoardWidth + 50 + 100                 # Total width of screen given boards width and extra pixels for spacing
        self._height      = 1004 + 100                                      # Total Height of screen given boards height and extra pixels for spacing.
        self._offset      = 4 / self._scale                                 # Offset of the top left corner of the board to the top left corner of the first square (4,4) pixels really but simpler to store 4, scaled

        self._battleship  = Battleship([Ship([(0,0)])],[Ship([(0,0)])])     # Initialize the battleship with dummy ships so the attribute exists to be edited later. Convenience
        self._screen      = pg.display.set_mode()                           # initializes the window as default values to be edited later.
        self._display_info = pg.display.Info()                              # Info about the Display, used for debugging in editor
        self._margin = 200 / self._scale                                    # Margin of 200 pixels to use for diaplying text and etc, scaled

        self._screen      = pg.display.set_mode(((self._width+self._margin)/self._scale, (self._height+self._margin)/self._scale))     # initializes the window to actual values

        self._soundManager = SoundManager()                                 # initialize Sound Manager for sfx
        self._animationManager = AnimationManager()                         # initialize AnimationManager for animations

        self._battleshipAI = None                                           # initialize dummy battleship AI variable
        self._usingAI = False                                               # initializes indicator for playing against AI

    def _main_menu(self):
        #Displays a main menu that allows the player to choose between 2 players or AI.
        pg.init()
        font = pg.font.Font(None, 48)
        screen = pg.display.set_mode((800, 600))
        #clock = pg.time.Clock()

        '''code that structures the main menu screen to be the same size as the game screen'''
        menu_width = (self._width +self._margin)/self._scale
        menu_height = (self._height +self._margin) / self._scale
        screen = pg.display.set_mode((int(menu_width), int(menu_height)))
        
        #prints the options
        options = ["2 Players", "Play against AI (Easy)", "Play against AI (Medium)", "Play against AI (Hard)"]
        selected_option = 0 
    
        while True:
            screen.fill((0, 0, 0)) #blank background

            # Render the menu options
            for i, option in enumerate(options):
                if i == selected_option:
                    label = font.render(option, True, (255, 0, 0))  # Highlight the selected option
                else:
                    label = font.render(option, True, (255, 255, 255))  # Normal options

                screen.blit(label, (200, 255 + i * 60)) 
                #displays menu
            pg.display.flip()

            # Handle user input
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:  # Move selection up
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pg.K_DOWN:  # Move selection down
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pg.K_RETURN:  # Confirm selection
                        '''
                        0: two players
                        1: easy AI
                        2: medium AI
                        3: hard AI
                        '''
                        return selected_option      # returns option based on menu selection

           # clock.tick(30)

    #Function to check that ship placement doesn't go off board using coords
    def check_ship_v_map(self, direction, ship_length, coords):
        if direction == "right":                # If going right
            if coords[0] + (ship_length-1) > 9: # If coords + number of sections in the ship minus the square it used goes off the board
                return False                    # Return false
        elif direction == "left":
            if coords[0] - (ship_length-1) < 0: # If coords - number of sections in the ship minus the square it used goes off the board
                return False                    # Return false
        elif direction == "up":
            if coords[1] - (ship_length-1) < 0: # If coords - number of sections in the ship minus the square it used goes off the board
                return False                    # Return false
        elif direction == "down":
            if coords[1] + (ship_length-1) > 9: # If coords + number of sections in the ship minus the square it used goes off the board
                return False                    # Return false
        return True                             # If nothing is wrong, return True

    # Function to check if ship intersects ship
    def check_ship_v_ship(self, direction, ship_length, coords, other_ships: list[Ship]):
        if direction == "right":                            # Checking whatever direction chosen
            for ship in other_ships:                        # For all ships placed already
                for i in range(ship_length):                # Iterating through every potential spot of the current ship
                    if ship.in_ship((coords[0]+i,coords[1])): # If the current spot would hit one of the other ships
                        return False                        # Return false as ships intersect
        ## Identical for other directions ##
        elif direction == "left":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.in_ship((coords[0]-i,coords[1])):
                        return False
        elif direction == "down":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.in_ship((coords[0],coords[1]+i)):
                        return False
        elif direction == "up":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.in_ship((coords[0],coords[1]-i)):
                        return False
        return True                                         # If no ship collision, return True as its fine

    def _coordsToPix(self, boardNum, coords):               # Takes in 0 or 1 (0 is left board, 1 is right board) to indicate board to draw on and takes coords to returns pixels on given board
        match coords[1]:
            case 0:
                y = 102/self._scale
            case 1:
                y = 202/self._scale
            case 2:
                y = 302/self._scale
            case 3:
                y = 402/self._scale
            case 4:
                y = 502/self._scale
            case 5:
                y = 602/self._scale
            case 6:
                y = 702/self._scale
            case 7:
                y = 802/self._scale
            case 8:
                y = 902/self._scale
            case 9:
                y = 1002/self._scale

        match coords[0]:
            case 0:
                x = 102/self._scale
            case 1:
                x = 202/self._scale
            case 2:
                x = 302/self._scale
            case 3:
                x = 402/self._scale
            case 4:
                x = 502/self._scale
            case 5:
                x = 602/self._scale
            case 6:
                x = 702/self._scale
            case 7:
                x = 802/self._scale
            case 8:
                x = 902/self._scale
            case 9:
                x = 1002/self._scale

        return ((x + ((boardNum * 1054)/self._scale), y))   # If boardNum is 0, it's left board and won't shift, if 1, it'll add on the constant x value of the left board to shift
    
    
    def _pixToCoords(self, pix :tuple, board):              # takes in pixels and returns coordinate values depending on coord number
        x, y = -1, -1                                       # initializes as -1 in case no coordinates are matched
        
        if (pix[1] < 202/self._scale):                      # Y is self explanitory, If the y value is less than on of the options, then its in that square
            y = 0
        elif (pix[1] < 302/self._scale):
            y = 1
        elif (pix[1] < 402/self._scale):
            y = 2
        elif (pix[1] < 502/self._scale):
            y = 3
        elif (pix[1] < 602/self._scale):
            y = 4
        elif (pix[1] < 702/self._scale):
            y = 5
        elif (pix[1] < 802/self._scale):
            y = 6
        elif (pix[1] < 902/self._scale):
            y = 7
        elif (pix[1] < 1002/self._scale):
            y = 8
        elif (pix[1] < 1104/self._scale):
            y = 9

        if board == 0:                                      # X takes board value to determine if should be checking left or right board (0 is means player 0 which means target right board. 1 is opposite)
            if (pix[0] < (202+(1054))/self._scale):
                x = 0
            elif (pix[0] < (302+(1054))/self._scale):
                x = 1
            elif (pix[0] < (402+(1054))/self._scale):
                x = 2
            elif (pix[0] < (502+(1054))/self._scale):
                x = 3
            elif (pix[0] < (602+(1054))/self._scale):
                x = 4
            elif (pix[0] < (702+(1054))/self._scale):
                x = 5
            elif (pix[0] < (802+(1054))/self._scale):
                x = 6
            elif (pix[0] < (902+(1054))/self._scale):
                x = 7
            elif (pix[0] < (1002+(1054))/self._scale):
                x = 8
            elif (pix[0] < (1104+(1054))/self._scale):
                x = 9
        else:
            if (pix[0] < (202)/self._scale):
                x = 0
            elif (pix[0] < (302)/self._scale):
                x = 1
            elif (pix[0] < (402)/self._scale):
                x = 2
            elif (pix[0] < (502)/self._scale):
                x = 3
            elif (pix[0] < (602)/self._scale):
                x = 4
            elif (pix[0] < (702)/self._scale):
                x = 5
            elif (pix[0] < (802)/self._scale):
                x = 6
            elif (pix[0] < (902)/self._scale):
                x = 7
            elif (pix[0] < (1002)/self._scale):
                x = 8
            elif (pix[0] < (1104)/self._scale):
                x = 9

        return ((x, y))                                     # Return the given value
    

    def _drawShips(self):                                      # Draws ships on board. Internal logic determines if player 0 or player 1s board is drawn
        single_square_x = (100)/self._scale #helper values
        single_square_y = (100)/self._scale

        shipImgs = [[pg.image.load(os.path.join('assets', 'RedShip1.png')),     # loads all ship images
                     pg.image.load(os.path.join('assets', 'RedShip2.png')),
                     pg.image.load(os.path.join('assets', 'RedShip3.png')),
                     pg.image.load(os.path.join('assets', 'RedShip4.png')),
                     pg.image.load(os.path.join('assets', 'RedShip5.png'))],

                    [pg.image.load(os.path.join('assets', 'GreenShip1.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip2.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip3.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip4.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip5.png'))]]
        
        if self._battleship.turn == 0:                          # If player 0 turn
            shipList = self._battleship.boardZero.shipList      # Get ship list from player 0
        else:                                                   # Since only two options, if not player 0, player 1
            shipList = self._battleship.boardOne.shipList       # Get ship list from player 1

        for ship in shipList:                                                                                               # For ship in shipList from player
            cur_ship_image = shipImgs[self._battleship.turn][ship.get_length()-1]                                           # Get image for ship based on the fact player 0s are in 0 index and same for player 1,
                                                                                                                            # and ships ordered by length, so ship of length 5 is in index 4
            if ship.get_direction() == "right":                                                                             # Based on direction of ship
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))   # Scale ship image to fit the sections, 100 wide, shiplength * 100 long Divided by scaling value
                cur_ship_image = pg.transform.rotate(cur_ship_image,90)                                                     # Rotate ship image to fit direction
                self._screen.blit(cur_ship_image, self._coordsToPix(self._battleship.turn, ship.coords[0]))                 # Place ship at the expected place using conversion function of coords to pix
            elif ship.get_direction() == "left":                                                                            # Same as above
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))   # Same as above
                cur_ship_image = pg.transform.rotate(cur_ship_image,90)                                                     # Same as above
                place_at_temp = self._coordsToPix(self._battleship.turn, ship.coords[0])                                    # Image always works from top left so left needs to be translated left by ship length
                place_at_x = place_at_temp[0] - (ship.get_length() * single_square_x)+single_square_x                       # Rest is just calculating that spot, feel free to make it smoother
                place_at_y = place_at_temp[1]
                place_at = tuple((place_at_x, place_at_y))
                self._screen.blit(cur_ship_image, place_at)
            elif ship.get_direction() == "down":                                                                            # Like the right placement to the left placement
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))   # scale image
                self._screen.blit(cur_ship_image, self._coordsToPix(self._battleship.turn, ship.coords[0]))                 # No need to rotate as ships are vertically oriented in images
            elif ship.get_direction() == "up":                                                                              # Like left, must by modified by ship length up, again, feel free to make it smoother
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))
                place_at_temp = self._coordsToPix(self._battleship.turn, ship.coords[0])
                place_at_y = place_at_temp[1] - (ship.get_length() * single_square_y)+single_square_y
                place_at_x = place_at_temp[0]
                place_at = tuple((place_at_x, place_at_y))
                self._screen.blit(cur_ship_image, place_at)


    def _drawShots(self):                                                                   # draws all the shots taken in the game on the correct side
        missedShot = pg.image.load(os.path.join('assets', 'MissedShot.png'))                # Load image for missed shots
        missedShot = pg.transform.scale(missedShot,(100/self._scale,100/self._scale))       # Scale image
        hitShot    = pg.image.load(os.path.join('assets', 'HitShot.png'))                   # Load image for hit shots
        hitShot    = pg.transform.scale(hitShot,(100/self._scale,100/self._scale))          # Scale image
        sunkShot   = pg.image.load(os.path.join('assets', 'SunkShot.png'))                  # Load image for sunk shots, when ship is sunk
        sunkShot   = pg.transform.scale(sunkShot,(100/self._scale,100/self._scale))         # Scale image

        if (self._battleship.turn == 0):                                                    # runs if current turn is PlayerZero
            for i in range(len(self._battleship.boardZero.coordsMatrix)):                   # iterates through current player's board rows
                for j in range(len(self._battleship.boardZero.coordsMatrix[i])):            # iterates through current player's board columns
                    match self._battleship.boardZero.coordsMatrix[i][j]:                    # checks if the current position has been shot in some way
                        case 1:                                                             # matches a missed shot value 
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))     # draws missed shot
                        case 3:                                                             # matches a hit shot value 
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))        # draws hit shot
                        case 4:                                                             # matches a sunk shot value 
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))       # draws sunk shot

            for i in range(len(self._battleship.boardOne.coordsMatrix)):                    # iterates through opponent's board rows
                for j in range(len(self._battleship.boardOne.coordsMatrix[i])):             # iterates through opponent's board columns
                    match self._battleship.boardOne.coordsMatrix[i][j]:                     # checks if the current position has been shot in some way
                        case 1:                                                             # matches a missed shot value 
                            self._screen.blit(missedShot, self._coordsToPix(1, (i, j)))     # draws missed shot
                        case 3:                                                             # matches a hit shot value 
                            self._screen.blit(hitShot, self._coordsToPix(1, (i, j)))        # draws hit shot
                        case 4:                                                             # matches a sunk shot value 
                            self._screen.blit(sunkShot, self._coordsToPix(1, (i, j)))       # draws sunk shot

        else:                                                                               # runs if current turn is PlayerOne (otherwise identical to above)
            for i in range(len(self._battleship.boardOne.coordsMatrix)):                    # iterates through current player's board rows
                for j in range(len(self._battleship.boardOne.coordsMatrix[i])):             # iterates through current player's board columns
                    match self._battleship.boardOne.coordsMatrix[i][j]:                     # checks if the current position has been shot in some way
                        case 1:                                                             # matches a missed shot value 
                            self._screen.blit(missedShot, self._coordsToPix(1, (i, j)))     # draws missed shot
                        case 3:                                                             # matches a hit shot value 
                            self._screen.blit(hitShot, self._coordsToPix(1, (i, j)))        # draws hit shot
                        case 4:                                                             # matches a sunk shot value 
                            self._screen.blit(sunkShot, self._coordsToPix(1, (i, j)))       # draws sunk shot

            for i in range(len(self._battleship.boardZero.coordsMatrix)):                   # iterates through opponent's board rows
                for j in range(len(self._battleship.boardZero.coordsMatrix[i])):            # iterates through opponent's board columns
                    match self._battleship.boardZero.coordsMatrix[i][j]:                    # checks if the current position has been shot in some way
                        case 1:                                                             # matches a missed shot value 
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))     # draws missed shot
                        case 3:                                                             # matches a hit shot value 
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))        # draws hit shot
                        case 4:                                                             # matches a sunk shot value 
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))       # draws sunk shot

    def _placeShips(self, turn, num_ships):
        background    = pg.image.load(os.path.join('assets', 'LabeledBackground.png'))                      # Load background image
        background    = pg.transform.scale(background, (self._width/self._scale, self._height/self._scale)) # Scale background image
        shipImgs = [[pg.image.load(os.path.join('assets', 'RedShip1.png')),     # loads all ship images (Probably could have made this an attribute given the number of accesses) 
                     pg.image.load(os.path.join('assets', 'RedShip2.png')),
                     pg.image.load(os.path.join('assets', 'RedShip3.png')),
                     pg.image.load(os.path.join('assets', 'RedShip4.png')),
                     pg.image.load(os.path.join('assets', 'RedShip5.png'))],

                    [pg.image.load(os.path.join('assets', 'GreenShip1.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip2.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip3.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip4.png')),
                     pg.image.load(os.path.join('assets', 'GreenShip5.png'))]]
        
        ## CREATING TEXT FOR IN GAME EVENTS
        font = pg.font.Font(None, 36)                                                       #set font size to 36 px arbitrarily
        text_surface = font.render("What Direction will the ship extend?", True, (0,0,0))   #remind players to choose a direction for ship to go
        place_err_map = font.render("Ship off map", True, (0,0,0))                          #Tell player that direction would make the ship go off the map
        place_err_flag = False                                                              # a flag to use to display the ship place error.

        place_err_ship = font.render("Ship would intersect Ship", True, (0,0,0))            #Tell player that direction would make the ship go off the map
        place_err_ship_flag = False                                                         #A flag to use to display the ship place error.

        placed = font.render("All Ships Have been Placed!", True, (0,0,0))                  #Indicate ships have been placed

        coords = [0,0]                                                                      #"coordinates" of the cursor. 0,0 to 9,9 to ease in making ships
        single_square_x = (100)/self._scale                                                 # Helper values
        single_square_y = (100)/self._scale                                                 # Helper values

        if turn == 0:                                                                       # If player 0 is placing, max placement is edge of left board
            max_x = (1004)/self._scale                                                      # edge of left board div by scale
        elif turn == 1:                                                                     # If player 1 is placing, max placement is edge of right board
            max_x = (2058)/self._scale                                                      # edge of right board div by scale
        
        max_y = (self._height-100)/self._scale                                              # Max_y is consitent between baords. height of board - 100 for border divided by scale

        min_x = ((100 + (turn*1054))/self._scale)                                           # Min x is 100 for border + either 0 for player zero and left baord or 1054 for player 1 and right board all divided by scale
        min_y = 100/self._scale                                                             # min y is consiteint between players. 100 for border div by scale

        allPlaced = False                                                                   # used to exit the loop once true
        placePrompt = False                                                                 # flag for when player is placing a ship
        shipList = []                                                                       # list to hold created ships to pass into battleship constructor
        placed_ship_objects = []                                                            # Used to draw ships while battleship constructor doesn't exist yet

        def_x = min_x + self._offset                                                        # Helper value to create cursor starting point for readability
        def_y = (100/self._scale)+self._offset                                              # Helper value to create cursor starting point for readability
        
        cursor = pg.Rect((def_x,def_y), (single_square_x-self._offset,single_square_y-self._offset)) #create cursor indicating chosen spot, where defx and defy are top left coords and the other values is the size
        

        while not allPlaced:                                                                # While ships have yet to be placed
                                                            ### DISPLAY STUFF ###
            self._screen.fill("white")                                                      # set background color
            self._screen.blit(background, (0, 0))                                           # Display the boards
            pg.draw.rect(self._screen, 'red', cursor)                                       # Create cursor image

            for image in placed_ship_objects:                                               # for ship in placed ships, draw the image of the ship (used as drawships can't be called without battleship constructor)
                self._screen.blit(image.picture, (image.x,image.y))                         # drawing the ship
            
                                                        ## DRAWING TEXT PROMPTS FOR USER ##
            if placePrompt:                                                                 # to place ship
                self._screen.blit(text_surface, ((self._width/2)/self._scale,max_y+(100/self._scale)))
            if place_err_flag:                                                              # error displayed if ship goes off map error
                self._screen.blit(place_err_map, ((self._width/2)/self._scale,max_y+(100/self._scale)))
            if place_err_ship_flag:                                                         # error displated if ship would interact another ship error
                self._screen.blit(place_err_ship, ((self._width/2)/self._scale,max_y+(100/self._scale)))
            
            pg.display.update()                                                             # update display with the above stuff
                                                            ### END DISPLAY STUFF ###

                                                            ### EVENT STUFF ###
            events = pg.event.get()                                                         # get events from pygame

            for event in events:                                                            # Check all events
                if event.type == pg.KEYDOWN:                                                # If a key was pressed
                    if event.key == pg.K_RIGHT:                                             # If that key was rght
                        if placePrompt:                                                     # if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("right", num_ships, coords):           #check ship doesn't go off map or intersect a previsiouly placed ship
                                if self.check_ship_v_ship("right", num_ships, coords, shipList):
                                    cur_ship_image = shipImgs[turn][num_ships-1]                                                        # Get next ship image (Maybe put this out of the loop)
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale))   #scale give ship image by the needed values
                                                                                                                                        #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    cur_ship_image = pg.transform.rotate(cur_ship_image,90)                                             #rotate ship to match direction chosen
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-(2/self._scale))) #add ship image to placed_ship_objects so its drawn
                                    new_ship_coords = []                                         #create new coords for Ship ship
                                    for i in range(num_ships):                                   #iterate shipsize times
                                        new_ship_coords.append((coords[0]+i,coords[1]))          #mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "right")                     #create ship from coord list and direction
                                    shipList.append(newShip)                                     #append new Ship to shipList
                                    num_ships -= 1                                               #decrement ship number as one was placed
                                                        ## reset cursor position ## (Maybe don't do this? I find it annoying personally)
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    coords = [0,0]          #reset coords for ship building
                                    placePrompt = False     #no longer placing a ship so no more place prompt
                                else:                           #if ship check fails then ship placement collides with other ship
                                    placePrompt = False         #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True  #call error type
                            else:                               #if map check fails then ship placement goes off map
                                placePrompt = False             #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True           #call error type
                        else:                                       #if not placing a ship
                            if coords[0] < 9:                       #if not at max x coord
                                cursor.move_ip((100/self._scale),0) #move right 1 square
                                coords[0] += 1                      #update coords
                            else:
                                cursor.x = def_x     #otherwise reset cursor to orginal
                                coords[0] = 0                       #same with coords

                    elif event.key == pg.K_LEFT:                                    # If that key was left
                        if placePrompt:                                             #if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("left", num_ships, coords):    #check ship doesn't go off map or intersect a previsiouly placed ship
                                if self.check_ship_v_ship("left", num_ships, coords, shipList):
                                    cur_ship_image = shipImgs[turn][num_ships-1]                                                        #identical to above
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale))   # ""
                                    cur_ship_image = pg.transform.rotate(cur_ship_image,90)                                             # ""
                                    #place ship left by ship size squares for display reasons, look at dcumentation/ drawships function for details
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(num_ships * single_square_x)+single_square_x-(2/self._scale),cursor.y-(2/self._scale))) 
                                    new_ship_coords = []                                #same as above
                                    for i in range(num_ships):                          # ""
                                        new_ship_coords.append((coords[0]-i,coords[1])) # have to decrement coord instead of incrementing as going left not right
                                    newShip = Ship(new_ship_coords, "left")             # same as above but left
                                    shipList.append(newShip)                            # ""
                                    num_ships -= 1                                      # ""
                                                        ## reset cursor position ## (Maybe don't do this? I find it annoying personally)
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    coords = [0,0]          #reset coords for ship building
                                    placePrompt = False     #no longer placing a ship so no more place prompt

                                else:                           #if ship check fails then ship placement collides with other ship
                                    placePrompt = False         #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True  #call error type
                            else:                               #if map check fails then ship placement goes off map
                                placePrompt = False             #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True           #call error type
                        else:                                       #if not placing a ship
                            if coords[0] > 0:                       #if not on first square
                                cursor.move_ip(-(100/self._scale),0)#move left 1 square
                                coords[0] -= 1                      #update coords
                            else:
                                cursor.x = max_x                    #otherwise set cursor to max
                                coords[0] = 9                       #same with coords

                    elif event.key == pg.K_DOWN:                                        # If that key was down
                        if placePrompt:                                                 # If the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("down", num_ships, coords):        #check ship doesn't go off map or intersect a previsiouly placed ship
                                if self.check_ship_v_ship("down", num_ships, coords, shipList):
                                    cur_ship_image = shipImgs[turn][num_ships-1]                                                        # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale))   #scale give ship image by the needed values
                                                                                                                                        #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-(2/self._scale))) #add ship image to placed_ship_objects so its drawn
                                    new_ship_coords = []                                #create new coords for Ship ship
                                    for i in range(num_ships):                          #iterate shipsize times
                                        new_ship_coords.append((coords[0],coords[1]+i)) #mark coords of ship using that, iterating y coords
                                    newShip = Ship(new_ship_coords, "down")             #create ship from coord list
                                    shipList.append(newShip)                            #append new Ship to shipList
                                    num_ships -= 1                                      #decrement ship number as one was placed
                                                        ## reset cursor position ## (Maybe don't do this? I find it annoying personally)
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    coords = [0,0]          #reset coords for ship building
                                    placePrompt = False     #no longer placing a ship so no more place prompt

                                else:                           #if ship check fails then ship placement collides with other ship
                                    placePrompt = False         #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True  #call error type
                            else:                               #if map check fails then ship placement goes off map
                                placePrompt = False             #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True           #call error type
                        else:                                       #if not placing a ship
                            if coords[1] < 9:                       #if not at max y
                                cursor.move_ip(0,(100/self._scale)) #move right 1 down
                                coords[1] += 1                      #update coords
                            else:
                                cursor.y = def_y                    #otherwise reset cursor to orginal
                                coords[1] = 0                       #same with coords

                    elif event.key == pg.K_UP:                                          # If that key was down
                        if placePrompt:                                                 # If the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("up", num_ships, coords):          #check ship doesn't go off map or intersect a previsiouly placed ship
                                if self.check_ship_v_ship("up", num_ships, coords, shipList):
                                    cur_ship_image = shipImgs[turn][num_ships-1]                                                        # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale))   #scale give ship image by the needed values
                                                                                                                                        #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-num_ships * single_square_y + single_square_y - (2/self._scale)))
                                    new_ship_coords = []                                    #create new coords for Ship ship
                                    for i in range(num_ships):                              #iterate shipsize times
                                        new_ship_coords.append((coords[0],coords[1]-i))     #mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "up")                   #create ship from coord list
                                    shipList.append(newShip)                                #append new Ship to shipList
                                    num_ships -= 1                                          #decrement ship number as one was placed
                                                        ## reset cursor position ## (Maybe don't do this? I find it annoying personally)
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    coords = [0,0]          #reset coords for ship building
                                    placePrompt = False     #no longer placing a ship so no more place prompt

                                else:                           #if ship check fails then ship placement collides with other ship
                                    placePrompt = False         #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True  #call error type
                            else:                               #if map check fails then ship placement goes off map
                                placePrompt = False             #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True           #call error type
                        else:                                       #if not placing a ship
                            if coords[1] > 0:                           #if not at square 0
                                cursor.move_ip(0,-(100/self._scale))    #move up 1 square
                                coords[1] -= 1                          #update coords
                            else:
                                cursor.y = max_y                        #otherwise go to bottom
                                coords[1] = 9                           #same with coords

                    elif event.key == pg.K_RETURN:  #If enter key is pressed then remove error flags and start placement logic
                        placePrompt = True
                        place_err_flag = False
                        place_err_ship_flag = False
            if num_ships == 0: #once num_ships = 0, then all have been palced
                allPlaced = True #stop loop
        
        self._screen.fill("white")                                                      # set background color
        self._screen.blit(background, (0, 0))                                           # Display the boards
        pg.draw.rect(self._screen, 'red', cursor)                                       # Create cursor image
        self._screen.blit(placed, ((self._width/2)/self._scale,max_y+(100/self._scale))) #Display text saying all ships have been placed
        pg.display.update() #update display with new text
        pg.time.wait(1000)  #pause for a second for player to read
        return shipList     # Return the created ship list for constructor use




    def run(self):
        pg.init() # Initialize pygame, lets events be detected
        '''
        -------------------------------------------------------------------------------------------
        Local Variables
        -------------------------------------------------------------------------------------------
        '''
        running       = True                                    # boolean for running the game loop
            ### Getting images for game loop ####
        welcomeScreen = pg.image.load(os.path.join('assets', 'WelcomeScreen.png'))      # loading and scaling welcome screen image
        welcomeScreen = pg.transform.scale(welcomeScreen, (self._width/self._scale, self._height/self._scale))
        background    = pg.image.load(os.path.join('assets', 'LabeledBackground.png'))  # Loading and scaling background image
        background    = pg.transform.scale(background, (self._width/self._scale, self._height/self._scale))
        passToP0      = pg.image.load(os.path.join('assets', 'PassToP0.png'))           # Loading and scaling swap to p0 (red player) image
        passToP0      = pg.transform.scale(passToP0, (self._width/self._scale, self._height/self._scale))
        passToP1      = pg.image.load(os.path.join('assets', 'PassToP1.png'))           # Loading and scaling swap to p1 (green player) image
        passToP1      = pg.transform.scale(passToP1, (self._width/self._scale, self._height/self._scale))
        winScreen     = [pg.image.load(os.path.join('assets', 'RedWinScreen.png')),     # Loading and scaling win screens
                         pg.image.load(os.path.join('assets', 'GreenWinScreen.png'))]   
        winScreen     = [pg.transform.scale(winScreen[0], (self._width/self._scale, self._height/self._scale)),
                         pg.transform.scale(winScreen[1], (self._width/self._scale, self._height/self._scale))]
        '''
        gamePhase marks the phase of the game:
        0: Intro screen
        1: PlayerZero (Red) ship placement screen
        2: PlayerOne (Green) ship placement screen
        3: Shooting screen for either player
        4: Game over screen
        '''
        gamePhase        = 0                                     # initializes to 0 for the intro screen
        passingScreen    = False                                 # bool check to see if passing screen should overlay
        winner           = 2                                     # initializes to 2 to show no winner
        chosen_num_ships = 1                                     # default value for testing if skipping intro screen
        max_y            = (self._height-100)/self._scale        # sets max y height of window

        '''
        -------------------------------------------------------------------------------------------
        Game Loop
        -------------------------------------------------------------------------------------------
        '''
        while (running):                                        # continuous game loop
            self._screen.fill("white")                              # set background color
            if (passingScreen):                                     # displays passing screen                
                if (gamePhase == 1 or (self._battleship.turn == 0 and gamePhase == 3) and not self._usingAI):   # displays pass to PlayerZero screen if in placement phase or their turn in shooting phase
                    self._screen.blit(passToP0, (0, 0))
                elif not self._usingAI:                                                                         # displays pass to PlayerOne screen if in placement phase or their turn
                    self._screen.blit(passToP1, (0, 0))
                else:
                    font = pg.font.Font(None, 56)                                                               # creates a size 56 font
                    text = font.render("AI turn!", True, (0, 0, 0))                                             # creates text for the AI turn
                    self._screen.blit(text, (((self._width/2)-100)/self._scale, (self._height/2)/self._scale))  # adds text to screen
                    pg.display.flip()                                                                           # updates the game window
                    pg.time.wait(1000)
                pg.display.flip()                                       # updates the game window
                if self._usingAI:                                       # if playing against AI, automatically skip "pass to player" screens
                    passingScreen = False
                for event in pg.event.get():                            # tracking for some sort of event to get out of passing screen
                    if (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN):
                        passingScreen = False

            else:                                                   # continues displaying the game if not in passing mode
                '''
                -----------------------------------------------------------------------------------
                Intro Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 0):                                 # intro screen loop
                    self._screen.blit(welcomeScreen, (0, 0))            #display welcome screen
                    pg.display.flip()                                   #update display
                    for event in pg.event.get():                                            # waits for keyboard event
                        if (event.type == pg.KEYDOWN):
                            if (event.key == pg.K_1):                                       # checks for 1 keypress
                                chosen_num_ships = 1                                            # sets number of ships
                                passingScreen = True                                            # enables passing screen
                                gamePhase     = 1                                               # changes game phase to PlayerZero ship placement
                            elif (event.key == pg.K_2):                                       # checks for 2 keypress
                                chosen_num_ships = 2                                            # sets number of ships
                                passingScreen = True                                            # enables passing screen
                                gamePhase     = 1                                               # changes game phase to PlayerZero ship placement
                            elif (event.key == pg.K_3):                                       # checks for 3 keypress
                                chosen_num_ships = 3                                            # sets number of ships
                                passingScreen = True                                            # enables passing screen
                                gamePhase     = 1                                               # changes game phase to PlayerZero ship placement
                            elif (event.key == pg.K_4):                                       # checks for 4 keypress
                                chosen_num_ships = 4                                            # sets number of ships
                                passingScreen = True                                            # enables passing screen
                                gamePhase     = 1                                               # changes game phase to PlayerZero ship placement
                            elif (event.key == pg.K_5):                                       # checks for 5 keypress
                                chosen_num_ships = 5                                            # sets number of ships
                                passingScreen = True                                            # enables passing screen
                                gamePhase     = 1                                               # changes game phase to PlayerZero ship placement

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerZero Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 1):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    pg.display.flip()                                       # updates the game window
                    p0_ship_list = self._placeShips(0, chosen_num_ships)    #Create temp ship list to construct battlship with later
                    gamePhase = 2                                           #update gamephase
                    passingScreen = True                                    #start passing screen

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerOne Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 2):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    pg.display.flip()                                       # updates the game window
                    # randomPlaceShips can be used here to create the AI's board and then sent to Battleship
                    p1_ship_list = self._placeShips(1,chosen_num_ships)     #Create temp ship list to construct battlship with later
                    gamePhase = 3                                           #update gamephase
                    self._battleship = Battleship(p0_ship_list,p1_ship_list)# Create battleship properly
                    passingScreen = True                                    #start passing screen

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                Shooting Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 3):                                      # core shooting game loop
                    self._screen.blit(background, (0, 0))                   # draws boards
                    self._drawShips()                                       # draws current players' ships
                    self._drawShots()                                       # draws shots on each board
                    pg.display.flip()                                       # updates the game window

                    # checks if not playing against AI or if it is the player's turn
                    # if so, use the wait for mouse
                    if not self._usingAI or self._battleship.turn == 0:
                        for event in pg.event.get():                            # waits for mouse event
                            if (event.type == pg.MOUSEBUTTONDOWN):              # if event is mouse button down
                                mouse_coords = (pg.mouse.get_pos())
                                coords = self._pixToCoords(mouse_coords,self._battleship.turn)          # gets the coordinates from the mouse position pixels
                                print(f'mouse coords: {mouse_coords}, grid coords: {coords}')
                                if (-1 in coords):                                      # invalid if either coordinate is negative (Should we tell the player?)
                                    continue                                                # goes to the next loop
                                    
                                # count total number of sunk ships of both sides before turn
                                curShipsSunk = [ship.isSunk() for ship in self._battleship.boardZero.shipList + self._battleship.boardOne.shipList].count(True)
                                winner = self._battleship.takeTurn(coords)              # sends coordinates to Battleship to take turn
                                # count sunk ships again after turn to see if a new ship has been sunk
                                newShipSunk = [ship.isSunk() for ship in self._battleship.boardZero.shipList + self._battleship.boardOne.shipList].count(True) > curShipsSunk

                                if (winner == 3):                                       # passes if the shot was invalid
                                    continue
                                
                                shotHit = False                                         # default value assuming shot missed
                                if (self._battleship.turn == 0):                        # checks if turn is set to 0
                                    if self._battleship.boardZero.coordsMatrix[coords[0]][coords[1]] != 1:  # checks boardZero value at coord
                                        shotHit = True                                                          # sets to true if shot was not a miss
                                else:                                                   # if turn is set to 1
                                    if self._battleship.boardOne.coordsMatrix[coords[0]][coords[1]] != 1:   # checks boardOne value at coord
                                        shotHit = True                                                          # sets to true if shot was not a miss

                                font = pg.font.Font(None, 36)                           # set font size to 36 px
                                if shotHit:
                                    if newShipSunk: # special message+sfx for sinking a ship
                                        text_surface = font.render("Hit! Sunk Ship!", True, (0,0,0))  # Tell the user the shot hit + ship sunk
                                        self._soundManager.playSink() # play sink.mp3
                                        self._animationManager.playAnimation(self._screen, mouse_coords, 'sink')
                                    else: # normal message+sfx for hitting a ship but not sinking it
                                        text_surface = font.render("Hit!", True, (0,0,0))       # Tell the user the shot hit
                                        self._soundManager.playHit() # play hit.mp3
                                        self._animationManager.playAnimation(self._screen, mouse_coords, 'hit')
                                else:
                                    text_surface = font.render("Miss!", True, (0,0,0))      # Tell the user the shot miss
                                    self._soundManager.playMiss() # play miss.mp3
                                    self._animationManager.playAnimation(self._screen, mouse_coords, 'miss')
                                
                                self._screen.blit(text_surface, ((self._width/2)/self._scale,max_y+(100/self._scale)))
                                pg.display.flip()
                                pg.time.wait(2000)

                                if (winner != 2):                                       # someone has won if a 0 or 1 is returned, no one has one if it is a 2
                                    self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                                    gamePhase = 4

                                else:
                                    passingScreen = True                                    # sets passing screen flag for end of turn
                    else:
                        # count total number of sunk ships of both sides before turn
                        coords = self._battleshipAI.aiTurn(self._battleship.boardZero) # generate a set of coordinates for attack based on difficulty
                        curShipsSunk = [ship.isSunk() for ship in self._battleship.boardZero.shipList + self._battleship.boardOne.shipList].count(True)
                        winner = self._battleship.takeTurn(coords)              # sends coordinates to Battleship to take turn
                        # count sunk ships again after turn to see if a new ship has been sunk
                        newShipSunk = [ship.isSunk() for ship in self._battleship.boardZero.shipList + self._battleship.boardOne.shipList].count(True) > curShipsSunk

                        if (winner != 2):                                       # someone has won if a 0 or 1 is returned, no one has one if it is a 2
                            self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                            gamePhase = 4
                        else:
                            passingScreen = True                                    # sets passing screen flag for end of turn

                    if passingScreen:                                       # breaks loop to enter passing screen
                        break

                '''
                -----------------------------------------------------------------------------------
                Winner Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 4):                                  # game over screen
                    self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                    pg.display.flip()                                       # updates the game window
                    for event in pg.event.get():
                        if (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN):
                            '''
                            -----------------------------------------------------------------------
                            Reset values to play again
                            -----------------------------------------------------------------------
                            '''
                            gamePhase = 0                                       # reinitializes to 1 for the intro screen
                            winner    = 2                                       # reinitializes to 2 to show no winner
                            
    def main(self):
        # Display menu and get user choice
        game_mode = self._main_menu()
        print(game_mode)
        if game_mode > 0:                                      # checks if gamemode is not two-player
            self._battleshipAI = BattleshipAI(None, game_mode) # placeholder for board in BattleshipAI
            self._usingAI = True                               # marks that AI is a player
