import pygame as pg
import os
from battleship import Battleship
from ship import Ship
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Image:
    def __init__(self, picture,x,y):
        self.picture = picture
        self.x = x
        self.y = y

class PyGameLoop:
    def __init__(self):
        '''
        Each board is 1004x1004 and displayed side by side
        10x10 pixels for each box with a 2 pixel outside border
        50 pixel gap between them when displayed
        100 pixel gap on the left and top to show labels
        Left board is where the player shoots
        Right board is where the player places their ships
        '''
        singleBoardWidth  = 1004
        self._width       = 2 * singleBoardWidth + 50 + 100
        self._height      = 1004 + 100
        self._offset      = 4

        self._battleship  = Battleship([Ship([(0,0)])],[Ship([(0,0)])])
        self._screen      = pg.display.set_mode()     # initializes the window
        self._display_info = pg.display.Info()
        self._margin = 200 #margin of 200 pixels cause wtf not
        self._scale = 1
        # if self._width > (self._display_info.current_w + self._margin):
        #     self._scale = self._width/self._display_info.current_w

        # elif self._height > (self._display_info.current_h + self._margin):
        #     self._scale = self._height/self._display_info.current_h
        self._scale += 1
        self._offset /= self._scale
        self._screen      = pg.display.set_mode(((self._width+self._margin)/self._scale, (self._height+self._margin)/self._scale))     # initializes the window
        self._placedShips = [[], []]                                 # list to store the user placed locations of the ships

    #Function to check that ship placement doesn't go off board
    def check_ship_v_map(self, direction, ship_length, coords):
        if direction == "right":#checking going right
            if coords[0] + (ship_length-1) > 9:#if shiplength times number of squares goes off the board
                return False #return false
        elif direction == "left":
            if coords[0] - (ship_length-1) < 0:#if shiplength times number of squares goes off the board
                return False #return false
        elif direction == "up":
            if coords[1] - (ship_length-1) < 0:#if shiplength times number of squares goes off the board
                return False #return false
        elif direction == "down":
            if coords[1] + (ship_length-1) > 9:#if shiplength times number of squares goes off the board
                return False #return false
        return True

    #function to check if ship intersects ship
    def check_ship_v_ship(self, direction, ship_length, coords, other_ships: list[Ship]):
        if direction == "right":#checking whatever direction chosen
            for ship in other_ships:#for all ships placed already
                for i in range(ship_length):#iterating through ever potential spot of the current ship
                    if ship.isHit((coords[0]+i,coords[1])):#if the current spot would hit one of the other ships
                        return False #return false as ships intersect
        elif direction == "left":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.isHit((coords[0]-i,coords[1])):
                        return False
        elif direction == "down":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.isHit((coords[0],coords[1]+i)):
                        return False
        elif direction == "up":
            for ship in other_ships:
                for i in range(ship_length):
                    if ship.isHit((coords[0],coords[1]-i)):
                        return False
        return True

    def _coordsToPix(self, boardNum, coords):                                     # takes in 0 or 1 to indicate board to draw on and takes coords to returns pixels on given board
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

        return ((x + ((boardNum * 1054)/self._scale), y))                                     # if boardNum is 0, it's left board and won't shift, if 1, it'll add on the constant x value of the left board to shift
    
    
    def _pixToCoords(self, pix :tuple):                                                  # takes in pixels and returns coordinate values SHOULD ONLY BE NEEDED FOR LEFT BOARD AND NOT RIGHT BOARD
        x, y = -1, -1                                                           # initializes as -1 in case no coordinates are matched
        
        if (pix[1] < 202):
            y = 0
        elif (pix[1] < 302):
            y = 1
        elif (pix[1] < 402):
            y = 2
        elif (pix[1] < 502):
            y = 3
        elif (pix[1] < 602):
            y = 4
        elif (pix[1] < 702):
            y = 5
        elif (pix[1] < 802):
            y = 6
        elif (pix[1] < 902):
            y = 7
        elif (pix[1] < 1002):
            y = 8
        elif (pix[1] < 1104):
            y = 9

        if (pix[0] < 202):
            x = 0
        elif (pix[0] < 302):
            x = 1
        elif (pix[0] < 402):
            x = 2
        elif (pix[0] < 502):
            x = 3
        elif (pix[0] < 602):
            x = 4
        elif (pix[0] < 702):
            x = 5
        elif (pix[0] < 802):
            x = 6
        elif (pix[0] < 902):
            x = 7
        elif (pix[0] < 1002):
            x = 8
        elif (pix[0] < 1104):
            x = 9

        return ((x, y))


# Modified below section a bit. Checking if event.key is the right key instead of event.type

    def _createShips(self, p0Ships, p1Ships):                               # creates ship list based on number of ships
        for event in pg.event.get():                                            # waits for keyboard event
            if (event.type == pg.KEYDOWN):
                if (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5]):            # always adds one ship
                    p0Ships.append([(0, 0)])                                                # positions ship in 0th column
                    p1Ships.append([(0, 0)])                                                # positions ship in 0th column

                if (event.key in [pg.K_2, pg.K_3, pg.K_4, pg.K_5]):                    # adds second ship if at least 2
                    p0Ships.append([(1, 0), (1, 1)])                                        # positions ship in 0th column
                    p1Ships.append([(1, 0), (1, 1)])                                        # positions ship in 0th column

                if (event.key in [pg.K_3, pg.K_4, pg.K_5]):                            # adds third ship if at least 3
                    p0Ships.append([(2, 0), (2, 1), (2, 2)])                                # positions ship in 0th column
                    p1Ships.append([(2, 0), (2, 1), (2, 2)])                                # positions ship in 0th column

                if (event.key in [pg.K_4, pg.K_5]):                                    # adds fourth ship if at least 4
                    p0Ships.append([(3, 0), (3, 1), (3, 2), (3, 3)])                        # positions ship in 0th column
                    p1Ships.append([(3, 0), (3, 1), (3, 2), (3, 3)])                        # positions ship in 0th column

                if (event.key in [pg.K_5]):                                            # adds fifth ship if it is 5
                    p0Ships.append([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])                # positions ship in 0th column
                    p1Ships.append([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])                # positions ship in 0th column


    def _drawShips(self, player=None):                                      # draws a player's ships
        single_square_x = (100)/self._scale
        single_square_y = (100)/self._scale
        if (player is None):                                                    # runs if nothing passed in
            player = self._battleship.turn                                          # defaults to whose turn it is

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
        
        if player == 0:
            shipList = self._battleship.boardZero.shipList
        
        for ship in shipList:
            cur_ship_image = shipImgs[player][ship.get_length()-1]
            if ship._direction == "right":
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))
                cur_ship_image = pg.transform.rotate(cur_ship_image,90)
                self._screen.blit(cur_ship_image, self._coordsToPix(player, ship.coords[0]))
            elif ship._direction == "left":
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))
                cur_ship_image = pg.transform.rotate(cur_ship_image,90)
                place_at_temp = self._coordsToPix(player, ship.coords[0])
                place_at_x = place_at_temp[0] - (ship.get_length() * single_square_x)+single_square_x
                place_at_y = place_at_temp[1]
                place_at = tuple((place_at_x, place_at_y))
                self._screen.blit(cur_ship_image, place_at)
            elif ship._direction == "down":
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))
                self._screen.blit(cur_ship_image, self._coordsToPix(player, ship.coords[0]))
            elif ship._direction == "up":
                cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*ship.get_length())/self._scale))
                place_at_temp = self._coordsToPix(player, ship.coords[0])
                cur_ship_image = pg.transform.rotate(cur_ship_image,180)
                place_at_y = place_at_temp[1] - (ship.get_length() * single_square_y)+single_square_y
                place_at_x = place_at_temp[0]
                place_at = tuple((place_at_x, place_at_y))
                self._screen.blit(cur_ship_image, place_at)


    def _drawShots(self):                                                   # draws all the shots taken in the game on the correct side
        missedShot = pg.image.load(os.path.join('assets', 'MissedShot.png'))
        missedShot = pg.transform.scale(missedShot,(100/self._scale,100/self._scale))
        hitShot    = pg.image.load(os.path.join('assets', 'HitShot.png'))
        hitShot    = pg.transform.scale(hitShot,(100/self._scale,100/self._scale))
        sunkShot   = pg.image.load(os.path.join('assets', 'SunkShot.png'))
        sunkShot   = pg.transform.scale(sunkShot,(100/self._scale,100/self._scale))

        if (self._battleship.turn == 0):                                        # runs if current turn is PlayerZero
            for i in range(len(self._battleship.boardZero.coordsMatrix)):                  # iterates through current player's board rows
                for j in range(len(self._battleship.boardZero.coordsMatrix[0])):                                                 # iterates through current player's board columns
                    match self._battleship.boardZero.coordsMatrix[i][j]:                           # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 4:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot

            for i in range(len(self._battleship.boardOne.coordsMatrix)):                   # iterates through opponent's board rows
                for j in range(len(self._battleship.boardOne.coordsMatrix[0])):                                                 # iterates through opponent's board columns
                    match self._battleship.boardOne.coordsMatrix[i][j]:                            # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(1, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(1, (i, j)))                # draws hit shot
                        case 4:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(1, (i, j)))               # draws sunk shot

        else:                                                                   # runs if current turn is PlayerOne
            for i in range(len(self._battleship.boardOne.coordsMatrix)):                   # iterates through current player's board rows
                for j in range(len(self._battleship.boardOne.coordsMatrix[0])):                                                 # iterates through current player's board columns
                    match self._battleship.boardOne.coordsMatrix[i][j]:                            # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(1, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(1, (i, j)))                # draws hit shot
                        case 4:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(1, (i, j)))               # draws sunk shot

            for i in range(len(self._battleship.boardZero.coordsMatrix)):                  # iterates through opponent's board rows
                for j in range(len(self._battleship.boardZero.coordsMatrix[0])):                                                 # iterates through opponent's board columns
                    match self._battleship.boardZero.coordsMatrix[i][j]:                           # checks if the current position has been shot in some way
                        case 1:                                                                 # matches a missed shot value PLACEHOLDER NUMBER
                            self._screen.blit(missedShot, self._coordsToPix(0, (i, j)))             # draws missed shot
                        case 2:                                                                 # matches a hit shot value PLACEHOLDER NUMBER
                            self._screen.blit(hitShot, self._coordsToPix(0, (i, j)))                # draws hit shot
                        case 4:                                                                 # matches a sunk shot value PLACEHOLDER NUMBER
                            self._screen.blit(sunkShot, self._coordsToPix(0, (i, j)))               # draws sunk shot

    def _placeShips(self, turn, num_ships):
        background    = pg.image.load(os.path.join('assets', 'LabeledBackground.png'))  # PHOTO HAS BEEN UPDATED WITH LABELS AND NEW SIZE
        background    = pg.transform.scale(background, (self._width/self._scale, self._height/self._scale))
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
        
        ## CREATING TEXT FOR IN GAME EVENTS
        # pg.init()
        font = pg.font.Font(None, 36)#set font size to 36 px
        text_surface = font.render("What Direction will the ship extend?", True, (0,0,0)) #remind players to choose a direction for ship to go
        place_err_map = font.render("Ship off map", True, (0,0,0)) #Tell player that direction would make the ship go off the map
        place_err_flag = False # a flag to use to display the ship place error.

        place_err_ship = font.render("Ship would intersect Ship", True, (0,0,0)) #Tell player that direction would make the ship go off the map
        place_err_ship_flag = False # a flag to use to display the ship place error.

        placed = font.render("All Ships Have been Placed!", True, (0,0,0)) #Indicate ships have been placed

        # 1056? is starting position. Highlight starting position
        # Width of a square on the board is 102
        coords = [0,0] #"coordinates" of the cursor. 0,0 to 9,9 to ease in making ships
        single_square_x = (100)/self._scale
        single_square_y = (100)/self._scale
        if turn == 0:
            max_x = (1004)/self._scale
        elif turn == 1:
            max_x = (2058)/self._scale
        max_y = (self._height-100)/self._scale
        min_x = ((100 + (turn*1054))/self._scale)
        min_y = 100/self._scale
        highlightedSquare = (0,0)
        allPlaced = False
        placePrompt = False
        shipList = []
        placed_ship_objects = [] #Placeholder while player class doesn't exist

        def_x = min_x + self._offset
        def_y = (100/self._scale)+self._offset
        
        #cursor = pg.Rect((min_x + offset,offset), (single_square_x-offset,single_square_y-offset))((y-4)/10)/mod
        cursor = pg.Rect((def_x,def_y), (single_square_x-self._offset,single_square_y-self._offset))
        
        while not allPlaced:
            self._screen.fill("white")#set background color
            self._screen.blit(background, (0, 0))
            pg.draw.rect(self._screen, 'red', cursor)

            for image in placed_ship_objects: # for ship in placed ships, draw the image of the ship
                self._screen.blit(image.picture, (image.x,image.y))
            
            ## DRAWING TEXT PROMPTS FOR USER
            if placePrompt:# to place ship
                self._screen.blit(text_surface, ((self._width/2)/self._scale,max_y+(100/self._scale)))
            if place_err_flag: #ship goes off map error
                self._screen.blit(place_err_map, ((self._width/2)/self._scale,max_y+(100/self._scale)))
            if place_err_ship_flag: #ship would interact another ship error
                self._screen.blit(place_err_ship, ((self._width/2)/self._scale,max_y+(10/self._scale)))
            
            pg.display.update()

            events = pg.event.get()

            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        if placePrompt:#if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("right", num_ships, coords):
                                if self.check_ship_v_ship("right", num_ships, coords, shipList):
                                    # curShipSize = num_ships    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                                    cur_ship_image = shipImgs[turn][num_ships-1]  # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale)) #scale give ship image by the needed values
                                    #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    cur_ship_image = pg.transform.rotate(cur_ship_image,90)#rotate ship to match direction chosen
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-(2/self._scale)))#add ship image to placed_ship_objects so its drawn
                                    new_ship_coords = [] #create new coords for Ship ship
                                    for i in range(num_ships):#iterate shipsize times
                                        new_ship_coords.append((coords[0]+i,coords[1]))#mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "right")#create ship from coord list
                                    shipList.append(newShip)#append new Ship to shipList
                                    num_ships -= 1 #decrement ship number as one was placed
                                    #reset cursor position
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    #reset coords for ship building
                                    coords = [0,0]
                                    #no longer placing a ship so no more place prompt
                                    placePrompt = False
                                else:#if ship check fails then ship placement collides with other ship
                                    placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True #call error type
                            else:#if map check fails then ship placement goes off map
                                placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True #call error type
                        else:#if not placing a ship
                            if coords[0] < 9:#if not one square beyond max
                                cursor.move_ip((100/self._scale),0)#move right 1 square
                                coords[0] += 1 #update coords
                            else:
                                cursor.x = min_x + self._offset #otherwise reset cursor to orginal
                                coords[0] = 0 #same with coords
                    elif event.key == pg.K_LEFT:
                        if placePrompt:#if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("left", num_ships, coords):
                                if self.check_ship_v_ship("left", num_ships, coords, shipList):
                                    # curShipSize = num_ships    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                                    cur_ship_image = shipImgs[turn][num_ships-1]  # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale)) #scale give ship image by the needed values
                                    #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    cur_ship_image = pg.transform.rotate(cur_ship_image,-90)#rotate ship to match direction chosen
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(num_ships * single_square_x)+single_square_x-(2/self._scale),cursor.y-(2/self._scale)))
                                    new_ship_coords = [] #create new coords for Ship ship
                                    for i in range(num_ships):#iterate shipsize times
                                        new_ship_coords.append((coords[0]-i,coords[1]))#mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "left")#create ship from coord list
                                    shipList.append(newShip)#append new Ship to shipList
                                    num_ships -= 1 #decrement ship number as one was placed
                                    #reset cursor position
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    #reset coords for ship building
                                    coords = [0,0]
                                    #no longer placing a ship so no more place prompt
                                    placePrompt = False
                                else:#if ship check fails then ship placement collides with other ship
                                    placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True #call error type
                            else:#if map check fails then ship placement goes off map
                                placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True #call error type
                        else:#if not placing a ship
                            if coords[0] > 0:#if not one square beyond max
                                cursor.move_ip(-(100/self._scale),0)#move right 1 square
                                coords[0] -= 1 #update coords
                            else:
                                cursor.x = max_x #otherwise reset cursor to orginal
                                coords[0] = 9 #same with coords
                    elif event.key == pg.K_DOWN:
                        if placePrompt:#if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("down", num_ships, coords):
                                if self.check_ship_v_ship("down", num_ships, coords, shipList):
                                    # curShipSize = num_ships    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                                    cur_ship_image = shipImgs[turn][num_ships-1]  # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale)) #scale give ship image by the needed values
                                    #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-(2/self._scale)))#add ship image to placed_ship_objects so its drawn
                                    new_ship_coords = [] #create new coords for Ship ship
                                    for i in range(num_ships):#iterate shipsize times
                                        new_ship_coords.append((coords[0],coords[1]+i))#mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "down")#create ship from coord list
                                    shipList.append(newShip)#append new Ship to shipList
                                    num_ships -= 1 #decrement ship number as one was placed
                                    #reset cursor position
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    #reset coords for ship building
                                    coords = [0,0]
                                    #no longer placing a ship so no more place prompt
                                    placePrompt = False
                                else:#if ship check fails then ship placement collides with other ship
                                    placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True #call error type
                            else:#if map check fails then ship placement goes off map
                                placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True #call error type
                        else:#if not placing a ship
                            if coords[1] < 9:#if not one square beyond max
                                cursor.move_ip(0,(100/self._scale))#move right 1 square
                                coords[1] += 1 #update coords
                            else:
                                cursor.y = min_y + self._offset #otherwise reset cursor to orginal
                                coords[1] = 0 #same with coords
                    elif event.key == pg.K_UP:
                        if placePrompt:#if the placeprompt is on then do ship placement logic
                            if self.check_ship_v_map("up", num_ships, coords):
                                if self.check_ship_v_ship("up", num_ships, coords, shipList):
                                    # curShipSize = num_ships    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                                    cur_ship_image = shipImgs[turn][num_ships-1]  # Get next ship image
                                    cur_ship_image = pg.transform.scale(cur_ship_image,(100/self._scale,(100*num_ships)/self._scale)) #scale give ship image by the needed values
                                    #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                                    #cur_ship_image = pg.transform.rotate(cur_ship_image,180)#rotate ship to match direction chosen
                                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/self._scale),cursor.y-num_ships * single_square_y + single_square_y - (2/self._scale)))
                                    new_ship_coords = [] #create new coords for Ship ship
                                    for i in range(num_ships):#iterate shipsize times
                                        new_ship_coords.append((coords[0],coords[1]-i))#mark coords of ship using that
                                    newShip = Ship(new_ship_coords, "up")#create ship from coord list
                                    shipList.append(newShip)#append new Ship to shipList
                                    num_ships -= 1 #decrement ship number as one was placed
                                    #reset cursor position
                                    cursor.x = def_x
                                    cursor.y = def_y
                                    #reset coords for ship building
                                    coords = [0,0]
                                    #no longer placing a ship so no more place prompt
                                    placePrompt = False
                                else:#if ship check fails then ship placement collides with other ship
                                    placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                    place_err_ship_flag = True #call error type
                            else:#if map check fails then ship placement goes off map
                                placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                                place_err_flag = True #call error type
                        else:#if not placing a ship
                            if coords[1] > 0:#if not one square beyond max
                                cursor.move_ip(0,-(100/self._scale))#move right 1 square
                                coords[1] -= 1 #update coords
                            else:
                                cursor.y = max_y #otherwise reset cursor to orginal
                                coords[1] = 9 #same with coords
                    elif event.key == pg.K_RETURN:#press the enter key
                        placePrompt = True
                        place_err_flag = False
                        place_err_ship_flag = False
            if num_ships == 0:
                allPlaced = True
        return shipList




    def run(self):
        pg.init()
        '''
        -------------------------------------------------------------------------------------------
        Local Variables
        -------------------------------------------------------------------------------------------
        '''
        running       = True                                    # boolean for running the game loop
        fps           = 60                                      # frames per second of the window
        fpsClock      = pg.time.Clock()                         # clock that FPS is based on
        #font          = pg.font.SysFont('Arial', 40)            # sets font for text within window (COMMENTED OUT FOR NOW, THINGS NEED TO BE INSTALLED FOR THE FONT)

        welcomeScreen = pg.image.load(os.path.join('assets', 'WelcomeScreen.jpg'))      # PHOTO NOT YET ADDED #####TEMP PHOTOS ADDED TO MAKE TOPLEVEL WORK#######
        background    = pg.image.load(os.path.join('assets', 'LabeledBackground.png'))  # PHOTO HAS BEEN UPDATED WITH LABELS AND NEW SIZE
        background    = pg.transform.scale(background, (self._width/self._scale, self._height/self._scale))
        passToP0      = pg.image.load(os.path.join('assets', 'PassToP0.jpg'))           # PHOTO NOT YET ADDED #####TEMP PHOTOS ADDED TO MAKE TOPLEVEL WORK#######
        passToP1      = pg.image.load(os.path.join('assets', 'PassToP1.jpg'))           # PHOTO NOT YET ADDED #####TEMP PHOTOS ADDED TO MAKE TOPLEVEL WORK#######
        passToP1      = pg.transform.scale(passToP1, (self._width/self._scale, self._height/self._scale))
        winScreen     = [pg.image.load(os.path.join('assets', 'RedWinScreen.jpg')),     # PHOTO NOT YET ADDED #####TEMP PHOTOS ADDED TO MAKE TOPLEVEL WORK#######
                         pg.image.load(os.path.join('assets', 'BlueWinScreen.jpg'))]    # PHOTO NOT YET ADDED #####TEMP PHOTOS ADDED TO MAKE TOPLEVEL WORK#######
        '''
        gamePhase marks the phase of the game:
        0: Intro screen
        1: PlayerZero ship placement screen
        2: PlayerOne ship placement screen
        3: Shooting screen for either player
        4: Game over screen
        '''
        gamePhase       = 1                                     # initializes to 1 for the intro screen
        passingScreen   = False                                 # bool check to see if passing screen should overlay
        winner          = 2                                     # initializes to 2 to show no winner
        p0UnplacedShips = []                                    # list to store the ships before placed by PlayerOne
        p1UnplacedShips = []                                    # list to store the ships before placed by PlayerOne

        '''
        -------------------------------------------------------------------------------------------
        Game Loop
        -------------------------------------------------------------------------------------------
        '''
        while (running):                                        # continuous game loop
            self._screen.fill("white")#set background color
            chosen_num_ships = 5                                    # Need to be able to choose number of ships
            pg.display.flip()                                       # updates the game window
            if (passingScreen):                                     # displays passing screen
                if (gamePhase == 1 | self.battleship.turn == 0):        # displays pass to PlayerZero screen if in placement phase or their turn
                    self._screen.blit(passToP0, (0, 0))
                else:                                                   # displays pass to PlayerOne screen if in placement phase or their turn
                    self._screen.blit(passToP1, (0, 0))

            else:                                                   # continues displaying the game if not in passing mode
                '''
                -----------------------------------------------------------------------------------
                Intro Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 0):                                 # intro screen loop
                    self._screen.blit(welcomeScreen, (0, 0))
                    
                    self._createShips(p0UnplacedShips, p1UnplacedShips)     # populates default ship coordinates
                    if (len(p0UnplacedShips) != 0):                         # checks if ships have been populated yet
                        passingScreen = True                                    # enables passing screen
                        gamePhase     = 1                                       # changes game phase to PlayerZero ship placement

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerZero Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 1):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    #self._drawShips(0)                                      # draws PlayerZero ships
                    pg.display.flip()                                       # updates the game window
                    p0_ship_list = self._placeShips(0,chosen_num_ships)
                    self._screen.fill("black")#set background color
                    self._screen.blit(passToP1, (0, 0))
                    pg.display.update()
                    switch = True
                    while (switch):
                        events = pg.event.get()#get events that have happened since last
                        for event in events: #checking all events
                            if event.type == pg.KEYDOWN:#if a key was pressed
                                if event.key == pg.K_RETURN:#press the enter key
                                    switch = False
                    gamePhase = 2
                    # logic for actual ship placement needs to go here

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                PlayerOne Ship Placement Phase
                -----------------------------------------------------------------------------------
                '''
                while (gamePhase == 2):                                 # PlayerZero ship placement screen (CAN PROBABLY MAKE THE PLACEMENT PHASES A FUNCTION TO CALL FOR GIVEN PLAYER)
                    self._screen.blit(background, (0, 0))                   # displays game background containing both boards
                    #self._drawShips(1)                                      # draws PlayerZero ships
                    pg.display.flip()                                       # updates the game window
                    p1_ship_list = self._placeShips(1,chosen_num_ships)
                    gamePhase = 3
                    self._battleship = Battleship(p0_ship_list,p1_ship_list)             # Create battleship proper

                if (passingScreen):                                     # checks if passingScreen needs to display
                    continue                                                # continues to force the passing screen to display

                '''
                -----------------------------------------------------------------------------------
                Shooting Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 3):                                      # core shooting game loop
                    print("HELLO")
                    self._screen.blit(background, (0, 0))                   # draws boards
                    self._drawShips(self._battleship.turn)                  # draws current players' ships
                    self._drawShots()                                       # draws shots on each board
                    pg.display.flip()                                       # updates the game window

                    for event in pg.event.get():                            # waits for mouse event
                        if (event.type == pg.MOUSEBUTTONDOWN):              # if event is mouse button down
                            mouse_coords = (pg.mouse.get_pos())
                            coords = self._pixToCoords(mouse_coords)          # gets the coordinates from the mouse position pixels
                            if (-1 in coords):                                      # invalid if either coordinate is negative
                                continue                                                # goes to the next loop
                            
                            ##QUESTION Is there a reason to have this here?
                            # self._screen.blit(background, (0, 0))                   # draws boards
                            # self._drawShips()                                       # draws current players' ships
                            # self._drawShots()                                       # draws shots on each board
                            # pg.display.flip()                                       # updates the game window

                            winner = self._battleship.takeTurn(coords)              # sends coordinates to Battleship to take turn
                            print(winner)
                            if (winner != 2):                                       # someone has won if a 0 or 1 is returned, no one has one if it is a 2
                                self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                                gamePhase = 4

                            else:
                                passingScreen = True

                '''
                -----------------------------------------------------------------------------------
                Winner Screen Phase
                -----------------------------------------------------------------------------------
                '''
                while(gamePhase == 4):                                  # game over screen
                    self._screen.blit(winScreen[winner], (0, 0))            # displays the winner's screen
                    pg.display.flip()                                       # updates the game window
                    for event in pg.event.get():
                        if (event.type == pg.MOUSEBUTTONDOWN):
                            '''
                            -----------------------------------------------------------------------
                            Reset values to play again
                            -----------------------------------------------------------------------
                            '''
                            gamePhase        = 1                                    # reinitializes to 1 for the intro screen
                            winner           = 2                                    # reinitializes to 2 to show no winner
                            self._battleship = Battleship()                         # recreates Battleship
                            p0UnplacedShips.clear()                                 # clear ships
                            p1UnplacedShips.clear()                                 # clear ships
                            self._placedShips[0].clear()                            # clear ships
                            self._placedShips[1].clear()                            # clear ships
