# Making this file to test pygame stuff
import pygame as pg
pg.init()

running = True
screen =  pg.display.set_mode((1000,1000))
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
                if rect.x < 900:
                    rect.move_ip(100,0)
                else:
                    rect.x = 0

            elif event.key == pg.K_LEFT:

                if rect.x > 0:
                    rect.move_ip(-100,0)
                else:
                    rect.x = 900
            
            elif event.key == pg.K_DOWN:

                if rect.y < 900:               
                    rect.move_ip(0,100)
                else:
                    rect.y = 0

            elif event.key == pg.K_UP:

                if rect.y > 0:
                    rect.move_ip(0,-100)
                else:
                    rect.y = 900
