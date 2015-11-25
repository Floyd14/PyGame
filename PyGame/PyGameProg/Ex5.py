# -*- coding: UTF-8 -*-

##
#    -- Game exemple, Classi, ecc  --
#    
# http://www.appuntidigitali.it/12120/sviluppare-un-gioco-in-python-il-suono-dei-videogiochi/
#
# vedi:
# http://www.charas-project.net/resources.php?lang=it
# http://www.tellim.com/texture_cd/
# http://www.freesound.org/
#
# Lo scopo: gestire suoni e musica..
##

import pygame
from pygame.locals import *
from sys import exit
 
# argomenti: nome della sprite, altezza h (quante sprites in altezza) e larghezza w della sprite, numero delle sprite
# ritorna una lista di frames..
def carica_imm_sprite(nome,h,w,num):
    # creo una lista in cui metteò le sprite..
    immagini = []
    # se l'immagine è 1 o None, carico l'immagine, forzando l'apha e ottengo le dimensioni..
    if num is None or num == 1:
        # Usare is None invece di num == None perchè:
        # Esempio:
        # >>> x = 1000
        # >>> x is 1000
        # False    -->  controllo solo l'ID (il puntatore) non il contenuto..
        # >>> x == 1000
        # True  
        imm1 =  pygame.image.load(nome+".png").convert_alpha()
        imm1_w, imm1_h = imm1.get_size()
        # seleziono il frame (x,y) ...
        # faccio variare x e y per interi ... in modo da selezionare uno a uno i vari frame..
        for y in range( int( imm1_h/h ) ):
            for x in range( int( imm1_w/w ) ):       
                # x*w ES frame 1 (x=1) per la lunghezza...
                # .subsurface taglia l'immagine: 
                # w,h = dimensioni dl rettangolo da ritagliare
                # x*w , y*h = coordinate 
                # .. appendo i ritagli nella lista immagini..
                immagini.append( imm1.subsurface(( x*w, y*h, w, h)))
        # ritorno la lista
        return immagini
    # altrimenti se ho più immagini..chiamate nome + un numero indicativo finale...
    # le converto e le appendo..
    else:
        for x in range(1,num):
            imm1 = pygame.image.load( nome+str(x)+".png").convert_alpha()
            immagini.append(imm1)
        return immagini
 
# Passiamo ora alla funzione agg_rect(), che prende come argomento una sprite. 
# Il compito principale di questa parte di codice è quello di aggiornare le 
# coordinate rect (coordinate necessarie per le collisioni) di una qualsiasi
# sprite. L’aggiornamento viene effettuato tramite la funzione move_ip(x,y), 
# che fa parte di uno dei metodi di rect.
def agg_rect(sprite):
    x,y = sprite.coordinate
    s,t,o,p = sprite.rect
    sprite.rect.move_ip(int(x)-s,int(y)-t)


# Restituisce il tempo trascorso in sec..
def tps(orologio, fps):
    temp = orologio.tick(fps)
    tps = temp /1000.
    return tps
 
# Estende pygame.sprite.Sprite, così da ereditare alcuni metodi e proprietà..
class oggetto_esplosione(pygame.sprite.Sprite):
    #===========================================================================
    #  un nuovo oggetto abbiamo bisogno del nome, l’altezza e la larghezza della 
    #  sprite che utilizzeremo, le coordinate della posizione iniziale (xy), 
    #  l’oggetto screen (che rappresenza lo schermo dove si renderizza il tutto)
    #  e il numero di immagini che compongono la sprite (num).
    #===========================================================================
    def __init__(self, nome, altezza, larghezza, xy, screen, num):
        
        # Inizializzo la Srite..
        pygame.sprite.Sprite.__init__(self)
        # Setto attributi oggetto esplosione che è una Sprite...
        self.immagini = carica_imm_sprite(nome, altezza, larghezza, num) # carico le immagini
        self.immagine = self.immagini[0] # imposto l'immagine iniziale

        self.coordinate = (int(xy[0]),int(xy[1]))
        self.rect = pygame.Rect((int(xy[0]+65),int(xy[1]+43)),(50,50))

        self.screen = screen
        self.esplosione = False

        self.audio = pygame.mixer.Sound("104447__dkmedic__EXPLODE.wav")
        self.canale_ex = pygame.mixer.Channel(4)

        self.maxframe = len(self.immagini)
        self.frame_corrente = 0

        self.tempo_anim = 0.0

        self.fine = False

    def update(self, tps, stringa):
        if self.esplosione == False and stringa is None:
            if ambiente.get_volume() != 1.0 and self.tempo_anim >= 1:
                ambiente.set_volume(ambiente.get_volume()+0.01)
                a_vento.set_volume(a_vento.get_volume()+0.01)
            else:
                self.tempo_anim += tps
            return
        else:
            self.esplosione = True

        if self.esplosione == True:
            if self.tempo_anim > 0.025 and self.frame_corrente != self.maxframe:
                if self.frame_corrente == 0:
                    ambiente.pause()
                    a_vento.pause()
                    self.canale_ex = self.audio.play()
                self.immagine = self.immagini[self.frame_corrente]
                self.screen.blit(self.immagine,self.coordinate)
                self.frame_corrente += 1
                self.tempo_anim = 0

            elif self.frame_corrente == self.maxframe:
                self.frame_corrente = 0
                self.esplosione = False
                self.tempo_anim = 0
                if self.fine == True:
                    x = self.screen.get_width()/2
                    x -= fine_gioco.get_width()/2
                    y = self.screen.get_height()/2
                    y -= fine_gioco.get_height()/2
                    notrun(self.screen, x,y)
                ambiente.set_volume(0.10)
                a_vento.set_volume(0.10)
                ambiente.unpause()
                a_vento.unpause()
                return

            else:
                self.screen.blit(self.immagine,self.coordinate)
                self.tempo_anim += tps
                return
 
class oggetto_sprite(pygame.sprite.Sprite):
    def __init__(self,nome,altezza,larghezza,xy,screen, num, gruppo):
        pygame.sprite.Sprite.__init__(self)
        self.immagini = carica_imm_sprite(nome,altezza,larghezza,num)
        self.immagine = self.immagini[0]

        self.coordinate = (int(xy[0]),int(xy[1]))
        self.screen = screen
        self.rect = pygame.Rect((int(xy[0]),int(xy[1])),(larghezza,altezza))

        self.animazione = False
        self.anim_corrente = 0

        self.tempo_animazione = 0.0

        self.passo1 = pygame.mixer.Sound("passo1.wav")
        self.passo2 = pygame.mixer.Sound("passo2.wav")
        self.Passi = pygame.mixer.Channel(1)

        self.gruppo = gruppo
        self.vita = True

    def collisione(self):
        for x in self.gruppo:
            if self.rect.colliderect(x.rect)== True and self.vita == True:
                self.vita = False
                x.update(tempo_passato, "esplodi")
                x.fine = True

    def anime(self,frame):
        if self.animazione == False:
            self.anim_corrente = 0
            self.immagine = self.immagini[frame]
            return
        else :
            if self.tempo_animazione<0.150:
                self.tempo_animazione += orologio.get_time()/1000.
            else:
                self.immagine = self.immagini[self.anim_corrente+frame]
                if self.Passi.get_sound() is None or self.Passi.get_sound() != self.passo1:
                    if self.Passi.get_busy() == False:
                        self.Passi = self.passo1.play()
                    else:
                        self.Passi.queue(self.passo1)
                else :
                    if self.Passi.get_busy() == True:
                        self.Passi.queue(self.passo2)
                if self.anim_corrente < 3:
                    self.anim_corrente +=1
                else:
                    self.anim_corrente = 0
                self.tempo_animazione = 0

    def update(self, direzione,frame):

        self.animazione = True
        self.anime(frame)
        x,y = self.coordinate
        if direzione == "basso":
            y += 1*speed*tempo_passato
            self.coordinate = x,y
            return
        if direzione == "alto":
            y -= 1*speed*tempo_passato
            self.coordinate = x,y
            return
        if direzione == "destra":
            x += 1*speed*tempo_passato
            self.coordinate = x,y
            return
        if direzione == "sinistra":
            x -= 1*speed*tempo_passato
            self.coordinate = x,y
            return

        elif direzione == "stop":
            self.animazione = False
            self.Passi.stop()

    def render(self):
        agg_rect(self)
        self.collisione()
        self.screen.blit(self.immagine, self.coordinate)
 
def notrun(screen,x,y):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                tasti_premuti = pygame.key.get_pressed()
                if tasti_premuti[K_ESCAPE]:
                    exit()
                elif tasti_premuti[K_LALT] and tasti_premuti[K_F4]:
                    exit()
                if tasti_premuti[K_RETURN]:
                    pygame.quit()
                    run()

        screen.fill((0,0,0))
        screen.blit(fine_gioco, (x,y))
        pygame.display.flip()

 
def run():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    pygame.display.set_caption("Sprites")

    schermo = pygame.display.set_mode((640,480),DOUBLEBUF|HWSURFACE,32)

    sfondo_erba = pygame.image.load("grass3_cyc.jpg").convert()
    sfondo_erba_scalato = pygame.transform.scale(sfondo_erba, (640,480))

    pygame.mixer.music.load("Relocation.mp3")

    esplosione1 = oggetto_esplosione("Explode",96,96,(320,340),schermo,8)
    esplosione2 = oggetto_esplosione("Explode",96,96,(100,200),schermo,8)
    esplosione3 = oggetto_esplosione("Explode",96,96,(300,100),schermo,8)
    esplosione4 = oggetto_esplosione("Explode",96,96,(450,50),schermo,8)
    esplosione5 = oggetto_esplosione("Explode",96,96,(400,300),schermo,8)

    esplosioni = pygame.sprite.Group()
    esplosioni.add(esplosione1, esplosione2, esplosione3, esplosione4, esplosione5)

    personaggio = oggetto_sprite("27382_1174921384",48,32, (320,240),schermo,None,esplosioni)

    pygame.key.set_repeat(100, 30)

    global fps
    global orologio
    global speed
    global tempo_passato
    global ambiente
    global a_vento
    global fine_gioco

    vento = pygame.mixer.Sound("34338__ERH__wind.wav")
    pioggia = pygame.mixer.Sound("81389__joedeshon__thunder_with_rain_02.wav")

    ambiente = pygame.mixer.Channel(2)
    a_vento = pygame.mixer.Channel(3)

    speed = 30.0
    orologio = pygame.time.Clock()
    fps = 30

    mio_font = pygame.font.SysFont('dejavusans.ttf', 100)
    fine_gioco = mio_font.render("GAME OVER", True, (0,255,0))

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            elif event.type == KEYDOWN:

                tasti_premuti = pygame.key.get_pressed()

                if tasti_premuti[K_ESCAPE]:
                    exit()
                elif tasti_premuti[K_LALT] and tasti_premuti[K_F4]:
                    exit()

                if tasti_premuti[K_DOWN]:
                    personaggio.update("basso",0)
                if tasti_premuti[K_UP]:
                    personaggio.update("alto",12)
                if tasti_premuti[K_RIGHT]:
                    personaggio.update("destra",8)
                if tasti_premuti[K_LEFT]:
                    personaggio.update("sinistra",4)
                if tasti_premuti[K_m]:
                    if pygame.mixer.music.get_busy() == False:
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.stop()
                if tasti_premuti[K_SPACE]:
                    if ambiente.get_busy() == False:
                        ambiente = pioggia.play(-1)
                        a_vento = vento.play(-1)
                    else:
                        ambiente.stop()
                        vento.stop()
                if tasti_premuti[K_RETURN]:
                    esplosioni.update(tempo_passato, "esplodi")

            elif event.type == KEYUP:

                tasti_rilasciati = pygame.key.get_pressed()

                if tasti_rilasciati[K_DOWN]:
                    personaggio.update("stop",0)
                if tasti_rilasciati[K_UP]:
                    personaggio.update("stop",12)
                if tasti_rilasciati[K_RIGHT]:
                    personaggio.update("stop",8)
                if tasti_rilasciati[K_LEFT]:
                    personaggio.update("stop",4)
                if tasti_rilasciati[K_RETURN]:
                    esplosioni.update(tempo_passato, None)

        tempo_passato = tps(orologio,fps)

        schermo.fill((0,0,0))
        schermo.blit(sfondo_erba_scalato, (0,0))
        personaggio.render()

        esplosioni.update(tempo_passato, None)

        pygame.display.flip()

if __name__ == "__main__":
    run()
