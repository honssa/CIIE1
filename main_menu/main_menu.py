import pygame
import os
from escena import Escena
from selection import Seleccion

def divide_imagen(image, rect):
    subimage = image.subsurface(rect)
    return subimage, rect



class MainMenu(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.width=director.win.get_width()
        self.height=director.win.get_height()

        self.titulo = pygame.image.load(os.path.join("Assets/main_menu", "titulo.png")).convert_alpha()
        self.pos_titulo = (103,30)
        self.btn_creditos = pygame.image.load(os.path.join("Assets/main_menu", "btn_creditos.png")).convert_alpha()
        self.btn_nova_partida = pygame.image.load(os.path.join("Assets/main_menu", "btn_nova_partida.png")).convert_alpha()
        self.btn_sair = pygame.image.load(os.path.join("Assets/main_menu", "btn_sair.png")).convert_alpha()
        self.pos_btn_creditos = (552,588)
        self.pos_btn_nova_partida = (80,588)
        self.pos_btn_sair = (1046,588)

        self.btn_hover = pygame.image.load(os.path.join("Assets/main_menu", "hover_final.png")).convert_alpha()

        self.cursor_pos = (0,0)

        self.hover = 0 # 1 : nova partida // 2 : creditos // 3: sair
        self.limites = (30,80) # limites onde oscila o titulo
        self.desplazamento = 0
        self.sentido = 1
        self.contador_tempo = 0
        self.tiras = []
        start_sound = pygame.mixer.Sound("Sounds/novos/start_menu_telaron.ogg")
        start_sound.set_volume(0.5)
        start_sound.play()
        for x in range(0, self.titulo.get_height()):
            subimage, rect = divide_imagen(self.titulo, pygame.Rect((0,x) ,(self.titulo.get_width(),1) ))
            self.tiras.append(subimage)



    def update(self, tiempo):
        self.cursor_pos = pygame.mouse.get_pos()
        if self.cursor_pos[0] > self.pos_btn_nova_partida[0] and self.cursor_pos[1] > self.pos_btn_nova_partida[1] and \
            self.cursor_pos[0] < (self.pos_btn_nova_partida[0] + self.btn_nova_partida.get_width()) and \
                self.cursor_pos[1] < (self.pos_btn_nova_partida[1] + self.btn_nova_partida.get_height()):
            self.hover = 1
        
        elif self.cursor_pos[0] > self.pos_btn_creditos[0] and self.cursor_pos[1] > self.pos_btn_creditos[1] and \
            self.cursor_pos[0] < (self.pos_btn_creditos[0] + self.btn_creditos.get_width()) and \
                self.cursor_pos[1] < (self.pos_btn_creditos[1] + self.btn_creditos.get_height()):
            self.hover = 2

        elif self.cursor_pos[0] > self.pos_btn_sair[0] and self.cursor_pos[1] > self.pos_btn_sair[1] and \
            self.cursor_pos[0] < (self.pos_btn_sair[0] + self.btn_sair.get_width()) and \
                self.cursor_pos[1] < (self.pos_btn_sair[1] + self.btn_sair.get_height()):
            self.hover = 3    
        
        else:
            self.hover = 0



    def eventos(self, lista_eventos):
            for event in lista_eventos:
                self.cursor_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    self.director.salirPrograma()

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if self.hover == 1:
                        from dialogs.intro import Intro
                        pygame.mixer.stop()
                        self.director.trigger_secreta = True
                        self.director.cambiarEscena(Intro(self.director))
                    
                    elif self.hover == 2:
                        pygame.mixer.stop()
                        from dialogs.creditos import Creditos
                        self.director.cambiarEscena(Creditos(self.director))

                    elif self.hover == 3:
                        pygame.mixer.stop()
                        self.director.salirPrograma()

            self.dibujar(self.director.win)



    def dibujar(self, win):
        win.fill((0,0,0))
        
        win.blit(self.btn_nova_partida, self.pos_btn_nova_partida)
        win.blit(self.btn_creditos, self.pos_btn_creditos)
        win.blit(self.btn_sair, self.pos_btn_sair)

        self.contador_tempo += 1
        if self.contador_tempo == 6:
            self.desplazamento += self.sentido
            if self.desplazamento >= self.limites[1]:
                self.sentido = -1
            elif self.desplazamento <= self.limites[0]:
                self.sentido = 1
            self.contador_tempo = 0

        for i in range(len(self.tiras)):
            win.blit(self.tiras[i], (self.pos_titulo[0], self.pos_titulo[1] + i + self.desplazamento) )

        if self.hover == 1:
            win.blit(self.btn_hover, (self.pos_btn_nova_partida[0]-40, self.pos_btn_nova_partida[1]-40) )
        elif self.hover == 2:
            win.blit(self.btn_hover, (self.pos_btn_creditos[0]-80, self.pos_btn_creditos[1]-40) )
        elif self.hover == 3:
            win.blit(self.btn_hover, (self.pos_btn_sair[0]-130, self.pos_btn_sair[1]-40) )