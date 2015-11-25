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

class main_menu():
    def __init__(self, screen1, altezza_s, larghezza_s, ingame): #menu_opzioni, caricamento_gioco, salvataggio_gioco,inizio_gioco,screen)
        self.istanza = 0
        self.screen = screen1
        self.anim_push = 0
        self.anim_push_bool = False
        self.ing = ingame
        self.bool_ing = False
        self.count_init = False

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
