

import pygame as pg

class MenuView:
    def __init__(self):
        self.setSfondo()
        self.addButton()
        
    def setSfondo(self, image):
        if type(image) is str:
            pg.image.load(image).convert()
        else:
            print('The method setSfondo() needs a strings as argument!')
            exit()
        
    def addButton(self, image):
        self.button
        if type(image) is str:
            pg.image.load(image).convert_alpha()
            pygame.Rect((self.x-150,self.y-200), (96,48))
            
        else:
            print('The method setSfondo() needs a strings as argument!')
            exit()
        
        return None
        
if __name__ == '__main__':
    #a = 'aa'
    #print (type(a))
    
    