# -*- coding: UTF-8 -*-

##
#    -- Gestire Mause e Tastiera --
#
# http://www.appuntidigitali.it/12120/sviluppare-un-gioco-in-python-il-suono-dei-videogiochi/
#
# Lo scopo: gestire i comandi
##

imm_sfondo = "./Resources/introduzione.jpg"
mouse = "./Resources/puntatore.png"

import pygame
from pygame.locals import *
from sys import exit

# imposto valori audio ( Hz, bit, stereo, buffer )
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((640,480), DOUBLEBUF | HWSURFACE, 32)
pygame.display.set_caption('Input Vari')

sfondo = pygame.image.load(imm_sfondo).convert()
puntatore = pygame.image.load(mouse).convert_alpha()

speed = 0.5
orologio = pygame.time.Clock()

tasto_start = pygame.Rect((200,100),(200,200))

controller = None

if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()

if controller is None:
    print ('Siamo spiacenti, ma hai bisogno di un joystick con almeno 10 tasti!')

x , y = 0,0
move_x, move_y = 0,0

# memorizzo gli effetti creati..
applausi = pygame.mixer.Sound('./Resources/applause-1.wav')
click = pygame.mixer.Sound('./Resources/come_on_1.wav')
click2 = pygame.mixer.Sound('./Resources/kisses.wav')
pygame.mixer.music.load('./Resources/Believe.wav')

playmusica = True
volume_musica = 1.0


# Main
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        elif event.type == KEYDOWN:
            tasti_premuti = pygame.key.get_pressed()

            if tasti_premuti[K_ESCAPE]:
                exit()
            if tasti_premuti[K_LALT] and tasti_premuti[K_F4]:
                exit()

            if event.key == K_UP:
                move_y = -1
            if event.key == K_DOWN:
                move_y = 1
            if event.key == K_LEFT:
                move_x = -1
            if event.key == K_RIGHT:
                move_x = 1

            if event.key == K_m:
                if playmusica:
                    playmusica = False
                else:
                    playmusica = True

            if event.key == K_KP_PLUS:
                if volume_musica == (1.0) and pygame.mixer.music.get_busy()==True:
                    volume_musica += 0.1
                    pygame.mixer.music.set_volume(volume_musica)

            if event.key == K_KP_MINUS:
                if volume_musica == (0.0) and pygame.mixer.music.get_busy()==True:
                    volume_musica -= 0.1
                    pygame.mixer.music.set_volume(volume_musica)

        elif event.type == KEYUP:

            if event.key == K_UP:
                move_y = 0
            if event.key == K_DOWN:
                move_y = 0
            if event.key == K_LEFT:
                move_x = 0
            if event.key == K_RIGHT:
                move_x = 0

        pulsanti_mouse = pygame.mouse.get_pressed()
        if pulsanti_mouse[0]==1:
            coordinate_mouse_attuali = pygame.mouse.get_pos()

            canaleclick = click.play()
            canaleclick.set_volume( 1.0 - (coordinate_mouse_attuali[0]/640.) , coordinate_mouse_attuali[0]/640.)

            if imm_sfondo == './Resources/introduzione.jpg':
                if tasto_start.collidepoint(coordinate_mouse_attuali):
                    canaleapp = applausi.play()
                    imm_sfondo = './Resources/giocoavviato.jpg';
                    sfondo = pygame.image.load(imm_sfondo).convert()

        if pulsanti_mouse[2]==1:

            canaleclick = click2.play()

            if imm_sfondo == './Resources/giocoavviato.jpg':
                imm_sfondo = './Resources/introduzione.jpg';
                sfondo = pygame.image.load(imm_sfondo).convert()

        if controller != None and controller.get_button(7):
            if imm_sfondo == './Resources/introduzione.jpg':

                canaleapp = applausi.play()

                imm_sfondo = './Resources/giocoavviato.jpg';
                sfondo = pygame.image.load(imm_sfondo).convert()

    if playmusica == True and pygame.mixer.music.get_busy()==False:
        pygame.mixer.music.play()

    if pygame.mixer.music.get_busy()==True and playmusica == False:
        pygame.mixer.music.stop()

    pygame.mouse.set_visible(False)
    coordinate_mouse = pygame.mouse.get_pos()

    tempo_passato = orologio.tick(60)
    tempo_passato_sec = tempo_passato/1000.0

    distanza_spostamento = tempo_passato*speed

    x += move_x*distanza_spostamento
    y += move_y*distanza_spostamento

    tasto_start.move_ip(move_x*distanza_spostamento,move_y*distanza_spostamento)

    screen.fill((0,0,0))
    screen.blit(sfondo,(x,y))
    screen.blit(puntatore,coordinate_mouse)

    pygame.display.flip()