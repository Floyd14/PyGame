# -*- coding: UTF-8 -*-

#===============================================================================
# This conteins all the global constants of the project.
# DON'T MODIFY THIS FILE
#===============================================================================
import os

class Path:
    def __init__(self):
        self.pulsantiImages = os.getcwd() + '\Assets\Data\Pulsanti'
        self.images = os.getcwd + '\Assets\Data\img'
        self.musics = self.sounds
        self.sounds = os.getcwd() + '\Assets\Data\Sound'
        
        
#if __name__=='__main__':
#    print os.getcwd()