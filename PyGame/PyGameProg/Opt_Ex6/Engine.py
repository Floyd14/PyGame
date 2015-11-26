# -*- coding: UTF-8 -*-

#===============================================================================
# This conteins all the engine of the project.
# DON'T MODIFY THIS FILE
#===============================================================================
from Global import Path
import pygame as pg

def tps(orologio, fps):
    temp = orologio.tick(fps)
    tps = temp /1000.
    return tps

def carica_imm_sprite(nome, h, w, num):
    immagini = []
    if num is None or num == 1:
        sprite =  pg.image.load(Path.images + nome + ".png").convert_alpha()
        #sprite_w, sprite_h = imm1.get_size()
        
        [immagini.append(sprite.subsurface(x*w, y*h, w, h)) for x in range(int(sprite.get_size()[0])/h) for y in range(int(sprite.get_size()[1])/w)]
        #for y in range(int(imm1_h/h)):
        #   for x in range(int(imm1_w/w)):
        #      immagini.append(imm1.subsurface((x*w, y*h, w, h)))     
    else:
        for x in range(1,num):
            sprite = pg.image.load("data/"+nome+str(x)+".png").convert_alpha()
            immagini.append(sprite)
    return immagini



