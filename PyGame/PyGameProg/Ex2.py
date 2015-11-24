# -*- coding: UTF-8 -*-

##
#    --PARALLAX SCROLLING--
#
# http://www.appuntidigitali.it/author/mirco-tracolli/page/4/
#
# Lo scopo: fare in modo che il nostro gioco sia percepito alla stessa velocità da 
# chiunque lo provi. Per fare questo utilizzeremo il modulo Time della libreria pygame.
##

imm_sfondo = "./Resources/ciaomondo.jpg"

import pygame
from pygame.locals import*
from sys import exit

# Avvio i moduli della libreria 
pygame.init()

# Setto la finestra con il titolo e lo sfondo...
screen = pygame.display.set_mode((640,480), DOUBLEBUF | HWSURFACE, 32) 
pygame.display.set_caption("Ciao Mondo FPS!!!")
sfondo = pygame.image.load(imm_sfondo).convert()

# Voglio renderizzare l'immagine partendo da una coordinata x che si sposta
spostamento_x = 0

# Sincronizzazione.. lo scopo non è solo far muovere l'immagine
# ma sincronizzare i frames..
# Imposto una velocità preimpostata e un orologio che tenga conto del tempo..
speed=250
orologio = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    # Implemento la sincronizzazione:
    # calcolo il tempo passato ogni 60s (/1000 perchè lo voglio in millisecondi)
    tempo_passato = orologio.tick(60)
    tempo_passato_msec = tempo_passato/1000.0
    
    # di quanto incremento lo spostamento?
    distanza_spostamento = tempo_passato_msec * speed
    
    # Quando lo spostamento è > 640 pixel torno indietro..
    if spostamento_x > 640:
        spostamento_x = 0
        
    # Incremento lo spostamento..
    spostamento_x += distanza_spostamento
    
    # blit(immagine ,(coordinate)) renderizza l'immagine
    screen.blit(sfondo,(spostamento_x , 0))
    # renderizzo in modo consecutivo...
    screen.blit(sfondo,(spostamento_x-640,0))
    
    # Alterno il buffer...
    pygame.display.flip()
