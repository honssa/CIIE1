import pygame
from escena import Escena
from main_menu.main_menu import MainMenu

MATTE_BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (33, 150, 243)
LIGHT_BLUE = (0, 191, 255)

FONT_LIGHT = 'Assets/fonts/OpenSans-Light.ttf'
FONT_BOLD = 'Assets/fonts/OpenSans-SemiBold.ttf'


class PauseMenu(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.window = pygame.display.get_surface()
        self.width, self.height = self.window.get_size()
        self.pause = True
        self.btn_pressed = 0
        self.init_bg = 0

        self.MENU_TEXT = pygame.font.Font(FONT_LIGHT, int(110/1080 * self.height))
        self.SMALL_TEXT = pygame.font.Font(FONT_BOLD, int(25/1440 * self.width))

        BUTTON_WIDTH = int(self.width * 0.625 // 3)
        BUTTON_HEIGHT = int(self.height * 5 // 81)
        button_x_start = (self.width - BUTTON_WIDTH) // 2
        self.button_layout_4 = [(button_x_start, self.height * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, self.height * 6 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, self.height * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, self.height * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.background.fill((*MATTE_BLACK, 160))


        self.text_surf1, self.text_rect1 = self.text_objects('C O N T I N U A R', self.SMALL_TEXT, colour=WHITE)
        self.text_surf2, self.text_rect2 = self.text_objects('M E N U  P R I N C I P A L', self.SMALL_TEXT, colour=WHITE)
        #self.text_surf3, self.text_rect3 = self.text_objects('O P C I O N S', self.SMALL_TEXT, colour=WHITE)
        self.text_surf4, self.text_rect4 = self.text_objects('S A I R  D O  X O G O', self.SMALL_TEXT, colour=WHITE)

        self.text_rect1.center = (int(self.button_layout_4[0][0]+self.button_layout_4[0][2]/2), int(self.button_layout_4[0][1]+self.button_layout_4[0][3]/2))
        self.text_rect2.center = (int(self.button_layout_4[1][0]+self.button_layout_4[1][2]/2), int(self.button_layout_4[1][1]+self.button_layout_4[1][3]/2))
        #self.text_rect3.center = (int(self.button_layout_4[2][0]+self.button_layout_4[2][2]/2), int(self.button_layout_4[2][1]+self.button_layout_4[2][3]/2))
        self.text_rect4.center = (int(self.button_layout_4[3][0]+self.button_layout_4[3][2]/2), int(self.button_layout_4[3][1]+self.button_layout_4[3][3]/2))

        pygame.mixer.music.stop()
        pygame.mixer.Sound("Sounds/novos/pause_menu_Iwangabovitch.ogg").play(-1)

        #pygame.mixer.Sound("Sounds/b423b42.wav").play()

	
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:    # Esto esta mal
                if self.btn_pressed == 1:
                    pygame.mixer.stop()
                    pygame.mixer.music.load("Sounds/novos/Background_theme_starlik.ogg")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    #pygame.mixer.music.play()
                    self.director.salirEscena()
                elif self.btn_pressed == 2:
                    pygame.mixer.stop()
                    self.director.cambiarEscena(MainMenu(self.director))
                #elif self.btn_pressed == 3:
                #    pass
                elif self.btn_pressed == 4:
                    pygame.mixer.stop()
                    self.director.salirPrograma()


    def update(self, tiempo):
        # Verificas que boton esta en hover
        mouse = pygame.mouse.get_pos()
        if self.button_layout_4[0][0] < mouse[0] < self.button_layout_4[0][0] + self.button_layout_4[0][2] and self.button_layout_4[0][1] < mouse[1] < self.button_layout_4[0][1] + self.button_layout_4[0][3]: 
            self.btn_pressed = 1
        elif self.button_layout_4[1][0] < mouse[0] < self.button_layout_4[1][0] + self.button_layout_4[0][2] and self.button_layout_4[1][1] < mouse[1] < self.button_layout_4[1][1] + self.button_layout_4[0][3]: 
            self.btn_pressed = 2
        #elif self.button_layout_4[2][0] < mouse[0] < self.button_layout_4[2][0] + self.button_layout_4[0][2] and self.button_layout_4[2][1] < mouse[1] < self.button_layout_4[2][1] + self.button_layout_4[0][3]: 
        #    self.btn_pressed = 3
        elif self.button_layout_4[3][0] < mouse[0] < self.button_layout_4[3][0] + self.button_layout_4[0][2] and self.button_layout_4[3][1] < mouse[1] < self.button_layout_4[3][1] + self.button_layout_4[0][3]: 
            self.btn_pressed = 4
        else:
            self.btn_pressed = 0



	
    def dibujar(self, window):
        if not self.init_bg:
            self.pause_menu_setup(self.background, window)
            self.init_bg = 1

        window.blit(self.background, (0,0))
        text_surf, text_rect = self.text_objects('Menu de Pausa', self.MENU_TEXT, colour = WHITE)
        text_rect.center = ((self.width // 2), (self.height // 4))
        window.blit(text_surf, text_rect)

        if self.btn_pressed == 1:
            pygame.draw.rect(window, LIGHT_BLUE, (self.button_layout_4[0][0], self.button_layout_4[0][1], self.button_layout_4[0][2], self.button_layout_4[0][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[1][0], self.button_layout_4[1][1], self.button_layout_4[1][2], self.button_layout_4[1][3]))
            #pygame.draw.rect(window, BLUE, (self.button_layout_4[2][0], self.button_layout_4[2][1], self.button_layout_4[2][2], self.button_layout_4[2][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[3][0], self.button_layout_4[3][1], self.button_layout_4[3][2], self.button_layout_4[3][3]))
        elif self.btn_pressed == 2:
            pygame.draw.rect(window, BLUE, (self.button_layout_4[0][0], self.button_layout_4[0][1], self.button_layout_4[0][2], self.button_layout_4[0][3]))
            pygame.draw.rect(window, LIGHT_BLUE, (self.button_layout_4[1][0], self.button_layout_4[1][1], self.button_layout_4[1][2], self.button_layout_4[1][3]))
            #pygame.draw.rect(window, BLUE, (self.button_layout_4[2][0], self.button_layout_4[2][1], self.button_layout_4[2][2], self.button_layout_4[2][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[3][0], self.button_layout_4[3][1], self.button_layout_4[3][2], self.button_layout_4[3][3]))
        elif self.btn_pressed == 3:
            pygame.draw.rect(window, BLUE, (self.button_layout_4[0][0], self.button_layout_4[0][1], self.button_layout_4[0][2], self.button_layout_4[0][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[1][0], self.button_layout_4[1][1], self.button_layout_4[1][2], self.button_layout_4[1][3]))
            #pygame.draw.rect(window, LIGHT_BLUE, (self.button_layout_4[2][0], self.button_layout_4[2][1], self.button_layout_4[2][2], self.button_layout_4[2][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[3][0], self.button_layout_4[3][1], self.button_layout_4[3][2], self.button_layout_4[3][3]))
        elif self.btn_pressed == 4:
            pygame.draw.rect(window, BLUE, (self.button_layout_4[0][0], self.button_layout_4[0][1], self.button_layout_4[0][2], self.button_layout_4[0][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[1][0], self.button_layout_4[1][1], self.button_layout_4[1][2], self.button_layout_4[1][3]))
            #pygame.draw.rect(window, BLUE, (self.button_layout_4[2][0], self.button_layout_4[2][1], self.button_layout_4[2][2], self.button_layout_4[2][3]))
            pygame.draw.rect(window, LIGHT_BLUE, (self.button_layout_4[3][0], self.button_layout_4[3][1], self.button_layout_4[3][2], self.button_layout_4[3][3]))
        else:
            pygame.draw.rect(window, BLUE, (self.button_layout_4[0][0], self.button_layout_4[0][1], self.button_layout_4[0][2], self.button_layout_4[0][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[1][0], self.button_layout_4[1][1], self.button_layout_4[1][2], self.button_layout_4[1][3]))
            #pygame.draw.rect(window, BLUE, (self.button_layout_4[2][0], self.button_layout_4[2][1], self.button_layout_4[2][2], self.button_layout_4[2][3]))
            pygame.draw.rect(window, BLUE, (self.button_layout_4[3][0], self.button_layout_4[3][1], self.button_layout_4[3][2], self.button_layout_4[3][3]))


        self.window.blit(self.text_surf1, self.text_rect1)
        self.window.blit(self.text_surf2, self.text_rect2)
        #self.window.blit(self.text_surf3, self.text_rect3)
        self.window.blit(self.text_surf4, self.text_rect4)

    
    def text_objects(self, text, font, colour=BLACK):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()


    def pause_menu_setup(self, background, window):
        window.blit(self.background, (0,0))
        pygame.display.update()
        self.background = window.copy()

