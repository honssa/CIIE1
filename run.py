import pygame
from escena import Escena
from director import Director
from main_menu.main_menu import MainMenu
from game import Game
from levels.level import Level1

if __name__ == "__main__":
    pygame.init()

    #crear director
    director=Director()
    #crear escena inicial, apilar y ejecutar
    escena=MainMenu(director)
    director.apilarEscena(escena)
    director.ejecutar()
    
    pygame.quit()
