# Making this file to test pygame stuff
import pygame as pg
import os


class Image:

    def __init__(self, picture,x,y):
        self.picture = picture
        self.x = x
        self.y = y



pg.init()

running = True
x = 1500
y = 1000

right_half_x = x/2
right_half_y = y/2

single_square_x = x / 10
single_square_y = y / 10


max_x = x - single_square_x
max_y = y - single_square_y

board = pg.image.load(os.path.join('assets','background.png'))
board = pg.transform.scale(board,(x,y))

shipImgs =         [pg.image.load(os.path.join('assets', 'RedShip1.png')),     # loads all ship images
                     pg.image.load(os.path.join('assets', 'RedShip2.png')),
                     pg.image.load(os.path.join('assets', 'RedShip3.png')),
                     pg.image.load(os.path.join('assets', 'RedShip4.png')),
                     pg.image.load(os.path.join('assets', 'RedShip5.png'))]

placed_ship_objects = []


screen =  pg.display.set_mode((x,y))
cursor = pg.Rect((0,0), (80,80))
font = pg.font.Font(None, 36)
text_surface = font.render("What Direction will the ship extend?", True, (0,0,0))

placed = font.render("All Ships Have been Placed!", True, (0,0,0))
exit = False

shipSizes = [1,2,3,4,5]
currentShip = 0
ships = []
shipsLeft = 5

# need to blit() if using an image
placePrompt = False

while running:
    screen.fill("white")
    screen.blit(board,(0,0))
    pg.draw.rect(screen, 'red', cursor)

    for ship in ships:
        pg.draw.rect(screen, 'blue', ship)
    
    for image in placed_ship_objects:
        screen.blit(image.picture, (image.x,image.y))

    if placePrompt:
        screen.blit(text_surface, (500,500))

    
    if shipsLeft == 0:
        screen.blit(placed, (300,50))
        running = False
        pg.display.update()
        pg.time.wait(2000)

    pg.display.update()
   

    events = pg.event.get()

    


    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if placePrompt:
                    curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                    cur_ship_image = shipImgs[shipsLeft-1]
                    cur_ship_image = pg.transform.rotate(cur_ship_image,90)
                    placed_ship_objects.append(Image(cur_ship_image,cursor.x,cursor.y))
                    #newShip = pg.Rect((cursor.x,cursor.y), (curShipSize * single_square_x,single_square_y))     # Create a new rectangle of the new ship
                    #ships.append(newShip)
                    shipsLeft -= 1
                    cursor.x = 0
                    cursor.y = 0
                    placePrompt = False

                else:
                    if cursor.x < max_x:
                        cursor.move_ip(single_square_x,0)
                    else:
                        cursor.x = 0

            elif event.key == pg.K_LEFT:
                if placePrompt:
                    curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                    cur_ship_image = shipImgs[shipsLeft-1]
                    cur_ship_image = pg.transform.rotate(cur_ship_image,-90)
                    placed_ship_objects.append(Image(cur_ship_image,cursor.x-(curShipSize * single_square_x)+single_square_x,cursor.y))
                    newShip = pg.Rect((cursor.x - (curShipSize * single_square_x) + single_square_x,cursor.y), (curShipSize * single_square_x,single_square_y))     # Create a new rectangle of the new ship
                    #ships.append(newShip)
                    shipsLeft -= 1
                    cursor.x = 0
                    cursor.y = 0
                    placePrompt = False
                
                else:
                    if cursor.x > 0:
                        cursor.move_ip(-(single_square_x),0)
                    else:
                        cursor.x = max_x
            
            elif event.key == pg.K_DOWN:
                if placePrompt:
                    curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                    cur_ship_image = shipImgs[shipsLeft-1]
                    placed_ship_objects.append(Image(cur_ship_image,cursor.x,cursor.y))
                    #newShip = pg.Rect((cursor.x,cursor.y), (single_square_x, curShipSize * single_square_y))     # Create a new rectangle of the new ship
                    #ships.append(newShip)
                    shipsLeft -= 1
                    cursor.x = 0
                    cursor.y = 0
                    placePrompt = False

                else:
                    if cursor.y < max_y:               
                        cursor.move_ip(0,single_square_y)
                    else:
                        cursor.y = 0

            elif event.key == pg.K_UP:
                if placePrompt:
                    curShipSize = shipSizes[shipsLeft-1]    # If we have 5 ships left, we want the 4th index. 4 left, 3rd index, and so on
                    cur_ship_image = shipImgs[shipsLeft-1]
                    placed_ship_objects.append(Image(cur_ship_image,cursor.x,cursor.y-curShipSize * single_square_y + single_square_y))
                    #newShip = pg.Rect((cursor.x,cursor.y - (curShipSize * single_square_y) + single_square_y), (single_square_x, curShipSize* single_square_y))     # Create a new rectangle of the new ship
                    #ships.append(newShip)
                    shipsLeft -= 1
                    cursor.x = 0
                    cursor.y = 0
                    placePrompt = False
                    
                else:
                    if cursor.y > 0:
                        cursor.move_ip(0,-(single_square_y))
                    else:
                        cursor.y = max_y

            # If the player is ready to place their ship
            elif event.key == pg.K_RETURN:
                placePrompt = True

