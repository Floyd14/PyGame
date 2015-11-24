# -*- coding: UTF-8 -*-

##
#    -- Gestire Mause e Tastiera --
#
# http://www.appuntidigitali.it/author/mirco-tracolli/page/4/
#
# Lo scopo: fare in modo che il nostro gioco sia percepito alla stessa velocit� da 
# chiunque lo provi. Per fare questo utilizzeremo il modulo Time della libreria pygame.
##

imm_sfondo = "./Resources/introduzione.jpg"
mouse = "./Resources/puntatore.png"

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640,480), DOUBLEBUF | HWSURFACE, 32)
pygame.display.set_caption("Input Vari")

sfondo = pygame.image.load(imm_sfondo).convert()
puntatore = pygame.image.load(mouse).convert_alpha() # perchè è un immagine con alpha..

speed = 0.5
orologio = pygame.time.Clock()

# creo un tasto start (non disegnato è solo handler)
# .Rect( (cordinate vertice in alto a sinistra), (dimensioni del rettangolo)
tasto_start = pygame.Rect((200,100),(200,200))

# Controllo e assegnazione di eventuali joystic
controller = None
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
if controller is None:
    print ("Siamo spiacenti, ma hai bisogno di un joystick con almeno 10 tasti!")

# Inizializzo variabili per il movimento..
x , y = 0,0
move_x, move_y = 0,0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        
        # Controllo Tasti Premuti..
        elif event.type == KEYDOWN:          
            # ..li metto il lista..
            tasti_premuti = pygame.key.get_pressed()
            if tasti_premuti[K_ESCAPE]:
                exit()
            if tasti_premuti[K_LALT] and tasti_premuti[K_F4]:
                exit()
            # ..oppure ci accedo direttamente..
            if event.key == K_UP:
                move_y = -1
            if event.key == K_DOWN:
                move_y = 1
            if event.key == K_LEFT:
                move_x = -1
            if event.key == K_RIGHT:
                move_x = 1
        # Controllo tasti rilasciati..        
        elif event.type == KEYUP:
            if event.key == K_UP:
                move_y = 0
            if event.key == K_DOWN:
                move_y = 0
            if event.key == K_LEFT:
                move_x = 0
            if event.key == K_RIGHT:
                move_x = 0
         
        # Gestisco i tasti del mouse premuti: li metto in lista  
        pulsanti_mouse = pygame.mouse.get_pressed() 
        # pulsante sinistro..
        if pulsanti_mouse[0]==1:
            coordinate_mouse_attuali = pygame.mouse.get_pos()
            # Se sono nella scermata introduzione e clicco il rettangolo con il tasto sinistro.. cambio immagine..
            if imm_sfondo == "./Resources/introduzione.jpg":
                if tasto_start.collidepoint(coordinate_mouse_attuali):
                    imm_sfondo = "./Resources/giocoavviato.jpg"
                    sfondo = pygame.image.load(imm_sfondo).convert()
        
        # pulsante destro..
        if pulsanti_mouse[2]==1:
            # se sono nella schermata gioco avviato vado all'introduzione con il tasto destro
            if imm_sfondo == "./Resources/giocoavviato.jpg":
                imm_sfondo = "./Resources/introduzione.jpg"
                sfondo = pygame.image.load(imm_sfondo).convert()
        
        # Se il controller c'è e premo il pulsante 8...
        if controller != None and controller.get_button(7):
            if imm_sfondo == "./Resources/introduzione.jpg":
                imm_sfondo = "./Resources/giocoavviato.jpg"
                sfondo = pygame.image.load(imm_sfondo).convert()
                
    # Disabilito il puntatore del mause di sistema e ottengo le coordinate del mouse..
    pygame.mouse.set_visible(False)
    coordinate_mouse = pygame.mouse.get_pos()
    
    # Setto l'orologio interno..
    tempo_passato = orologio.tick(60)
    tempo_passato_sec = tempo_passato/1000.0
    
    # calcolo della distanza in base alla velocità da noi impostata..
    distanza_spostamento = tempo_passato*speed
    
    # a seconda del tasto move_x vale +1 o -1 ...
    x += move_x*distanza_spostamento
    y += move_y*distanza_spostamento
    
    # faccio muovere il tasto start (non creo una copia).. insieme con l'immagine..
    tasto_start.move_ip( move_x*distanza_spostamento, move_y*distanza_spostamento)
    
    # riempe lo schermo di nero quando sposto l'immagine..
    screen.fill((0,0,0))
    screen.blit(sfondo,(x,y))
    screen.blit(puntatore,coordinate_mouse)
    
    # gestisco il buffer...
    pygame.display.flip()
