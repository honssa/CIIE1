import pygame
from escena import Escena
#from dialogs.creditos import Creditos
import os


def draw_text_2(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = (POS[0] + text_rect.width//2, POS[1]) 
    window.blit(text_surf, text_rect)



class Secreta(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        w=director.win.get_width()
        h=director.win.get_height()
        self.finDialogo=False
        letra_px = 'Assets/fonts/Avenixel-Regular.ttf'
        self.fuente = pygame.font.Font(letra_px, int(27))
        self.fonte_grande = pygame.font.Font(letra_px, int(54))
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets/cinematicas","secreta.png")), (746,434)).convert_alpha()

        secret_sound = pygame.mixer.Sound("Sounds/novos/bck_theme1_matthewpablo.ogg")
        secret_sound.set_volume(0.5)
        secret_sound.play()


        # Cadro de dialogo
        self.cadro_dialogo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","cadro_dialogo.png")),(w, h)).convert_alpha()

        self.dialogo = []	# Pequenas variacions entre comandantes
        self.dialogo.append(("...", 2))
        self.dialogo.append(("... vexo que tiñas mais ganas de vernos ca min...",2))
        self.dialogo.append(("a vosa labor foi increible, resistichedes como o rei leonidas ou a gran cidade de constantinopla frente ao asedio otomano", 5))
        self.dialogo.append(("realmente a humanidade e capaz de todo, e unha pena que un falso profeta vos estea levando a destruccion", 5))
        self.dialogo.append(("... necesitamos axuda", 2))
        self.dialogo.append(("Deus e o voso mellor aliado por eso me enviou a min, eu non son humano pero a miña alma si o e", 5))
        self.dialogo.append(("e compartimos o odio por este despoxo de sociedade na que as leis naturais e divinas son infectadas pola corrupcion tecnocrata e avariciosa da compañia skum", 5))
        self.dialogo.append(("(Pode que os renegados sexan de moi boa axuda)",2))
        self.dialogo.append(("benvido as filas da resistencia, eu son Paper. Temos que dirixirnos agora mesmo cara o bastion, non podemos deixar que Olen o tome",2))
        self.dialogo.append(("reunirei agora mesmo aos meus homes, a batalla nos espera..",5))
        self.dialogo.append(("Por certo perdoa que non me presentara, o meu nome e Ludwig",5))
        

        self.dialogos = []
        self.quen_fala = []
        
        for d in self.dialogo:
            self.dialogos.append(d[0])
            self.quen_fala.append(d[1])

        # PORTRAITS
        self.portrait_paper = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","paper.png")),(272, 272)).convert_alpha()
        self.portrait_ludwig = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","ludwig.png")),(272, 272)).convert_alpha()

        self.MAX_DIALOG = len(self.dialogo)
        self.num=0 
        self.aux=""
        self.i=0

    def update(self, tiempo):
        pass
        
        
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            elif self.num>=self.MAX_DIALOG-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                from main_menu.main_menu import MainMenu
                pygame.mixer.stop()
                escena = MainMenu(self.director)
                self.director.cambiarEscena(escena)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.finDialogo==True:
                self.num+=1
                self.i=0
                self.aux=""
                self.finDialogo=False

    def dibujar(self, win):
        win.fill((0,0,0))
        win.blit(self.bg, (260,0))

        if self.num >= len(self.quen_fala):
            pass
        elif self.quen_fala[self.num] == 2: # Fala paper
            win.blit(self.cadro_dialogo, (0,0))
            win.blit(self.portrait_paper, (50,378))
            draw_text_2("PAPER", self.fonte_grande, (255,255,255), (330,480), win)
        elif self.quen_fala[self.num] == 5: # Fala ???
            win.blit(self.cadro_dialogo, (0,0))
            win.blit(self.portrait_ludwig, (50,378))
            draw_text_2("?????", self.fonte_grande, (255,255,255), (330,480), win)
            
            
        if not (self.num>=self.MAX_DIALOG-1):
            textoEntradaSize=len(self.dialogos[self.num])
        else:
            self.num = self.MAX_DIALOG-1
            textoEntradaSize=len(self.dialogos[self.num])
            
        if self.i<textoEntradaSize:
            self.aux+=self.dialogos[self.num][self.i]
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
