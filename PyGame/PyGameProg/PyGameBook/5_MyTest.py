# -*- coding: utf_8 -*-

'''
This is a game test for first 4th lessons. 

The program should:
- loads a backround, and an image that moves foward and back
- '''

import pygame as pg
import os

pg.init()
pg.display.set_mode((640,480), )
pg.display.set_caption('A Title...')

surface = pg.Surface(screen.get_size())
surface.convert()
backgroung_image = pg.image.load('./data/ente.jpg', )

mainloop = True
while mainloop:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                mainloop = False # user pressed ESC
    
    surface.blit(backgroung_image,(0,0)
    
    
    
    
    