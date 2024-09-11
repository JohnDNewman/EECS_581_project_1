# Making this file to test pygame stuff
import pygame as pg
pg.init()

running = True
screen =  pg.display.set_mode((1000,1000))
rect = pg.Rect((0,0), (100,100))
while running:
    pg.draw.rect(screen, 'red', rect)
    pg.display.update()