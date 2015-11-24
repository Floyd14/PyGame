# -*- coding: UTF-8 -*-

imm_sfondo = "./Resources/ciaomondo.jpg"
import pygame
from pygame.locals import *
from sys import exit

##
# La libreria Pygame � divisa in moduli che gestiscono vari tipi di eventi, 
# per esempio display gestir� lo schermo, mentre mixer servir� per caricare 
# e gestire eventi sonori. Tutti i moduli sono avviabili singolarmente, ma 
# con pygame.init() li avvieremo tutti insieme,
##
pygame.init()

##
# creiamo una finestra 640�480 con doppio buffer (da notare che dobbiamo scrivere 
# solo DOUBLEBUF e non pygame.DOUBLEBUF perch� abbiamo importato le variabili locali), 
# accelerazione hardware (HWSURFACE) e con profondit� 32 bit
##
screen = pygame.display.set_mode((640,480), DOUBLEBUF | HWSURFACE, 32)

# settiamo il nome della finestra che abbiamo creato.
pygame.display.set_caption("Ciao Mondo!!!")

# carichiamo lo sfondo e lo convertiamo in una superficie per essere visualizzato
# sullo schermo. La conversione � necessaria.
sfondo = pygame.image.load(imm_sfondo).convert()

##
# Questo � il vero corpo di gioco, per ora. Il primo ciclo equivale in poche parole 
# ad una frame di gioco, mentre il secondo � indispensabile per controllare gli eventi 
# al di fuori del gioco per far interagire l�utente. In questo caso basta controllare
# solamente se viene premuto il tasto di uscita della finestra (la �x� della cornice).
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    screen.blit(sfondo,(0,0))
    
    ##
    # avendo utilizzato l’accelerazione hardware abbiamo aggiunto un secondo buffer; 
    # in poche parole in questo secondo buffer il computer si prepara il prossimo 
    # frame da visualizzare. Quindi quando stampiamo a video la nostra immagine non 
    # dobbiamo ridisegnare da capo, ma dobbiamo semplicemente scambiare il buffer 
    # attuale con quello successivo. In questo modo si evitano discrepanze visive 
    # dovute al refresh della memoria video che deve ridisegnare ogni volta la stessa 
    # immagine sullo stesso buffer.
    pygame.display.flip()

fff
