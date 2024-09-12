# Making this file to test pygame stuff
import pygame as pg
pg.init()

running = True
x = 1000
y = 1000
single_square_x = x / 10
single_square_y = y / 10

max_x = x - single_square_x
max_y = y - single_square_y

screen =  pg.display.set_mode((x,y))
rect = pg.Rect((0,0), (100,100))

# need to blit() if using an image

while running:
    screen.fill('black')
    pg.draw.rect(screen, 'red', rect)
    pg.display.update()

    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if rect.x < max_x:
                    rect.move_ip(single_square_x,0)
                else:
                    rect.x = 0

            elif event.key == pg.K_LEFT:

                if rect.x > 0:
                    rect.move_ip(-(single_square_x),0)
                else:
                    rect.x = max_x
            
            elif event.key == pg.K_DOWN:

                if rect.y < max_y:               
                    rect.move_ip(0,single_square_y)
                else:
                    rect.y = 0

            elif event.key == pg.K_UP:

                if rect.y > 0:
                    rect.move_ip(0,-(single_square_y))
                else:
                    rect.y = max_y
