import pygame
from escena import Escena
from dialogs.creditos import Creditos
import os



def draw_text_2(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = (POS[0] + text_rect.width//2, POS[1]) 
    window.blit(text_surf, text_rect)



class Cinematica(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        w=director.win.get_width()
        h=director.win.get_height()
        self.finDialogo=False
        letra_px = 'Assets/fonts/Avenixel-Regular.ttf'
        self.fuente = pygame.font.Font(letra_px, int(27))
        self.fonte_grande = pygame.font.Font(letra_px, int(54))
        self.bg= pygame.transform.scale(pygame.image.load(os.path.join("Assets/cinematicas","primeira.png")), (820,474)).convert_alpha()
        self.bg2= pygame.transform.scale(pygame.image.load(os.path.join("Assets/cinematicas","segunda.png")), (820,474)).convert_alpha()
        self.final_sound = pygame.mixer.Sound("Sounds/novos/final_scene_subspace.ogg")
        self.final_sound.set_volume(0.5)
        self.final_sound.play()

        #print(self.bg)
        
        # Cadro de dialogo
        self.cadro_dialogo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","cadro_dialogo.png")),(w, h)).convert_alpha()
        self.cadro_dialogo2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","cadro_dialogo_2.png")),(w, h)).convert_alpha()
        
        # PORTRAITS
        self.portrait_chema = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","chema.png")),(272, 272)).convert_alpha()
        self.portrait_olen = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","olen.png")),(272, 272)).convert_alpha()
        self.portrait_rock = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","rock.png")),(272, 272)).convert_alpha()
        self.portrait_paper = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","paper.png")),(272, 272)).convert_alpha()
        
        ## Dialogo inicial
        self.dialogo_cinematica = []	# Pequenas variacions entre comandantes
        self.dialogo_cinematica.append(("Este e o final do camiño, Chema, non podes parar o progreso", 4))
        self.dialogo_cinematica.append(("mirate.. un loitador coma ti, nestas condicions, a vellez de seguro que e unha miseria non si?", 4))
        self.dialogo_cinematica.append(("... Aforra o teu discurso, non sei como te puideche colar aqui dentro", 0))
        self.dialogo_cinematica.append(("Hahaha Chema eu son mais vello ca ti e mirame... debichete unir a min, esta guerra xa estaria mais que acabada e vivirias ben durente moitos anos", 4))
        self.dialogo_cinematica.append(("Non era ese o meu destino, eu sirvo a resistencia, son un soldado. Se ves matarme aforra as tuas palabras non che vou entreter mais", 0))
        self.dialogo_cinematica.append(("Descansa eternamente pois...", 4))
        
        ## TRANSICION A NEGRO E SONA UN DISPARO (PRIMEIRA INTERRUPCION)
        
        ## Dialogo cando rock aparece
        self.dialogo_cinematica2 = []
        self.dialogo_cinematica2.append(("Oh no... SEÑOR!",1))
        self.dialogo_cinematica2.append(("...",4))
        self.dialogo_cinematica2.append(("..!!!",1))
        self.dialogo_cinematica2.append(("Acabas de cometer o peor erro da tua vida...",4))
        self.dialogo_cinematica2.append(("despidete",4))
        
        ## SONIDO DE RECEPTOR DE OLEN (SEGUNDA INTERRUPCION)
        
        self.dialogo_cinematica3 = []
        self.dialogo_cinematica3.append(("(Que poderia ser agora...)",4))
        self.dialogo_cinematica3.append(("*Chik *Chik",4))
        self.dialogo_cinematica3.append(("Ola? Aqui o xeneral Olen, que esta acontecendo?",4))
        self.dialogo_cinematica3.append(("Como? Estan asoballando as liñas de cerco os reforzos da resistencia, pero senon avistaran ningun movemento en semanas..",4))
        self.dialogo_cinematica3.append(("Esta ben vou inmediatamente... *Chik Chik",4))
        self.dialogo_cinematica3.append(("Non teño tempo para enfrentarme a ti agora, Pero mellor sera que te afastes senon queres acabar igual",4))
        
        ## OLEN VAISE, SONA O RECEPTOR DE CHEMA, ROCK ACHEGASE E O COLLE (TERCEIRA INTERRUPCION)
        
        self.dialogo_cinematica4 = []
        self.dialogo_cinematica4.append(("...",1))
        self.dialogo_cinematica4.append(("foise... maldito",1))
        self.dialogo_cinematica4.append(("reforzos? Eso e mais ben imposible...",1))
        self.dialogo_cinematica4.append(("Que? Esta soando o receptor do señor Jenkins, debo collelo",1))
        self.dialogo_cinematica4.append(("*Chik *Chik",1))
        self.dialogo_cinematica4.append(("...",1))
        self.dialogo_cinematica4.append(("Señor Jenkins, ten que sair de ali inmediatamente, Olen Skum acabase de infiltrar no forte, quedan poucos minutos",2))
        self.dialogo_cinematica4.append(("Chegas tarde... podese saber onde diaños estas, Paper?",1))
        self.dialogo_cinematica4.append(("... merda",2))
        self.dialogo_cinematica4.append(("Non teño tempo para dar explicacions, estanme perseguindo, se todo sae ben comunicareime contigo ou con Scissors, pero evacuade inmediatamente",2))
        self.dialogo_cinematica4.append(("(... colgou)",1))
        self.dialogo_cinematica4.append(("(levareime o seu corpo)",1))
        self.dialogo_cinematica4.append(("(xuro que matarei a ese miserable de Olen Skum)",1))
        
        ## TRANSICION A NEGRO E ENTRA A ESCENA DE CREDITOS
        self.dialogos = []
        self.quen_fala = [] #personaxe  # 0: Chema // 1: Rock // 2: Paper // 3 Scissors // 4: Olen // 5: ??? (Ludwig)

        self.dialogos2 = []
        self.quen_fala2 = []

        self.dialogos3 = []
        self.quen_fala3 = []

        self.dialogos4 = []
        self.quen_fala4 = []
        
        for dialogo in self.dialogo_cinematica:
            self.dialogos.append(dialogo[0])
            self.quen_fala.append(dialogo[1])

        for dialogox in self.dialogo_cinematica2:
            self.dialogos2.append(dialogox[0])
            self.quen_fala2.append(dialogox[1])

        for dialogoxx in self.dialogo_cinematica3:
            self.dialogos3.append(dialogoxx[0])
            self.quen_fala3.append(dialogoxx[1])
        
        for dialogoxxx in self.dialogo_cinematica4:
            self.dialogos4.append(dialogoxxx[0])
            self.quen_fala4.append(dialogoxxx[1])
        #print("DIALOGO 2: " + str(self.dialogos2))

        
        ## VARIABLES DE IVAN
        self.MAX_DIALOG = []    # Cantos dialogos hai en cada conversacion
        self.MAX_DIALOG.append(len(self.dialogo_cinematica))
        self.MAX_DIALOG.append(len(self.dialogo_cinematica2))
        self.MAX_DIALOG.append(len(self.dialogo_cinematica3))
        self.MAX_DIALOG.append(len(self.dialogo_cinematica4))
        self.num=0 
        self.aux=""
        self.i=0


        # Variable de estados
        # 0 : Olen conversa con Chema
        # 1 : transicion a negro e disparo (INTERRUPCION 1)
        # 2 : Aparece Rock e conversa con Olen
        # 3 : Chaman a Olen (INTERRUPCION 2)
        # 4 : Conversacion Olen con alguen
        # 5 : Olen vaise, sona o receptor de chema, rock achegase e o colle (INTERRUPCION 3)
        # 6 : Rock conversa con Paper   
        self.state = 0
        self.frame_counter = 0
        self.TEMPO_TRANSICION_1_2 = 240
        self.TEMPO_TRANSICION_3_4 = 300
        self.TEMPO_TRANSICION_5_6 = 120
        self.chema_ring = True 
        



    def update(self, tiempo):
        pass
        
        
        
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            # Transicion do estado 0 ao 1
            if self.num>=self.MAX_DIALOG[0]-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.state == 0:
                self.state = 1
                self.final_sound.stop()
                pygame.mixer.Sound("Sounds/powerful_shot.ogg").play()
                self.num = 0
                self.aux=""
                self.i=0
            # Transicion do estado 2 ao 3 (interrupcion do telefono de Olen)
            elif self.num>=self.MAX_DIALOG[1]-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.state == 2:
                self.state = 3
                pygame.mixer.Sound("Sounds/olen_receptor.ogg").play()
                self.num = 0
                self.aux=""
                self.i=0

            elif self.num>=self.MAX_DIALOG[2]-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.state == 4:
                self.state = 5
                self.num = 0
                self.aux=""
                self.i=0

            elif self.num>=self.MAX_DIALOG[3]-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.state == 6:
                escena = Creditos(self.director)
                self.director.cambiarEscena(escena)
            #	pygame.mixer.stop()
            #	escena = Seleccion(self.director, 3)
            #	self.director.cambiarEscena(escena)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.finDialogo==True and (self.state == 0 or self.state == 2 or self.state == 4 or self.state == 6):
                self.num+=1
                self.i=0
                self.aux=""
                self.finDialogo=False
                
                
                
                
    def dibujar(self, win):
        win.fill((0,0,0))
        #win.blit(self.bg, (250,-10))
        
        #win.blit(self.p_bg, self.pos_bg)
        
        if self.state == 0:
            win.blit(self.bg, (250,-10))
            if self.num >= len(self.quen_fala):
                pass
            elif self.quen_fala[self.num] == 0: # Fala chema
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_chema, (50,378))
                draw_text_2("CHEMA JENKINS", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala[self.num] == 1: # Fala rock
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_rock, (50,378))
                draw_text_2("ROCK", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala[self.num] == 2: # Fala paper
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_paper, (50,378))
                draw_text_2("PAPER", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala[self.num] == 4: # Fala olen
                win.blit(self.cadro_dialogo2, (0,0))
                win.blit(self.portrait_olen, (50,378))
                draw_text_2("OLEN SKUM", self.fonte_grande, (255,255,255), (330,480), win)
            
            
            if not (self.num>=self.MAX_DIALOG[0]-1):
                textoEntradaSize=len(self.dialogos[self.num])
            else:
                self.num = self.MAX_DIALOG[0]-1
                textoEntradaSize=len(self.dialogos[self.num])
            
            if self.i<textoEntradaSize:
                self.aux+=self.dialogos[self.num][self.i]
                self.i+=1
            else:
                self.finDialogo=True
            
            self.blit_text(win, (330, 505), self.fuente)
        
        elif self.state == 1:
            self.frame_counter += 1
            if self.frame_counter > self.TEMPO_TRANSICION_1_2:
                self.frame_counter = 0
                self.state = 2

        elif self.state == 2:
            win.blit(self.bg2, (250,-10))

            if self.num >= len(self.quen_fala2):
                pass
            elif self.quen_fala2[self.num] == 0: # Fala chema
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_chema, (50,378))
                draw_text_2("CHEMA JENKINS", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala2[self.num] == 1: # Fala rock
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_rock, (50,378))
                draw_text_2("ROCK", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala2[self.num] == 2: # Fala paper
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_paper, (50,378))
                draw_text_2("PAPER", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala2[self.num] == 4: # Fala olen
                win.blit(self.cadro_dialogo2, (0,0))
                win.blit(self.portrait_olen, (50,378))
                draw_text_2("OLEN SKUM", self.fonte_grande, (255,255,255), (330,480), win)
            
            
            if not (self.num>=self.MAX_DIALOG[1]-1):
                textoEntradaSize=len(self.dialogos2[self.num])
            else:
                self.num = self.MAX_DIALOG[1]-1
                textoEntradaSize=len(self.dialogos2[self.num])
            
            if self.i<textoEntradaSize:
                self.aux+=self.dialogos2[self.num][self.i]
                self.i+=1
            else:
                self.finDialogo=True
            
            self.blit_text(win, (330, 505), self.fuente)
        

        elif self.state == 3:
            win.blit(self.bg2, (250,-10))
            self.frame_counter += 1
            if self.frame_counter > self.TEMPO_TRANSICION_3_4:
                self.frame_counter = 0
                self.state = 4
            #print("en construccion")
        

        elif self.state == 4:
            win.blit(self.bg2, (250,-10))

            if self.num >= len(self.quen_fala3):
                pass
            elif self.quen_fala3[self.num] == 0: # Fala chema
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_chema, (50,378))
                draw_text_2("CHEMA JENKINS", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala3[self.num] == 1: # Fala rock
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_rock, (50,378))
                draw_text_2("ROCK", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala3[self.num] == 2: # Fala paper
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_paper, (50,378))
                draw_text_2("PAPER", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala3[self.num] == 4: # Fala olen
                win.blit(self.cadro_dialogo2, (0,0))
                win.blit(self.portrait_olen, (50,378))
                draw_text_2("OLEN SKUM", self.fonte_grande, (255,255,255), (330,480), win)
            
            
            if not (self.num>=self.MAX_DIALOG[2]-1):
                textoEntradaSize=len(self.dialogos3[self.num])
            else:
                self.num = self.MAX_DIALOG[2]-1
                textoEntradaSize=len(self.dialogos3[self.num])
            
            if self.i<textoEntradaSize:
                self.aux+=self.dialogos3[self.num][self.i]
                self.i+=1
            else:
                self.finDialogo=True
            
            self.blit_text(win, (330, 505), self.fuente)
        

        elif self.state == 5:
            self.frame_counter += 1
            if self.frame_counter > self.TEMPO_TRANSICION_5_6:
                self.frame_counter = 0
                self.state = 6


        elif self.state == 6:
            if self.num >= len(self.quen_fala4):
                pass
            elif self.quen_fala4[self.num] == 0: # Fala chema
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_chema, (50,378))
                draw_text_2("CHEMA JENKINS", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala4[self.num] == 1: # Fala rock
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_rock, (50,378))
                draw_text_2("ROCK", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala4[self.num] == 2: # Fala paper
                win.blit(self.cadro_dialogo, (0,0))
                win.blit(self.portrait_paper, (50,378))
                draw_text_2("PAPER", self.fonte_grande, (255,255,255), (330,480), win)
            elif self.quen_fala4[self.num] == 4: # Fala olen
                win.blit(self.cadro_dialogo2, (0,0))
                win.blit(self.portrait_olen, (50,378))
                draw_text_2("OLEN SKUM", self.fonte_grande, (255,255,255), (330,480), win)
            
            if self.num == 3 and self.chema_ring:
                pygame.mixer.Sound("Sounds/chema_receptor.ogg").play()
                self.chema_ring = False
            elif self.num > 3 and (not self.chema_ring):
                pygame.mixer.stop()
                self.chema_ring = True

            

            
            if not (self.num>=self.MAX_DIALOG[3]-1):
                textoEntradaSize=len(self.dialogos4[self.num])
            else:
                self.num = self.MAX_DIALOG[3]-1
                textoEntradaSize=len(self.dialogos4[self.num])
            
            if self.i<textoEntradaSize:
                self.aux+=self.dialogos4[self.num][self.i]
                self.i+=1
            else:
                self.finDialogo=True
            
            self.blit_text(win, (330, 505), self.fuente)
        
        
        
    def blit_text(self, surface, pos, font, color=pygame.Color('white')):
        words = [word.split(' ') for word in self.aux.splitlines()]
        space = font.size(' ')[0]
        max_width = surface.get_width()-75
        max_height = surface.get_height()-75
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height  