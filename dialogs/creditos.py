import pygame
import os
from escena import Escena

def draw_text(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = POS
    window.blit(text_surf, text_rect)

class Creditos(Escena):
    def __init__(self, director):
        self.director=director
        self.s_width=self.director.win.get_width()
        self.s_height=self.director.win.get_height()

        self.textos = []
        self.textos.append("Autores:")
        self.textos.append("Nicolas Martinez Gonzalez")
        self.textos.append("Angel Lagares Vazquez")
        self.textos.append("G. Xoel Otero Gonzalez")
        self.textos.append("Ivan Folgueira Cabado")
        self.textos.append("Alberto Peteiro Gandara")
        self.textos.append("sprites:")
        self.textos.append("Buch")
        self.textos.append("Ansimuz")
        self.textos.append("Penusbmic")
        self.textos.append("Mikiz")
        self.textos.append("Kronovi")
        self.textos.append("Quintino")
        self.textos.append("Vaca Roxa")

        self.textos.append("musica e sons:")
        self.textos.append("Starlik")
        self.textos.append("Luke.RUSTLD")
        self.textos.append("Kenney")
        self.textos.append("CelestialGhost8")
        self.textos.append("Matthew Pablo")
        self.textos.append("Alexander Zhelanov")
        self.textos.append("Qubodup")
        self.textos.append("Iwan Gabovitch")
        self.textos.append("Jalastram")
        self.textos.append("Remaxim")
        self.textos.append("Bertsz")
        self.textos.append("Demberz")
        self.textos.append("Michel Baradari")
        self.textos.append("Telaron")
        self.textos.append("Ansimuz")
        self.textos.append("Realizado para a asignatura de Contornos Inmersivos e de entretemento")
        self.textos.append("Facultade de informatica de A Coruña")

        FONT_PIXEL = 'Assets/fonts/KnoxFont.ttf'
        self.PIXEL_TEXT = pygame.font.Font(FONT_PIXEL, 16)

        self.indice_texto = 0   # Contador que di canto texto falta por ensinar
        self.textos_en_pantalla = []
        self.counter_spawn = 0
        self.final = False
        
        
        
    def update(self, *args):
        pass
        
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                from main_menu.main_menu import MainMenu
                from dialogs.secreta import Secreta
                if self.director.trigger_secreta:
                    self.director.cambiarEscena(Secreta(self.director))
                else:
                    self.director.cambiarEscena(MainMenu(self.director))


                
                
    def dibujar(self, win):
        win.fill((0,0,0))
        for texto in self.textos_en_pantalla:
            draw_text(texto[0], self.PIXEL_TEXT, (191,228,230), (self.s_width//2, texto[1]), win)
            texto[1] -= 1
            if texto[1] <= -10:
                self.textos_en_pantalla.remove(texto)
        
        self.counter_spawn += 1
        if self.counter_spawn >= 120: # Cada dous segundos spawnea novo texto
            if self.indice_texto < len(self.textos):
                self.textos_en_pantalla.append([self.textos[self.indice_texto], self.s_height])
                self.counter_spawn = 0
                self.indice_texto += 1
        
        if self.indice_texto >= len(self.textos) and self.counter_spawn >= 780:
            draw_text("Grazas por xogar", self.PIXEL_TEXT, (191,228,230), (self.s_width//2, self.s_height//2), win)

        if self.indice_texto >= len(self.textos) and self.counter_spawn >= 840:
            self.final = True
            draw_text("(Prema click esquerdo para sair dos creditos)", self.PIXEL_TEXT, (191,228,230), (self.s_width//2, self.s_height//2 + 32), win)
