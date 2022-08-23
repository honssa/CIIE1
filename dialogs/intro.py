import pygame
import os
from escena import Escena
from dialogs.cinematica_final import Cinematica



COR_TEXTO = (191,228,230)

def divide_imagen(image, rect):
    subimage = image.subsurface(rect)
    return subimage, rect



def draw_text(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = POS
    window.blit(text_surf, text_rect)


class Intro(Escena):
    def __init__(self, director):
        self.director=director
        self.tam_intro = (544, 320)
        pygame.mixer.Sound("Sounds/novos/introsound_matthewpablo.ogg").play(-1)

        self.intros = []
        self.intros.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets/intro/","intro1.png")).convert_alpha(), self.tam_intro) )
        self.intros.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets/intro/","intro2.png")).convert_alpha(), self.tam_intro) )
        self.intros.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets/intro/","intro3.png")).convert_alpha(), self.tam_intro) )
        self.intros.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets/intro/","intro4.png")).convert_alpha(), self.tam_intro) )

        self.pos_bg = (380,50)
        self.pos_texto = (200, 505)
        self.tiras_total = []
        self.tiras_intro1 = []
        self.tiras_intro2 = []
        self.tiras_intro3 = []
        self.tiras_intro4 = []
        
        self.current_image = 0
        self.counter_transicion = 0
        self.debuxar_texto_agora = False

        FONT_PIXEL = 'Assets/fonts/KnoxFont.ttf'
        self.PIXEL_TEXT = pygame.font.Font(FONT_PIXEL, 16)
        self.textos = []
        self.textos.append("FAI XA MOITOS ANOS UNHA GRAN COMPAÑIA INDUSTRIAL DESENVOLVEU UN PRODUTO PARA TERMINAR COAS ENFERMIDADES E AS DEBILIDADES DOS HUMANS.")
        self.textos.append("A SUA INFLUENCIA ESPALLOUSE POR TODO O MUNDO PERO AS SUAS INTENCIONS ESTABAN CORRUPTAS.")
        self.textos.append("ANSIARON CREAR UNHA NOVA ESPECIE, CONDUCIR A HUMANIDADE A UNHA NOVA ERA, PERO ESTO SO TROUXO A MAIOR DAS GUERRAS.")
        self.textos.append("DESPOIS DE MOITOS ANOS DE LOITA, A RESISTENCIA QUEDOU DEBILITADA, A COMPAÑIA DIRIXE AGORA A SUA ATENCION CARA UN DOS PILARES DA RESISTENCIA,\
 O BASTION FORT KNOX, COMANDADO POLO LEXENDARIO EXCOMBATENTE CHEMA JENKINS.")


        self.dialogo_a_continuacion = []
        self.dialogo_a_continuacion.append(("Despois de varios anos de calma parece que volven as andadas.",0))
        self.dialogo_a_continuacion.append(("Deberiamos retirar as tropas expedicionarias señor.",1))
        self.dialogo_a_continuacion.append(("Nunca! Esta expedición está comezando a dar os seus froitos, necesitamos unhas poucas semanas e\
 poderemos repoñer todas as reservas.",3))
        self.dialogo_a_continuacion.append(("O inimigo estase achegando e non temos información suficiente, pode que sexa máis poderoso ca última vez. ",0))
        self.dialogo_a_continuacion.append(("...",2))
        self.dialogo_a_continuacion.append(("Según os meus rastrexadores o ataque será inminente pero non teño información sobre o número ou o tipo de armamento.",2))
        self.dialogo_a_continuacion.append(("Está ben, iniciaremos un plan defensivo, pero non debemos deixar que destruan a entrada ao sector principal.",0))
        self.dialogo_a_continuacion.append(("Que comandante levará a cabo esta misión?",0))

        for x in range(0, self.intros[0].get_width()):
            subimage, rect = divide_imagen(self.intros[0], pygame.Rect((x,0) ,(1,self.tam_intro[1]) ))
            self.tiras_intro1.append(subimage)
        for x in range(0, self.intros[1].get_width()):
            subimage, rect = divide_imagen(self.intros[1], pygame.Rect((x,0) ,(1,self.tam_intro[1]) ))
            self.tiras_intro2.append(subimage)
        for x in range(0, self.intros[2].get_width()):
            subimage, rect = divide_imagen(self.intros[2], pygame.Rect((x,0) ,(1,self.tam_intro[1]) ))
            self.tiras_intro3.append(subimage)
        for x in range(0, self.intros[3].get_width()):
            subimage, rect = divide_imagen(self.intros[3], pygame.Rect((x,0) ,(1,self.tam_intro[1]) ))
            self.tiras_intro4.append(subimage)
        self.tiras_total.append(self.tiras_intro1)
        self.tiras_total.append(self.tiras_intro2)
        self.tiras_total.append(self.tiras_intro3)
        self.tiras_total.append(self.tiras_intro4)

        self.num=0
        self.aux=""
        self.i=0


    
    def update(self, *args):
        pass

    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            if self.num== len(self.textos)-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                from dialogs.dialog_scene import Dialogos
                pygame.mixer.stop()

                escena = Dialogos(self.director, None, self.dialogo_a_continuacion, "o", 9)
                #from levels.level import Level3
                #escena = Level3(self.director, "rock")
                self.director.cambiarEscena(escena)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.num+=1
                self.i=0
                self.aux=""
                self.finDialogo=False
                self.debuxar_texto_agora = False
                self.counter_transicion = 0
                if self.current_image < len(self.intros)-1:
                    self.current_image += 1
        
        
        
    def dibujar(self, win):
        win.fill((0,0,0))
        self.counter_transicion += 3
        if self.counter_transicion >= self.tam_intro[0]:
            win.blit(self.intros[self.current_image], self.pos_bg)
            self.debuxar_texto_agora = True
        else:
            for i in range(self.counter_transicion):
                win.blit(self.tiras_total[self.current_image][i], (self.pos_bg[0]+i, self.pos_bg[1]))

        if self.debuxar_texto_agora:
            if not (self.num>=len(self.textos)-1):
                textoEntradaSize=len(self.textos[self.num])
            else:
                self.num = len(self.textos)-1 
                textoEntradaSize=len(self.textos[self.num])

            if self.i<textoEntradaSize:
                self.aux+=self.textos[self.num][self.i]
                self.i+=1
            else:
                self.finDialogo=True
        
            self.blit_text(win, self.pos_texto, self.PIXEL_TEXT)
    



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
