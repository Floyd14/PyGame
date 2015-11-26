# -*- coding: UTF-8 -*-

##
#    -- Game Menu e salvataggi  --
#    
# http://www.appuntidigitali.it/13619/sviluppare-un-gioco-in-python-menu-e-salvataggi-quarta-parte/
#
# vedi:
# http://www.charas-project.net/resources.php?lang=it
# http://www.tellim.com/texture_cd/
# http://www.freesound.org/
#
##
import pygame
from pygame.locals import *
from sys import exit
import cPickle

#===============================================================================
# As usuall: ritorna il tempo di gioco in secondi
#===============================================================================
def tps(orologio, fps):
    temp = orologio.tick(fps)
    tps = temp /1000.
    return tps


#===============================================================================
# As usuall: ritorna la lista di sprites..
#===============================================================================
def carica_imm_sprite(nome,h,w,num):
    immagini = []
    if num is None or num == 1:
        imm1 =  pygame.image.load("data/"+nome+".png").convert_alpha()
        imm1_w, imm1_h = imm1.get_size()

        for y in range(int(imm1_h/h)):
            for x in range(int(imm1_w/w)):
                immagini.append(imm1.subsurface((x*w,y*h,w,h)))
                
        return immagini
    else:
        for x in range(1,num):
            imm1 = pygame.image.load("data/"+nome+str(x)+".png").convert_alpha()
            immagini.append(imm1)
        return immagini
    
#===============================================================================
# Mancata gestione di Rect, perché in questo caso vogliamo solo muovere il 
# nostro giocatore sullo schermo e memorizzare la sua posizione con un 
# salvataggio. La gestione dell’animazione è identica, come la sua renderizzazione.
#===============================================================================
class giocatore(pygame.sprite.Sprite):
    def __init__(self,nome,altezza,larghezza,xy,num):
        pygame.sprite.Sprite.__init__(self)
        self.immagini = carica_imm_sprite(nome,altezza,larghezza,num)
        self.immagine = self.immagini[0]

        self.coordinate = (int(xy[0]),int(xy[1]))

        self.animazione = False
        self.anim_corrente = 0

        self.tempo_animazione = 0.0

        self.passo1 = pygame.mixer.Sound("data/sound/passo1.wav")
        self.passo2 = pygame.mixer.Sound("data/sound/passo2.wav")
        self.Passi = pygame.mixer.Channel(1)
        
#===============================================================================
# 
#===============================================================================

    def anime(self,frame):
        if self.animazione == False:
            self.anim_corrente = 0
            self.immagine = self.immagini[frame]
            return
        else :
            if self.tempo_animazione<0.075:
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

#===============================================================================
# update():  imposta l'animazioni true o false e aggiorna i frame con le nuove
# coordinate
#===============================================================================
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
            self.Passi.stop()
            self.animazione = False
            
#===============================================================================
# Questa classe ha il compito di mantere e gestire l’istanza di gioco. In 
# questo caso viene inizializzata con il giocatore corrente, lo schermo dove 
# si deve renderizzare e l’immagine dello sfondo.
# Il render è molto semplice e consiste solo nel fatto di stampare a video 
# l’immagine dello sfondo con il giocatore.
# Questa classe è necessaria, in questo esempio, per passare dal menù al gioco 
# e viceversa. Separando le due cose infatti, è più semplice gestire quello che 
# sono le semplici meccaniche di gioco dalla gestione esterna. Nella nostra 
# situazione però, come già accennato, sarà sempre il menù ad avere il “comando” 
# della situazione.
#===============================================================================
class ingame():
    def __init__(self, player1, screen1, base):
        self.giocatore = player1 #giocatore
        self.screen = screen1 # schermo dove si renderizza
        self.base = base #sfondo
        
    # renderizza lo screen
    def render(self):
        self.screen.blit(self.base, (0,0))
        self.screen.blit(self.giocatore.immagine, self.giocatore.coordinate)


#===============================================================================
# Come possiamo vedere, questa classe ha bisogno solo di essere inizializzata 
# con delle impostazioni di base. Per ora non abbiamo impostato nessun metodo 
# che lavori su di essa, perché ho preferito agire direttamente sui suoi
# componenti per cambiare lo stato delle cose. Essendo gestita in questo modo, 
# non ha bisogno di altro perché ci servirà solo per creare il nostro primo 
# oggetto impostazioni, che sarà salvato con cPickle (vedremo in seguito come), 
# per poi essere modificato dal menù a seconda delle nostre esigenze.
#===============================================================================
class impostazioni():
    def __init__(self):
        self.larghezza_schermo = 640 # larghezza e altezza dllo schermo
        self.altezza_schermo = 480  
        self.full = False   # booleani per full schreen, acc hardware, ecc
        self.bool_hw = False
        self.bool_buff = False
        self.bool_opengl = False
        self.depth = 32 # altre impostazioni: freq, buffer ecc..
        self.frequenza = 44100
        self.dimensione = -16
        self.canali = 2
        self.buffer = 4096

class main_menu():
    #===========================================================================
    # Istanza ci serve per tenere conto se siamo nel menù, oppure nel menù opzioni. 
    # Memorizziamo poi screen ed ingame. Le variabili anim_push ed anim_push_bool 
    # servono per gestire le animazioni dei pulsanti, invece bool_ing e count_init
    # servono per tenere conto se siamo in gioco e se è la prima volta che inziamo 
    # a giocare.
    #===========================================================================
    def __init__(self, screen1, altezza_s, larghezza_s, ingame): #menu_opzioni, caricamento_gioco, salvataggio_gioco,inizio_gioco,screen)
        self.istanza = 0
        self.screen = screen1
        self.anim_push = 0
        self.anim_push_bool = False
        self.ing = ingame
        self.bool_ing = False
        self.count_init = False
        

#===============================================================================
# Apriamo il file impostazioni utilizzando cPickle e teniamo conto delle attuali 
# impostazioni per essere modificate memorizzandole in variabili omonime: 
# _Schermo_larghezza, _Schermo_altezza, _full, _bool_buff, _bool_hw e _bool_opengl. 
# Come potete notare gestiamo l’apertuare del file con le eccezioni, per ovviare 
# a problemi di apertura o chiusura file.
#===============================================================================
        try:
            stream = open("data/impostazioni.pkl", "r")
            pk = cPickle.Unpickler(stream)
            imp = pk.load()
            self._Schermo_larghezza = imp.larghezza_schermo
            self._Schermo_altezza = imp.altezza_schermo
            self._full = imp.full
            self._bool_buff = imp.bool_buff
            self._bool_hw = imp.bool_hw
            self._bool_opengl = imp.bool_opengl
            stream.close()

        except IOError:
            print ("Impossibile inizializzare Pygame")
            exit()


#===============================================================================
# Carichiamo sfondo di gioco e tutti i pulsanti del menù principale (comprese le 
# loro animazioni, ovvero i tasti premuti). Dimezziamo le coordinate dello schermo, 
# perché il nostro menù sarà sempre centrato, così da non portare complicazioni 
# con risoluzioni differenti (ed ecco spiegato perché il gioco si riavvia una 
# volta cambiate le impostazioni). Memorizziamo poi le zone dove dobbiamo gestire
# le collisioni, per creare le animazioni dei pulsanti e cliccare quindi su di essi. 
# Carichiamo il puntatore del mouse e l’audio del click, prenotando un canale per
# lui. Teniamo conto del tasto premuto attualmente, in questo caso si parte da 
# -1 perché il primo tasto, “Inizio”, sarà lo 0, mentre “Esci”, che è l’ultimo, 
# sarà il 4.
#===============================================================================
        ######
        # Menu
        self.Sfondo = pygame.image.load("data/Sfondo.jpg").convert()
        self.Sfondo = pygame.transform.scale(self.Sfondo, (self._Schermo_larghezza, self._Schermo_altezza))

        self.Continua = pygame.image.load("data/pulsanti/Continua.png").convert_alpha()
        self.Inizio = pygame.image.load("data/pulsanti/Inizio.png").convert_alpha()
        self.Carica = pygame.image.load("data/pulsanti/Carica.png").convert_alpha()
        self.Salva = pygame.image.load("data/pulsanti/Salva.png").convert_alpha()
        self.Opzioni = pygame.image.load("data/pulsanti/Opzioni.png").convert_alpha()
        self.Esci = pygame.image.load("data/pulsanti/Esci.png").convert_alpha()
        self.Continua_push = pygame.image.load("data/pulsanti/Continua_push.png").convert_alpha()
        self.Inizio_push = pygame.image.load("data/pulsanti/Inizio_push.png").convert_alpha()
        self.Carica_push = pygame.image.load("data/pulsanti/Carica_push.png").convert_alpha()
        self.Salva_push = pygame.image.load("data/pulsanti/Salva_push.png").convert_alpha()
        self.Opzioni_push = pygame.image.load("data/pulsanti/Opzioni_push.png").convert_alpha()
        self.Esci_push = pygame.image.load("data/pulsanti/Esci_push.png").convert_alpha()

        self.x = larghezza_s/2
        self.y = altezza_s/2

        self.Inizio_rect = pygame.Rect((self.x-48,self.y-24-48*2), (96,48))
        self.Carica_rect = pygame.Rect((self.x-48,self.y-24-48), (96,48))
        self.Salva_rect = pygame.Rect((self.x-48,self.y-24), (96,48))
        self.Opzioni_rect = pygame.Rect((self.x-48,self.y-24+48), (96,48))
        self.Esci_rect = pygame.Rect((self.x-48,self.y-24+48*2), (96,48))

        self.Puntatore = pygame.image.load("data/puntatore.png").convert_alpha()
        self.anim_punt = False
        self.audio_click = pygame.mixer.Sound("data/sound/beep-3.wav")
        self.canale_mouse = pygame.mixer.Channel(1)

        self.Premuto = -1
        self.Premuto_op = -1

        ##############
        # Menu Opzioni
        self._640 = pygame.image.load("data/pulsanti/640.png").convert_alpha()
        self._800 = pygame.image.load("data/pulsanti/800.png").convert_alpha()
        self._1024 = pygame.image.load("data/pulsanti/1024.png").convert_alpha()
        self._1280 = pygame.image.load("data/pulsanti/1280.png").convert_alpha()
        self._AccHw = pygame.image.load("data/pulsanti/AccHw.png").convert_alpha()
        self._OpenGl = pygame.image.load("data/pulsanti/Opengl.png").convert_alpha()
        self._DoppioBuff = pygame.image.load("data/pulsanti/DoppioBuff.png").convert_alpha()
        self._Indietro = pygame.image.load("data/pulsanti/Indietro.png").convert_alpha()
        self._Applica = pygame.image.load("data/pulsanti/Applica.png").convert_alpha()
        self._FullScreen = pygame.image.load("data/pulsanti/FullScreen.png").convert_alpha()
        self._640_push = pygame.image.load("data/pulsanti/640_push.png").convert_alpha()
        self._800_push = pygame.image.load("data/pulsanti/800_push.png").convert_alpha()
        self._1024_push = pygame.image.load("data/pulsanti/1024_push.png").convert_alpha()
        self._1280_push = pygame.image.load("data/pulsanti/1280_push.png").convert_alpha()
        self._AccHw_push = pygame.image.load("data/pulsanti/AccHw_push.png").convert_alpha()
        self._OpenGl_push = pygame.image.load("data/pulsanti/Opengl_push.png").convert_alpha()
        self._DoppioBuff_push = pygame.image.load("data/pulsanti/DoppioBuff_push.png").convert_alpha()
        self._Indietro_push = pygame.image.load("data/pulsanti/Indietro_push.png").convert_alpha()
        self._Applica_push = pygame.image.load("data/pulsanti/Applica_push.png").convert_alpha()
        self._FullScreen_push = pygame.image.load("data/pulsanti/FullScreen_push.png").convert_alpha()
        self._640_a = pygame.image.load("data/pulsanti/640_attivo.png").convert_alpha()
        self._800_a = pygame.image.load("data/pulsanti/800_attivo.png").convert_alpha()
        self._1024_a = pygame.image.load("data/pulsanti/1024_attivo.png").convert_alpha()
        self._1280_a = pygame.image.load("data/pulsanti/1280_attivo.png").convert_alpha()
        self._AccHw_a = pygame.image.load("data/pulsanti/AccHw_attiva.png").convert_alpha()
        self._OpenGl_a = pygame.image.load("data/pulsanti/Opengl_attiva.png").convert_alpha()
        self._DoppioBuff_a = pygame.image.load("data/pulsanti/DoppioBuff_attivo.png").convert_alpha()
        self._FullScreen_a = pygame.image.load("data/pulsanti/FullScreen_a.png").convert_alpha()

        self._640_rect = pygame.Rect((self.x-150,self.y-200), (96,48))
        self._800_rect = pygame.Rect((self.x+150-96,self.y-200), (96,48))
        self._1024_rect = pygame.Rect((self.x-150,self.y-150), (96,48))
        self._1280_rect = pygame.Rect((self.x+150-96,self.y-150), (96,48))
        self._AccHw_rect = pygame.Rect((self.x-150,self.y-50), (96,48))
        self._OpenGl_rect = pygame.Rect((self.x+150-96,self.y-50), (96,48))
        self._DoppioBuff_rect = pygame.Rect((self.x-150,self.y+25), (96,48))
        self._Indietro_rect = pygame.Rect((self.x-150,self.y+125), (96,48))
        self._Applica_rect = pygame.Rect((self.x+150-96,self.y+125), (96,48))
        self._FullScreen_rect = pygame.Rect((self.x+150-96,self.y+25), (96,48))

        self.rect_premere = [self.Inizio_rect, self.Carica_rect,self.Salva_rect, self.Opzioni_rect,self.Esci_rect]
        self.rect_premere_opzioni = [self._640_rect,self._800_rect,
self._1024_rect,self._1280_rect,
self._AccHw_rect,self._OpenGl_rect,
self._DoppioBuff_rect,self._Indietro_rect,
self._Applica_rect,self._FullScreen_rect]

    ##########################################
    # Funzione che gestisce le azioni nel menu
    def action(self,coordinate_mouse):
        if self.bool_ing == False:
            if self.canale_mouse.get_busy() != True:
                self.canale_mouse = self.audio_click.play()
            if self.istanza == 0:
                for x in range(0,len(self.rect_premere)):
                    if self.rect_premere[x].collidepoint(coordinate_mouse):
                        self.Premuto = x
                        self.anim_push_bool = True
            elif self.istanza == 1:
                for x in range(0,len(self.rect_premere_opzioni)):
                    if self.rect_premere_opzioni[x].collidepoint(coordinate_mouse):
                        self.Premuto_op = x
                        self.anim_push_bool = True

    ############################################
    # Funzione per muovere il personaggio ingame
    def action_p (self, stringa, num):
        if self.bool_ing == True:
            self.ing.giocatore.update(stringa,num)

    #########################################
    # Funzione per chiamare il menu da ingame
    def action_esc(self):
        if self.bool_ing == True:
            self.bool_ing = False
            self.istanza = 0
        else:
            self.bool_ing = True
            self.istanza = -1

    ####################################
    # Funzione per il salvataggio ingame
    def save_this(self):
        try:
            stream = open("data/save.pkl", "w")
            pk = cPickle.Pickler(stream)
            pk.dump(self.ing.giocatore.coordinate)
            stream.close()
            pk.clear_memo()
        except IOError:
            print ("Impossibile salvare il gioco")
            exit()

    ####################################
    # Funzione per il caricamento ingame
    def carica_this(self):
        try:
            stream = open("data/save.pkl", "r")
            pk = cPickle.Unpickler(stream)
            coord = pk.load()
            base = self.ing.base
            stream.close()
            personaggio = giocatore("27382_1174921384",48,32, coord, None)
            Ingame = ingame(personaggio, self.screen, base)
            self.ing = Ingame
        except IOError:
            print ("Nessun salvataggio presente")

    #################################
    # Funzione che gestisce il render
    def render(self,screen,temp,msxy):
        if self.bool_ing == True:
            self.ing.render()
            return

            screen.blit(self.Sfondo,(0,0))

        #############
        # Render Menu
        if self.istanza == 0:
                if self.Premuto == 0:
                    if self.count_init == False:
                        screen.blit(self.Inizio_push,(self.x-48,self.y-24-48*2-15))
                    else:
                        screen.blit(self.Continua_push,(self.x-48,self.y-24-48*2-15))
                else:
                    if self.count_init == False:
                        screen.blit(self.Inizio,(self.x-48,self.y-24-48*2-15))
                    else :
                        screen.blit(self.Continua,(self.x-48,self.y-24-48*2-15))
                if self.Premuto == 1:
                    screen.blit(self.Carica_push,(self.x-48,self.y-24-48-10))
                else:
                    screen.blit(self.Carica,(self.x-48,self.y-24-48-10))
                if self.Premuto == 2:
                    screen.blit(self.Salva_push,(self.x-48,self.y-24-5))
                else:
                    screen.blit(self.Salva,(self.x-48,self.y-24-5))
                if self.Premuto == 3:
                    screen.blit(self.Opzioni_push,(self.x-48,self.y-24+48+5))
                else:
                    screen.blit(self.Opzioni,(self.x-48,self.y-24+48+5))
                if self.Premuto == 4:
                    screen.blit(self.Esci_push,(self.x-48,self.y-24+48*2+10))
                else :
                    screen.blit(self.Esci,(self.x-48,self.y-24+48*2+10))

                if self.anim_push > 0.025 and self.Premuto == 4: # Esci
                    exit()
                elif self.anim_push > 0.030 and self.Premuto == 3: # Opzioni
                    self.Premuto = -1
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.istanza = 1
                    try:
                        stream = open("data/impostazioni.pkl", "r")
                        pk = cPickle.Unpickler(stream)
                        imp = pk.load()
                        self._Schermo_larghezza = imp.larghezza_schermo
                        self._Schermo_altezza = imp.altezza_schermo
                        self._full = imp.full
                        self._bool_buff = imp.bool_buff
                        self._bool_hw = imp.bool_hw
                        self._bool_opengl = imp.bool_opengl
                        stream.close()
                    except pygame.error,IOError:
                        print ("Impossibile inizializzare Pygame")
                        print (pygame.get_error())
                        exit()
                elif self.anim_push > 0.030 and self.Premuto == 2: # Salva
                    self.Premuto = -1
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.save_this()
                elif self.anim_push > 0.030 and self.Premuto == 1: # Carica
                    self.Premuto = -1
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.carica_this()
                elif self.anim_push > 0.030 and self.Premuto == 0: # Inizio
                    self.Premuto = -1
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.bool_ing = True
                    self.istanza = -1
                    self.count_init = True
                else :
                    if self.anim_push_bool == True:
                        self.anim_push += temp

                if self.anim_punt == False:
                    screen.blit(self.Puntatore,msxy)

        #####################
        # Render Menu Opzioni
        if self.istanza == 1:

            if self.Premuto_op == 0:
                screen.blit(self._640_push,(self.x-150,self.y-200))
            else:
                if self._Schermo_larghezza == 640 and self._Schermo_altezza == 480:
                    screen.blit(self._640_a,(self.x-150,self.y-200))
                else:
                    screen.blit(self._640,(self.x-150,self.y-200))

            if self.Premuto_op == 1:
                    screen.blit(self._800_push,(self.x+150-96,self.y-200))
            else:
                if self._Schermo_larghezza == 800 and self._Schermo_altezza == 600:
                    screen.blit(self._800_a,(self.x+150-96,self.y-200))
                else:
                    screen.blit(self._800,(self.x+150-96,self.y-200))

            if self.Premuto_op == 2:
                    screen.blit(self._1024_push,(self.x-150,self.y-150))
            else:
                if self._Schermo_larghezza == 1024 and self._Schermo_altezza == 768:
                    screen.blit(self._1024_a,(self.x-150,self.y-150))
                else:
                    screen.blit(self._1024,(self.x-150,self.y-150))

            if self.Premuto_op == 3:
                    screen.blit(self._1280_push,(self.x+150-96,self.y-150))
            else:
                if self._Schermo_larghezza == 1280 and self._Schermo_altezza == 1024:
                    screen.blit(self._1280_a,(self.x+150-96,self.y-150))
                else:
                    screen.blit(self._1280,(self.x+150-96,self.y-150))

            if self.Premuto_op == 4:
                    screen.blit(self._AccHw_push,(self.x-150,self.y-50))
            else:
                if self._bool_hw == True:
                    screen.blit(self._AccHw_a,(self.x-150,self.y-50))
                else:
                    screen.blit(self._AccHw,(self.x-150,self.y-50))

            if self.Premuto_op == 5:
                    screen.blit(self._OpenGl_push,(self.x+150-96,self.y-50))
            else:
                if self._bool_opengl == True:
                    screen.blit(self._OpenGl_a,(self.x+150-96,self.y-50))
                else:
                    screen.blit(self._OpenGl,(self.x+150-96,self.y-50))

            if self.Premuto_op == 6:
                    screen.blit(self._DoppioBuff_push,(self.x-150,self.y+25))
            else:
                if self._bool_buff == True:
                    screen.blit(self._DoppioBuff_a,(self.x-150,self.y+25))
                else:
                    screen.blit(self._DoppioBuff,(self.x-150,self.y+25))

            if self.Premuto_op == 7:
                    screen.blit(self._Indietro_push,(self.x-150,self.y+125))
            else:
                screen.blit(self._Indietro,(self.x-150,self.y+125))

            if self.Premuto_op == 8:
                    screen.blit(self._Applica_push,(self.x+150-96,self.y+125))
            else:
                screen.blit(self._Applica,(self.x+150-96,self.y+125))

            if self.Premuto_op == 9:
                screen.blit(self._FullScreen_push,(self.x+150-96,self.y+25))
            else:
                if self._full == True:
                        screen.blit(self._FullScreen_a,(self.x+150-96,self.y+25))
                else:
                    screen.blit(self._FullScreen,(self.x+150-96,self.y+25))

            #########################################################
            # Animazioni menu opzioni e cambiamenti impostazioni

            if self.anim_push > 0.030 and self.Premuto_op == 9: # FullScreen
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
                    if self._full == False:
                        self._full = True
                    else:
                        self._full = False
            elif self.anim_push > 0.030 and self.Premuto_op == 8: # Applica
                    aggiorna_imp( self._Schermo_larghezza, self._Schermo_altezza, self._full, self._bool_buff, self._bool_hw, self._bool_opengl)
                    pygame.quit()
                    run()
            elif self.anim_push > 0.030 and self.Premuto_op == 7: # Indietro
                    self.istanza = 0
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 6: # DoppioBuffer
                    if (self._bool_hw == True or self._bool_opengl == True) and self._bool_buff == False:
                        self._bool_buff = True
                    else:
                        self._bool_buff = False
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 5: # OpenGl
                    if self._bool_opengl == False and self._bool_hw == False:
                        self._bool_opengl = True
                    else:
                        self._bool_opengl = False
                        self._bool_buff = False
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 4: # AccHw
                    if self._bool_hw == False and self._bool_opengl == False:
                        self._bool_hw = True
                    else:
                        self._bool_hw = False
                        self._bool_buff = False
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 3: # 1280
                    self._Schermo_larghezza = 1280
                    self._Schermo_altezza = 1024
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 2: # 1024
                    self._Schermo_larghezza = 1024
                    self._Schermo_altezza = 768
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 1: # 800
                    self._Schermo_larghezza = 800
                    self._Schermo_altezza = 600
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            elif self.anim_push > 0.030 and self.Premuto_op == 0: #640
                    self._Schermo_larghezza = 640
                    self._Schermo_altezza = 480
                    self.anim_push = 0
                    self.anim_push_bool = False
                    self.Premuto_op = -1
            else :
                if self.anim_push_bool == True:
                    self.anim_push += temp

            if self.anim_punt == False:
                    screen.blit(self.Puntatore,msxy)

 
    #################################
#Funzione che gestisce gli eventi
def Eventi(event, Main):

    if event.type == QUIT:
        exit()

    tasti_premuti = pygame.key.get_pressed()
    pulsanti_mouse = pygame.mouse.get_pressed()

    if event.type == KEYDOWN :
        if tasti_premuti[K_ESCAPE]:
            Main.action_esc()
        elif tasti_premuti[K_LALT] and tasti_premuti[K_F4]:
            exit()
        elif tasti_premuti[K_DOWN]:
            Main.action_p("basso",0)
        elif tasti_premuti[K_UP]:
            Main.action_p("alto",12)
        elif tasti_premuti[K_RIGHT]:
            Main.action_p("destra",8)
        elif tasti_premuti[K_LEFT]:
            Main.action_p("sinistra",4)

    if event.type == MOUSEBUTTONDOWN:
        if pulsanti_mouse[0]==1:
            coordinate_mouse = pygame.mouse.get_pos()
            Main.action(coordinate_mouse)
 
def caricamento_imp():
    try:
        stream = open("data/impostazioni.pkl", "r")
        pk = cPickle.Unpickler(stream)
        imp = pk.load()
        stream.close()
        pygame.mixer.pre_init(imp.frequenza, imp.dimensione, imp.canali, imp.buffer)
        pygame.init()
        if imp.full == False and imp.bool_buff == False and imp.bool_hw == False and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo))
        elif imp.full == False and imp.bool_buff == False and imp.bool_hw == False and imp.bool_opengl == True:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),OPENGL,imp.depth)
        elif imp.full == False and imp.bool_buff == False and imp.bool_hw == True and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),HWSURFACE,imp.depth)
        elif imp.full == True and imp.bool_buff == False and imp.bool_hw == True and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),FULLSCREEN | HWSURFACE,imp.depth)
        elif imp.full == False and imp.bool_buff == True and imp.bool_hw == True and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),DOUBLEBUF | HWSURFACE,imp.depth)
        elif imp.full == True and imp.bool_buff == True and imp.bool_hw == True and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),FULLSCREEN | DOUBLEBUF | HWSURFACE,imp.depth)
        elif imp.full == True and imp.bool_buff == False and imp.bool_hw == False and imp.bool_opengl == False:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),FULLSCREEN,imp.depth)
        elif imp.full == True and imp.bool_buff == True and imp.bool_hw == False and imp.bool_opengl == True:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),FULLSCREEN | DOUBLEBUF | OPENGL,imp.depth)
        elif imp.full == False and imp.bool_buff == True and imp.bool_hw == False and imp.bool_opengl == True:
            screen = pygame.display.set_mode((imp.larghezza_schermo, imp.altezza_schermo),DOUBLEBUF | OPENGL,imp.depth)

        return screen

    except IOError:
        print ("Impossibile inizializzare Pygame")
        exit()
 
def salvataggio_imp():
    try:
        stream = open("data/impostazioni.pkl", "w")
        pk = cPickle.Pickler(stream)
        imp = impostazioni()
        pk.dump(imp)
        stream.close()
        pk.clear_memo()
        
    except IOError:
        print ("Impossibile creare file di configurazione")
        exit()
 
def aggiorna_imp(w,h,full,buff,hw,opengl):
    try:
        stream = open("data/impostazioni.pkl", "w")
        pk = cPickle.Pickler(stream)
        imp = impostazioni()
        imp.larghezza_schermo = w
        imp.altezza_schermo = h
        imp.full = full
        imp.bool_hw = hw
        imp.bool_buff = buff
        imp.bool_opengl = opengl
        pk.dump(imp)
        stream.close()
        pk.clear_memo()

    except IOError:
        print ("Impossibile creare file di configurazione")
        exit()
 
def run():
    try:
        stream = open("data/impostazioni.pkl", "r")
    except IOError:
        salvataggio_imp()

    Schermo = caricamento_imp()
    Altezza_s = Schermo.get_height()
    Larghezza_s = Schermo.get_width()
    pygame.mouse.set_visible(False)

    sfondo_erba = pygame.image.load("data/grass3_cyc.jpg").convert()
    sfondo_erba_scalato = pygame.transform.scale(sfondo_erba, (Larghezza_s,Altezza_s))
    personaggio = giocatore("27382_1174921384",48,32, (320,240), None)

    global fps
    global orologio
    global tempo_passato
    global speed

    speed = 30.0
    orologio = pygame.time.Clock()
    fps = 60

    Ingame = ingame(personaggio, Schermo, sfondo_erba_scalato)
    Main = main_menu(Schermo, Altezza_s, Larghezza_s, Ingame)

    pygame.key.set_repeat(100, 30)

    while (True):
        for event in pygame.event.get():
            Eventi(event,Main)

        tempo_passato = tps(orologio,fps)
        mouse_x_y = pygame.mouse.get_pos()

        Main.render(Schermo,tempo_passato,mouse_x_y)

        pygame.display.flip()

if __name__ == "__main__":
    run()

