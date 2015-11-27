# -*- coding: utf_8 -*-

'''
This is a game test for first 4th lessons'''

import pygame as pg
import os

###

opts = {'width': 800,
        'height': 600,
        'backcol': (0, 0, 0),
        'fps': 100}

###

def setScreen(width=800, height=600, collision=True, **opts):
    screen_surface = pg.display.set_mode( (width,height), )
    if collision:
        screen_rect = screen_surface.get_rect()



mainloop = True
while mainloop:  
    pg.init()
    setScreen()
    clock = pg.time.Clock()
    milliseconds = clock.tick( opts['fps'] )      # do not go faster than this framerate
    playtime += milliseconds / 1000.0
    
    
    
    # for stopping the mainloop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                mainloop = False # user pressed ESC
                
               


