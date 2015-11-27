# -*- coding: utf_8 -*-

'''
This is a game test for first 4th lessons. 

The program should:
- loads a backround, and an image that moves foward and back
- '''

import pygame


# inizializzo i moduli
pygame.init()
# setto un display
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
pygame.display.set_caption('A Title..')

# setto un backgroung (Surface, superficie) nel display
pygame.Surface(screen.get_size()).convert() #convert for suit screen

# un orologio
FPS = 60
pygame.time.Clock(FPS)

# Un loop ... 
                
                
                