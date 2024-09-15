'''
THIS FILE IS FOR TESTING PURPOSES AND IS NOT USED WITHIN THE PROPER GAME
'''
# Making this file to test pygame stuff
import pygame as pg
import os
from ship import Ship


class Image:

    def __init__(self, picture,x,y):
        self.picture = picture
        self.x = x
        self.y = y



pg.init()
mod = 2 #modify the size of the board so the screen isn't bigger than my monitor: also helps with rescaling
running = True #make sure the game loop is running
x = 2058 #x size of the board image
y = 1004 #y size of the board image
offset = 4/mod #calulate the offset of the tile sections given 4 pixels on orginal board

coords = [0,0] #"coordinates" of the cursor. 0,0 to 9,9 to ease in making ships

## Unused vars. potentially useful in other means
# section = 2 #define which half of the board is in use /////////Not actually used, just thought could be useful later
# right_half_x = (x+50)/2 
# right_half_y = y -2

single_square_x = ((((x-50)/2)-4)/10)/mod #define the x size of one square given a board:
#x is total size, 50 pixels between baords so eliminate those, then divide by 2 to get size of one board, subtract 4 border pixels,
# divide into 10 sections then div by mod

single_square_y = ((y-4)/10)/mod
# Same as x except only 1 board tall with no split so subtract 4 border pixels, divide by 10 sections then div by mod


max_x = x/mod - single_square_x #calculate the max x val of where cursor can be
max_y = y/mod - single_square_y #calculate the max y val of where cursor can be

min_x = ((x/mod) + (50/mod))/mod # calculate the min x, THIS IS USED TO SPECIFY WHICH PART OF THE BOARD TO USE
#if it were the left half, min_x would be 0
min_y = 0 #always 0, unless a new margin at the top is added.

#load the image of the board
board = pg.image.load(os.path.join('assets','background.png'))
board = pg.transform.scale(board,(x/mod,y/mod))#scale the board to the defined size, with mod as a modifier

shipImgs =         [pg.image.load(os.path.join('assets', 'RedShip1.png')),     # loads all ship images
                     pg.image.load(os.path.join('assets', 'RedShip2.png')),
                     pg.image.load(os.path.join('assets', 'RedShip3.png')),
                     pg.image.load(os.path.join('assets', 'RedShip4.png')),
                     pg.image.load(os.path.join('assets', 'RedShip5.png'))]

placed_ship_objects = [] #Placeholder while player class doesn't exist
shipList = [] #made with real ships, from ships, by ships. landrew for the win.


screen =  pg.display.set_mode((x/mod,(y+100)/mod)) #Define size of the window: add 100 + on y to give space for text notices
cursor = pg.Rect((min_x + offset,offset), (single_square_x-offset,single_square_y-offset)) #make a rectangle to highlight where the cursor is
# first is coordinates, which is offset of min_x and min_y. this aligns cursor to the inside of the squares
#second is dimensions of the rectagle, which is the size of a single square - offset
font = pg.font.Font(None, 36)#set font size to 36 px

## CREATING TEXT FOR IN GAME EVENTS
text_surface = font.render("What Direction will the ship extend?", True, (0,0,0)) #remind players to choose a direction for ship to go
place_err_map = font.render("Ship off map", True, (0,0,0)) #Tell player that direction would make the ship go off the map
place_err_flag = False # a flag to use to display the ship place error.

place_err_ship = font.render("Ship would intersect Ship", True, (0,0,0)) #Tell player that direction would make the ship go off the map
place_err_ship_flag = False # a flag to use to display the ship place error.

placed = font.render("All Ships Have been Placed!", True, (0,0,0)) #Indicate ships have been placed

shipSizes = [1,2,3,4,5]
currentShip = 0
ships = []
shipsLeft = 5

# need to blit() if using an image
placePrompt = False

#Function to check that ship placement doesn't go off board
def check_ship_v_map(direction, ship_length, x, y):
    if direction == "right":#checking going right
        if x + ((ship_length-1)*single_square_x) > max_x:#if shiplength times number of squares goes off the board
            return False #return false
    elif direction == "left":
        if x - ((ship_length-1)*single_square_x) < min_x:#if shiplength times number of squares goes off the board
            return False #return false
    elif direction == "up":
        if y - ((ship_length-1)*single_square_y) < min_y:#if shiplength times number of squares goes off the board
            return False #return false
    elif direction == "down":
        if y + ((ship_length-1)*single_square_y) > max_y:#if shiplength times number of squares goes off the board
            return False #return false
    return True

#function to check if ship intersects ship
def check_ship_v_ship(direction, ship_length, coords, other_ships: list[Ship]):
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


while running:
    
    screen.fill("white")#set background color
    screen.blit(board,(0,0)) #create board image on the background at coordintes 0,0 (top left corner)
    pg.draw.rect(screen, 'red', cursor)#draw the red box for the cursor location

## test code, unneeded now
    # for ship in ships:#for all ships in ship
    #     pg.draw.rect(screen, 'blue', ship)
    
    for image in placed_ship_objects: # for ship in placed ships, draw the image of the ship
        screen.blit(image.picture, (image.x,image.y))

## DRAWING TEXT PROMPTS FOR USER
    if placePrompt:# to place ship
        screen.blit(text_surface, ((x/2)/mod,max_y+(100/mod)))
    if place_err_flag: #ship goes off map error
        screen.blit(place_err_map, (100/mod,max_y+(100/mod)))
    if place_err_ship_flag: #ship would interact another ship error
        screen.blit(place_err_ship, (100/mod,max_y+(100/mod)))
        

    
    if shipsLeft == 0:#when all ships are placed
        screen.blit(placed, (300,max_y+(100/mod)))# display the text saying so
        running = False # stop running loop
        pg.display.update() #update immediatly so text above can be seen
        pg.time.wait(2000) # wait a bit for user to see

    pg.display.update()#update the screen with all new blits and rects and whatever
   

    events = pg.event.get()#get events that have happened since last

    curShipSize = shipSizes[shipsLeft-1]   #determine current ship size, used for checking ship placement is valid

    for event in events: #checking all events
        if event.type == pg.KEYDOWN:#if a key was pressed
            if event.key == pg.K_RIGHT:#if the right arrow key was pressed
                if placePrompt:#if the placeprompt is on then do ship placement logic
                    if check_ship_v_map("right", curShipSize, cursor.x, cursor.y):
                        if check_ship_v_ship("right", curShipSize, coords, shipList):
                            curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                            cur_ship_image = shipImgs[shipsLeft-1]  # Get next ship image
                            cur_ship_image = pg.transform.scale(cur_ship_image,(100/mod,(100*curShipSize)/mod)) #scale give ship image by the needed values
                            #100 pixels x, 100* ship size as ships are oriented vertically until rotated
                            cur_ship_image = pg.transform.rotate(cur_ship_image,90)#rotate ship to match direction chosen
                            placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/mod),cursor.y-(2/mod)))#add ship image to placed_ship_objects so its drawn
                            new_ship_coords = [] #create new coords for Ship ship
                            for i in range(curShipSize):#iterate shipsize times
                                new_ship_coords.append((coords[0]+i,coords[1]))#mark coords of ship using that
                            newShip = Ship(new_ship_coords)#create ship from coord list
                            shipList.append(newShip)#append new Ship to shipList
                            shipsLeft -= 1 #decrement ship number as one was placed
                            #reset cursor position
                            cursor.x = min_x + offset 
                            cursor.y = offset
                            #reset coords for ship building
                            coords = [0,0]
                            #no longer placing a ship so no more place prompt
                            placePrompt = False
                        else:#if ship check fails then ship placement collides with other ship
                            placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                            place_err_ship_flag = True #call error type
                    else:#if map check fails then ship placement goes off map
                        placePrompt = False #no longer placing a ship because they chose a bad spot maybe
                        place_err_map = True #call error type
                else:#if not placing a ship
                    if cursor.x < max_x:#if not one square beyond max
                        cursor.move_ip(single_square_x,0)#move right 1 square
                        coords[0] += 1 #update coords
                    else:
                        cursor.x = min_x + offset #otherwise reset cursor to orginal
                        coords[0] = 0 #same with coords

            elif event.key == pg.K_LEFT:
                if placePrompt:
                    if check_ship_v_map("left", curShipSize, cursor.x, cursor.y):
                        if check_ship_v_ship("left", curShipSize, coords, shipList):
                            curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                            cur_ship_image = shipImgs[shipsLeft-1]
                            cur_ship_image = pg.transform.scale(cur_ship_image,(100/mod,(100*curShipSize)/mod))
                            cur_ship_image = pg.transform.rotate(cur_ship_image,-90)
                            placed_ship_objects.append(Image(cur_ship_image,cursor.x-(curShipSize * single_square_x)+single_square_x-(2/mod),cursor.y-(2/mod)))
                            new_ship_coords = [] #create new coords for Ship ship
                            for i in range(curShipSize):#iterate shipsize times
                                new_ship_coords.append((coords[0]-i,coords[1]))#mark coords of ship using that
                            newShip = Ship(new_ship_coords)#create ship from coord list
                            shipList.append(newShip)#append new Ship to shipList
                            shipsLeft -= 1 #decrement ship number as one was placed
                            cursor.x = min_x + offset
                            cursor.y = offset
                            coords = [0,0]
                            placePrompt = False
                        else:
                            placePrompt = False
                            place_err_ship_flag = True
                    else:
                        placePrompt = False
                        place_err_flag = True
                else:
                    if cursor.x > min_x + offset:
                        cursor.move_ip(-(single_square_x),0)
                        coords[0] -= 1
                    else:
                        cursor.x = max_x
                        coords[0] = 9
            
            elif event.key == pg.K_DOWN:
                if placePrompt:
                    if check_ship_v_map("down", curShipSize, cursor.x, cursor.y):
                        if check_ship_v_ship("down", curShipSize, coords, shipList):
                            curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                            cur_ship_image = shipImgs[shipsLeft-1]
                            cur_ship_image = pg.transform.scale(cur_ship_image,(100/mod,(100*curShipSize)/mod))
                            placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/mod),cursor.y-(2/mod)))
                            
                            new_ship_coords = [] #create new coords for Ship ship
                            for i in range(curShipSize):#iterate shipsize times
                                new_ship_coords.append((coords[0],coords[1]+i))#mark coords of ship using that
                            newShip = Ship(new_ship_coords)#create ship from coord list
                            shipList.append(newShip)#append new Ship to shipList
                            shipsLeft -= 1 #decrement ship number as one was placed
                            cursor.x = min_x + offset
                            cursor.y = offset
                            coords = [0,0]
                            placePrompt = False
                        else:
                            placePrompt = False
                            place_err_ship_flag = True
                    else:
                        placePrompt = False
                        place_err_flag = True

                else:
                    if cursor.y < max_y:               
                        cursor.move_ip(0,single_square_y)
                        coords[1] += 1
                    else:
                        cursor.y = offset
                        coords[1] = 0

            elif event.key == pg.K_UP:
                if placePrompt:
                    if check_ship_v_map("up", curShipSize, cursor.x, cursor.y):
                        if check_ship_v_ship("up", curShipSize, coords, shipList):
                            curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                            cur_ship_image = shipImgs[shipsLeft-1]
                            cur_ship_image = pg.transform.scale(cur_ship_image,(100/mod,(100*curShipSize)/mod))
                            placed_ship_objects.append(Image(cur_ship_image,cursor.x-(2/mod),cursor.y-curShipSize * single_square_y + single_square_y - (2/mod)))
                            new_ship_coords = [] #create new coords for Ship ship
                            for i in range(curShipSize):#iterate shipsize times
                                new_ship_coords.append((coords[0],coords[1]-i))#mark coords of ship using that
                            newShip = Ship(new_ship_coords)#create ship from coord list
                            shipList.append(newShip)#append new Ship to shipList
                            shipsLeft -= 1 #decrement ship number as one was placed
                            cursor.x = min_x + offset
                            cursor.y = offset
                            coords = [0,0]
                            placePrompt = False
                        else:
                            placePrompt = False
                            place_err_ship_flag = True
                    else:
                        placePrompt = False
                        place_err_flag = True
                    
                else:
                    if cursor.y > offset:
                        cursor.move_ip(0,-(single_square_y))
                        coords[1] -= 1
                    else:
                        cursor.y = max_y
                        coords[1] = 9

            # If the player is ready to place their ship
            elif event.key == pg.K_RETURN:#press the enter key
                placePrompt = True
                place_err_flag = False
                place_err_ship_flag = False

        elif event.type == pg.QUIT:#if quit event is called (the close button is pressed)
            running = False #stop running the game
