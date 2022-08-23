import pygame
import os
from escena import Escena

WHITE = (255, 255, 255)
MATTE_BLACK = (20, 20, 20)
COR_TEXTO = (191, 228, 230)
coord_panel = (470,60)
coord_titulo = (135,50)
coord_continuar = (195,200)
coord_reintentar = (180,200)
coord_voltar = (195, 400)
# Coords de hovers
coord_hover_continuar = (149,190)
coord_hover_reintentar = (165,210)
coord_hover_voltar = (132,390)
FONT_PIXEL = 'Assets/fonts/KnoxFont.ttf'



class EndLevelScreen(Escena):
    def __init__(self, director, comander, nivel, victory):
        Escena.__init__(self, director)
        self.director=director
        self.victory = victory
        self.window = pygame.display.get_surface()
        self.width, self.height = self.window.get_size()

        self.init_bg = 0
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.background.fill((*MATTE_BLACK, 160))

        self.panel = pygame.image.load(os.path.join("Assets/pantallas", "pantalla_final_nivel.png")).convert_alpha()
        self.victoria_titulo = pygame.image.load(os.path.join("Assets/pantallas", "victoria_titulo.png")).convert_alpha()
        self.derrota_titulo = pygame.image.load(os.path.join("Assets/pantallas", "derrota_titulo.png")).convert_alpha()
        self.hover_continuar = pygame.image.load(os.path.join("Assets/pantallas", "hover_continuar.png")).convert_alpha()
        self.hover_reintentar = pygame.image.load(os.path.join("Assets/pantallas", "hover_reintentar.png")).convert_alpha()
        self.hover_menu = pygame.image.load(os.path.join("Assets/pantallas", "hover_voltar.png")).convert_alpha()
        self.PIXEL_TEXT = pygame.font.Font(FONT_PIXEL, 11)

        self.cursor_pos = (0,0) # Para pillar os hovers
        self.hover = 0 # 0: non hai hover, 1: hai hover no primeiro btn, 2: hai hover no segundo btn

        self.comander=comander
        self.nivel = nivel
        #pygame.mixer.stop()


    def update(self, tiempo):
        self.cursor_pos = pygame.mouse.get_pos()
        if self.cursor_pos[0] > (coord_continuar[0]+coord_panel[0]-60) and self.cursor_pos[0] < (coord_continuar[0]+coord_panel[0]+180) and\
            self.cursor_pos[1] > (coord_continuar[1]+coord_panel[1]-30) and self.cursor_pos[1] < (coord_continuar[1]+coord_panel[1]+70):
            self.hover = 1
        elif self.cursor_pos[0] > (coord_voltar[0]+coord_panel[0]-60) and self.cursor_pos[0] < (coord_voltar[0]+coord_panel[0]+180) and\
            self.cursor_pos[1] > (coord_voltar[1]+coord_panel[1]-30) and self.cursor_pos[1] < (coord_voltar[1]+coord_panel[1]+70):
            self.hover = 2
        else:
            self.hover = 0
	
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            self.cursor_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.director.salirPrograma()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                from main_menu.main_menu import MainMenu
                from dialogs.dialog_scene import Dialogos
                from levels.level import Level1, Level2, Level3
                #dialogo que vai logo de gañar o primeiro nivel e antes de seleccionar para o segundo
                dialogo1 = []
                dialogo1.append(("Bo traballo, conseguichedes aguantar o asedio inimigo e deunos tempo a recoller unha chea de recursos.", 0))
                dialogo1.append(("A mandar xefe! Caeron como mosquitos.", 3))
                dialogo1.append(("Non poderán con nos, os nosos escudos son demasiado fortes.", 1))
                dialogo1.append(("...", 2))
                dialogo1.append(("Tes que estar de broma... Resistir un asedio non é unha vitoria, dende agora encargareime personalmente.", 4))
                dialogo1.append(("Os nosos comandantes son bos no seu traballo. Cesa os teus ataques, non tes ningunha posibilidade.", 0))
                dialogo1.append(("Teño soldados esperando nos sete continentes. Pensas que me vou rendir asi de facil. Non tes ningún xeito de pararme. Teño un exército. Unha especie propia.", 4))
                dialogo1.append(("Unha especie metálica, unha sociedade metálica con persoas metálicas e pensamentos metálicos, sen o único que fai que este planeta estea tan vivo. Xente. Xente común, estúpida, brillante.", 0))
                dialogo1.append(("A persoas presentan fallos, enferman, pelexan entre eles.... Coa miña proposta todo iso queda no pasado.", 4))
                dialogo1.append(("Todo o que inventaches, fixechelo para mellorar a vida das persoas. Iso é brillante. Moi humano. Podeste librar das enfermidades e do envellecemento sen converter ás persoas en máquinas ao teu control.", 0))
                dialogo1.append(("Moi ben entón, vexo que non queres rendirte, prepara aos teus comandantes esta vez non será tan doado. O Fort Knox estará aos meus pés e ninguén vai poder impedilo.",4))
                dialogo1.append(("Que comandante liderará esta misión?", 0))

                #dialogo que vai logo de gañar o nivel 2 e antes de seleccionar para o 3
                dialogo2 = []
                dialogo2.append(("Señor Jenkins, os inimigos acaban de penetrar pola liña Ferruson-Maginot estamos sendo rodeados.", 1))
                dialogo2.append(("Como vai rapaces, menuda lle gastamos, escarallamos a todos eses reloxiños mecánicos, encántame o sonido da metralla impactando neses bechos.",3))
                dialogo2.append(("Por certo, non dou atopado ao comandante Paper, alguén de vos sabe onde vai?", 3))
                dialogo2.append(("Desapareceu esta maña... xa sabes como é, nunca di nada sobre o que fai, pero que desapareza neste momento tan crucial...", 0))
                dialogo2.append(("Espero que teña unha boa razón...", 0))
                dialogo2.append(("Vexo que o que contaban da vella lenda é certo, dun soldado de élite a líder do bastión máis importante do frente, es un bon oponente, Chema.", 4))
                dialogo2.append(("Detén os teus ataques. A xente deste refuxio non quere as túas melloras.", 0))
                dialogo2.append(("Por que? O máis precioso é o cerebro humano e, aínda así, permitimos que morra.",4))
                dialogo2.append(("Todos sabemos o que implica, a resposta é non, se tratas de atacar, defenderémonos.", 0))
                dialogo2.append(("Melloras de metal e un corpo que nunca vai envellecer, como podes didir que non a iso? Ao seguinte nivel da humanidade.",4))
                dialogo2.append(("O seguinte nivel da humanidade? Dirás someterse a túa voluntade.",0))
                dialogo2.append(("Moi ben, resistídevos... Que comence o ataque.", 4))
                dialogo2.append(("Preparemos as defensas!! Que comandante liderará esta misión?", 0))

                dialogo3 = []
                dialogo3.append(("Señor, a artillería inimiga está rompendo todos os nosos escudos e andamos escasos en recursos.", 1))
                dialogo3.append(("Temos que comezar a evacuar a xente do refuxio.", 3))
                dialogo3.append(("Eu non me vou a ningunha parte, se ei de morrer, prefilo facelo na batalla como o fixeron os meus vellos camaradas na gran guerra,", 0))
                dialogo3.append(("Non te vou a abandonar xefe, pero temos que evacuar a poboación, dirixirei o meu batallón para impedir que se acheguen as portas.", 1))
                dialogo3.append(("Comandante Scissors, reúne aos teus homes para evacuar a todos os refuxiados, o túnel aínda está despexado.", 1))
                dialogo3.append(("Rock, pode que este sexa o final da guerra, se a compañía Skum toma este forte... Que opcións lle quedarán a humanidade?", 0))
                dialogo3.append(("... non sei.", 1))
                dialogo3.append(("Pero o que si sei e que debemos loitar ata o final.", 1))
                dialogo3.append(("Rápido vai as portas, parece que están chegando novas brigadas, en canto Scissors teña lista a evacuación sae de aquí, esto vaise poñer demasiado feo.", 0))
                orden1 = []
                orden2 = []
                orden3=[4, 0, 0,0]
                if self.hover == 1 and self.victory:
                    if self.nivel == 1:
                        self.director.cambiarEscena(Dialogos(self.director, self.comander, dialogo1, orden1, 10))
                    elif self.nivel == 2:
                        self.director.cambiarEscena(Dialogos(self.director, self.comander, dialogo2, orden2, 11))
                    elif self.nivel == 3:
                        self.director.cambiarEscena(Dialogos(self.director, self.comander, dialogo3, orden3, 4))
                elif self.hover == 1 and not self.victory:
                    if self.nivel==1:
                        self.director.cambiarEscena(Level1(self.director, self.comander))
                    elif self.nivel==2:
                        self.director.cambiarEscena(Level2(self.director, self.comander))
                    elif self.nivel==3:
                        self.director.cambiarEscena(Level3(self.director, self.comander))
                elif self.hover == 2:
                    self.director.cambiarEscena(MainMenu(self.director))




    def dibujar(self, window):
        if not self.init_bg:
            self.end_level_setup(window)
            self.init_bg = 1
        window.blit(self.background, (0,0))
        window.blit(self.panel, coord_panel)

        # Se ganhache debuxa titulo de victoria e boton de continuar, senon o de reintentar
        if self.victory:
            window.blit(self.victoria_titulo, (coord_panel[0]+coord_titulo[0], coord_panel[1]+coord_titulo[1]) )
            self.draw_text("CONTINUAR", self.PIXEL_TEXT, COR_TEXTO, (coord_panel[0]+coord_continuar[0], coord_panel[1]+coord_continuar[1]), self.window)   
        else:
            window.blit(self.derrota_titulo, (coord_panel[0]+coord_titulo[0], coord_panel[1]+coord_titulo[1]) )
            self.draw_text("REINTENTAR", self.PIXEL_TEXT, COR_TEXTO, (coord_panel[0]+coord_continuar[0], coord_panel[1]+coord_continuar[1]), self.window)

        self.draw_text("VOLTAR AO MENU", self.PIXEL_TEXT, COR_TEXTO, (coord_panel[0]+coord_voltar[0], coord_panel[1]+coord_voltar[1]), self.window)

        if self.hover == 1:
            window.blit(self.hover_continuar, (coord_hover_continuar[0] + coord_panel[0], coord_hover_continuar[1] + coord_panel[1]) )
        elif self.hover == 2:
            window.blit(self.hover_menu, (coord_hover_voltar[0] + coord_panel[0], coord_hover_voltar[1] + coord_panel[1]) )


    def draw_text(self, text, font, COLOUR, POS, window):
        text_surf = font.render(text, True, COLOUR)
        text_rect = text_surf.get_rect()
        text_rect.center = POS
        window.blit(text_surf, text_rect)
    
    def end_level_setup(self, window):
        window.blit(self.background, (0,0))
        pygame.display.update()
        self.background = window.copy()
