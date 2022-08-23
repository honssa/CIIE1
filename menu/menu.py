import pygame
import os

ANCHO=1340
ALTO=700
pygame.init()
pygame.display.set_mode((ANCHO, ALTO))
# Clase abstracta para un boton
class Button:
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.x = menu.x
        self.y = menu.y
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    

    def click(self, X, Y):
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True 
        return False


    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


    def update(self):
        self.x = self.menu.x
        self.y = self.menu.y 

class TowerButton(Button):
    def __init__(self, img,img_focus,img2, x, y, name, cost=0):
        self.name = name
        self.img_unfocus = img
        self.img_focus = img_focus

        self.img = img
        self.img2 = img2
        self.x = x 
        self.y = y 
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    def set_focus(self,b):
        if b:
            self.img = self.img_focus
        else:
            self.img = self.img_unfocus
    def draw(self,window):
        super().draw(window)
        window.blit(self.img2, (self.x+4,self.y-14))
    


def draw_text(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = POS
    window.blit(text_surf, text_rect)



def draw_text_2(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = (POS[0] + text_rect.width//2, POS[1]) 
    window.blit(text_surf, text_rect)



class HUDStatic():
    def __init__(self, max_health_gate):
        self.scrap_panel = pygame.image.load(os.path.join("Assets/HUD", "panel_chatarra.png")).convert_alpha()
        self.battery_panel = pygame.image.load(os.path.join("Assets/HUD", "panel_baterias.png")).convert_alpha()
        self.status_gate = pygame.image.load(os.path.join("Assets/HUD", "porta_status.png")).convert_alpha()
        self.max_health_gate = max_health_gate
        FONT_PIXEL = 'Assets/fonts/KnoxFont.ttf'
        self.PIXEL_TEXT = pygame.font.Font(FONT_PIXEL, 11)

    def draw(self, window, scrap, batteries, health_gate):
        #window.blit(self.status_gate, ())
        HEALTH_BAR_DIMENSIONS = (166,20)
        offset = (10,6)
        
        pygame.draw.rect(window,(62,81,84),(10+offset[0],10+offset[1],HEALTH_BAR_DIMENSIONS[0],HEALTH_BAR_DIMENSIONS[1]))
        pygame.draw.rect(window,(191,228,230),(10+offset[0],10+offset[1],HEALTH_BAR_DIMENSIONS[0]*health_gate/100,HEALTH_BAR_DIMENSIONS[1]))
        window.blit(self.status_gate, (10,10))

        width, height = window.get_size()
        window.blit(self.scrap_panel, (width-300, 10))
        window.blit(self.battery_panel, (width-550, 10))
        draw_text("CHATARRA : " + str(scrap), self.PIXEL_TEXT, (44,54,52), (width-170, 32), window)
        draw_text("BATERIAS : " + str(batteries), self.PIXEL_TEXT, (44,54,52), (width-420, 32), window)


class HUDState():

    name = "state"
    allowed = []
    FONT_PIXEL = 'Assets/fonts/KnoxFont.ttf'
    PIXEL_TEXT = pygame.font.Font(FONT_PIXEL, 10)
    PIXEL_TEXT_BIG = pygame.font.Font(FONT_PIXEL, 16)
    HUD_TEXT_COLOUR = (44, 54, 52)
    

    pos_panel1 = (188, 508)
    pos_panel2 = (508, 508)
    pos_panel3 = (828, 508)

    # Tamanho normal dos botons estandar
    std_btn_size = (50,50)

    #Offsets
    p3_b1 = (65, 19)
    p3_b2 = (143, 19)
    p3_b3 = (221, 19)
    p3_b4 = (144, 126)

    p1_b1 = (40, 19)
    p1_b2 = (117, 19)
    p1_b3 = (196, 19)

    # Coste das torres
    std_twr_cost = 30
    rg_twr_cost = 40
    dmg_twr_cost = 50

    repair_cost = 20
    upgrade_cost = 1

    # Info das torres
    # (dano)
    dmg_twr_std = 2
    dmg_twr_rg = 1
    dmg_twr_dmg = 4

    # (rango)
    rg_twr_std = 4
    rg_twr_rg = 5
    rg_twr_dmg = 3

    # (cadencia)
    cad_twr_std = 30
    cad_twr_rg = 30
    cad_twr_dmg = 30

    # (vida)

    # (tempo de construccion)
    tmp_twr_std = 5
    tmp_twr_rg = 5
    tmp_twr_dmg = 5

    # Imaxes cargadas
    panel1_desactivado = pygame.image.load(os.path.join("Assets/HUD", "panel1_desactivado.png")).convert_alpha()
    panel1_activado = pygame.image.load(os.path.join("Assets/HUD", "panel1_activado.png")).convert_alpha()
    panel2_info_moving = pygame.image.load(os.path.join("Assets/HUD", "panel2_info_moving.png")).convert_alpha()
    panel2_desactivado = pygame.image.load(os.path.join("Assets/HUD", "panel2_desactivado.png")).convert_alpha()
    panel3_desactivado = pygame.image.load(os.path.join("Assets/HUD", "panel3_desactivado.png")).convert_alpha()
    panel3_activado = pygame.image.load(os.path.join("Assets/HUD", "panel3_activado.png")).convert_alpha()
    ab_rock = pygame.image.load(os.path.join("Assets/HUD", "ab_rock.png")).convert_alpha()
    ab_scissors = pygame.image.load(os.path.join("Assets/HUD", "ab_scissors.png")).convert_alpha()
    ab_paper = pygame.image.load(os.path.join("Assets/HUD", "ab_paper.png")).convert_alpha()

    # Fondo da barra de vida
    bg_healthbar = pygame.image.load(os.path.join("Assets/HUD", "health_bar_info.png")).convert_alpha()

    # Hovers
    hover_twr_img = pygame.image.load(os.path.join("Assets/HUD", "hover_torres_panel3.png")).convert_alpha()
    hover_reparar = pygame.image.load(os.path.join("Assets/HUD", "reparar_hover.png")).convert_alpha()
    hover_mellorar = pygame.image.load(os.path.join("Assets/HUD", "mellorar_hover.png")).convert_alpha()
    hover_reciclar = pygame.image.load(os.path.join("Assets/HUD", "reciclar_hover.png")).convert_alpha()
    hover_ab = pygame.image.load(os.path.join("Assets/HUD", "hover_ab.png")).convert_alpha()

    cancel_desactivado = pygame.image.load(os.path.join("Assets/HUD", "cancel_desactivado.png")).convert_alpha() 
    cancel_activado = pygame.image.load(os.path.join("Assets/HUD", "cancel_activado.png")).convert_alpha() 
    cancel_hover = pygame.image.load(os.path.join("Assets/HUD", "cancel_hover.png")).convert_alpha() 

    img_std_twr = pygame.image.load(os.path.join("Assets/HUD", "img_std_twr.png")).convert_alpha()
    img_rg_twr = pygame.image.load(os.path.join("Assets/HUD", "img_rg_twr.png")).convert_alpha()
    img_dmg_twr = pygame.image.load(os.path.join("Assets/HUD", "img_dmg_twr.png")).convert_alpha()

    img_build_repair =  pygame.image.load(os.path.join("Assets/HUD", "build_repair.png")).convert_alpha()
    img_upgrade =  pygame.image.load(os.path.join("Assets/HUD", "upgrade.png")).convert_alpha()


    def is_cursor_in_p3_b1(self, pos):
        # posicion do cursor sobre o boton 1 do panel3
        if pos[0] > self.pos_panel3[0] + self.p3_b1[0] and pos[0] < self.pos_panel3[0] + self.p3_b1[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel3[1] + self.p3_b1[1] and pos[1] < self.pos_panel3[1] + self.p3_b1[1] + self.std_btn_size[1]:
                return True
        else:
            return False

    def is_cursor_in_p3_b2(self, pos):
        if pos[0] > self.pos_panel3[0] + self.p3_b2[0] and pos[0] < self.pos_panel3[0] + self.p3_b2[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel3[1] + self.p3_b2[1] and pos[1] < self.pos_panel3[1] + self.p3_b2[1] + self.std_btn_size[1]:
                return True
        else:
            return False

    def is_cursor_in_p3_b3(self, pos):
        if pos[0] > self.pos_panel3[0] + self.p3_b3[0] and pos[0] < self.pos_panel3[0] + self.p3_b3[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel3[1] + self.p3_b3[1] and pos[1] < self.pos_panel3[1] + self.p3_b3[1] + self.std_btn_size[1]:
                return True
        else:
            return False
    

    def is_cursor_in_p3_b4(self, pos):
        if pos[0] > self.pos_panel3[0] + self.p3_b4[0] and pos[0] < self.pos_panel3[0] + self.p3_b4[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel3[1] + self.p3_b4[1] and pos[1] < self.pos_panel3[1] + self.p3_b4[1] + self.std_btn_size[1]:
                return True
        else:
            return False
    
    ##################################

    def is_cursor_in_p1_b1(self, pos):
        # posicion do cursor sobre o boton 1 do panel3
        if pos[0] > self.pos_panel1[0] + self.p1_b1[0] and pos[0] < self.pos_panel1[0] + self.p1_b1[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel1[1] + self.p1_b1[1] and pos[1] < self.pos_panel1[1] + self.p1_b1[1] + self.std_btn_size[1]:
                return True
        else:
            return False

    def is_cursor_in_p1_b2(self, pos):
        if pos[0] > self.pos_panel1[0] + self.p1_b2[0] and pos[0] < self.pos_panel1[0] + self.p1_b2[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel1[1] + self.p1_b2[1] and pos[1] < self.pos_panel1[1] + self.p1_b2[1] + self.std_btn_size[1]:
                return True
        else:
            return False

    def is_cursor_in_p1_b3(self, pos):
        if pos[0] > self.pos_panel1[0] + self.p1_b3[0] and pos[0] < self.pos_panel1[0] + self.p1_b3[0] + self.std_btn_size[0] and\
            pos[1] > self.pos_panel1[1] + self.p1_b3[1] and pos[1] < self.pos_panel1[1] + self.p1_b3[1] + self.std_btn_size[1]:
                return True
        else:
            return False


    def switch(self, state):
        # Cambiar de estado
        if state.name in self.allowed:
            return True

        else:
            return False

    def __str__(self):
        return self.name



# Estado no que non hai nada seleccionado nin obxeto flotante
class HUDStateZero(HUDState):
    name = "state_0"
    allowed = ["state_1", "state_2", "state_3"]

    def __init__(self, comander, reload_ab=None):
        self.comander = comander
        self.hover = 0
        self.ab_img = None
        self.reload_ab = reload_ab
        self.max_recarga = 0
     
        if self.comander == "rock":
            self.ab_img = self.ab_rock
            self.max_recarga = 3600
        elif self.comander == "paper":
            self.ab_img = self.ab_paper
            self.max_recarga = 2400
        elif self.comander == "scissors":
            self.ab_img = self.ab_scissors
            self.max_recarga = 1200

    def update_pos(self, pos):
        result = [None, ""]
        if self.is_cursor_in_p3_b1(pos):
            self.hover = 1
        
        elif self.is_cursor_in_p3_b2(pos):
            self.hover = 2

        elif self.is_cursor_in_p3_b3(pos):
            self.hover = 3
        
        elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
            self.hover = 4
        
        else:
            self.hover = 0
        return result
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = ["", ""]
        if not selected_tower:
            if self.is_cursor_in_p3_b1(pos) and scrap >= self.std_twr_cost:
                pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
                result[0] =  "add_std_twr"
                result[1] = "to_state_2"
            elif self.is_cursor_in_p3_b2(pos) and scrap >= self.rg_twr_cost:
                pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
                result[0] = "add_rg_twr"
                result[1] = "to_state_2"
            elif self.is_cursor_in_p3_b3(pos) and scrap >= self.dmg_twr_cost:
                pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
                result[0] = "add_dmg_twr"
                result[1] = "to_state_2"
            elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
                pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
                result[0] = "ab_"+self.comander
                result[1] = "to_state_4"
        else:
            if selected_tower.operativa:
                result[1] = "to_state_1"
            else:
                result[1] = "to_state_3"

        return result

    def draw(self, window, ab_counter):
        panel1 = self.panel1_desactivado
        panel2 = self.panel2_desactivado
        panel3 = self.panel3_activado
        hover_img = self.hover_twr_img

        window.blit(panel1, (self.pos_panel1))
        window.blit(panel2, (self.pos_panel2))
        window.blit(panel3, (self.pos_panel3))
        if not self.reload_ab[1]:
            window.blit(self.ab_img, (self.pos_panel3[0]+self.p3_b4[0], self.pos_panel3[1]+self.p3_b4[1]))
        else:
            length = 46
            move_by = ab_counter / self.max_recarga  # 10 s Tempo de carga
            time_bar = round(move_by * length)
            pygame.draw.rect(window, (44, 54, 52), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, length, 6), 0)
            pygame.draw.rect(window, (191,228,230), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, time_bar, 6), 0)
        if self.hover == 1:
            window.blit(hover_img, (self.pos_panel3[0]+56, self.pos_panel3[1]+14))
            draw_text_2(str(self.std_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+80, self.pos_panel3[1]+93), window)
        elif self.hover == 2:
            window.blit(hover_img, (self.pos_panel3[0]+133, self.pos_panel3[1]+14))
            draw_text_2(str(self.rg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+157, self.pos_panel3[1]+93), window)
        elif self.hover == 3:
            window.blit(hover_img, (self.pos_panel3[0]+212, self.pos_panel3[1]+14))
            draw_text_2(str(self.dmg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+236, self.pos_panel3[1]+93), window)
        elif self.hover == 4:
            window.blit(self.hover_ab, (self.pos_panel3[0]+self.p3_b4[0]-6, self.pos_panel3[1]+self.p3_b4[1]-6))



# Estado no que tes seleccionada unha torre operativa
class HUDStateOne(HUDState):
    name = "state_1"
    allowed = ["state_0", "state_2", "state_3"]

    def __init__(self, twr, comander, reload_ab):
        self.comander = comander
        self.ab_img = None
        self.reload_ab = reload_ab
        self.max_recarga = 0
        if self.comander == "rock":
            self.ab_img = self.ab_rock
            self.max_recarga = 3600
        elif self.comander == "paper":
            self.ab_img = self.ab_paper
            self.max_recarga = 2400
        elif self.comander == "scissors":
            self.ab_img = self.ab_scissors
            self.max_recarga = 1200
            

        if twr.type == "std":
            aux = self.img_std_twr
            aux_name_txt = "TORRE DE RAFAGAS"
        elif twr.type == "rg":
            aux = self.img_rg_twr
            aux_name_txt = "TORRE DE ARTILLERIA"
        else:
            aux = self.img_dmg_twr
            aux_name_txt = "TORRE DE CAÑONS"
        self.twr = twr
        self.twr_img = aux
        self.name_txt = aux_name_txt
        self.rg_txt = "RANGO DE ATAQUE:  " + str(twr.tw_range)
        self.dmg_txt = "PUNTOS DE ATAQUE:  " + str(twr.dmg)
        self.cad_txt = "CADENCIA DE DISPARO:  " + str(twr.cadence)
        self.tmp_txt = "TEMPO DE CONSTRUCION:  " + str(5) + " s"

        self.hover = 0

    def update_pos(self, pos):
        result = [self.twr, ""]
        if self.twr.non_operative_status == "dead":
            result[1] = "to_state_0"
        if self.is_cursor_in_p3_b1(pos):
            self.hover = 1
        
        elif self.is_cursor_in_p3_b2(pos):
            self.hover = 2

        elif self.is_cursor_in_p3_b3(pos):
            self.hover = 3

        elif self.is_cursor_in_p1_b1(pos):
            self.hover = 4
        
        elif self.is_cursor_in_p1_b2(pos) and self.twr.nivel < 3:
            self.hover = 5
        
        elif self.is_cursor_in_p1_b3(pos):
            self.hover = 6
        
        elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
            self.hover = 7

        else:
            self.hover = 0

        return result
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = ["", ""]
        
        if self.is_cursor_in_p3_b1(pos) and scrap >= self.std_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] =  "add_std_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b2(pos) and scrap >= self.rg_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "add_rg_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b3(pos) and scrap >= self.dmg_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "add_dmg_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "ab_"+self.comander
            result[1] = "to_state_4"
        elif self.is_cursor_in_p1_b1(pos) and scrap >= self.repair_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "repair"
            result[1] = "to_state_3"
        elif self.is_cursor_in_p1_b2(pos) and self.twr.nivel < 3 and batteries >= self.upgrade_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            self.twr.non_operative_status = "upgrading"
            result[0] = "upgrade"
            result[1] = "to_state_3"
        elif self.is_cursor_in_p1_b3(pos):
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "reciclar"
            result[1] = "to_state_0"
        # clicas e deseleccionas (transicionas ao estado 0)
        elif not selected_tower:
            result[1] = "to_state_0"
        # E seleccionada unha torre distinta
        elif selected_tower != self.twr:
            if selected_tower.operativa:
                result[1] = "to_state_1"
            else:
                result[1] = "to_state_3"

        return result



    def draw(self, window, ab_counter):
        panel1 = self.panel1_activado
        panel2 = self.panel2_info_moving
        panel3 = self.panel3_activado

        window.blit(panel1, (self.pos_panel1))
        window.blit(panel2, (self.pos_panel2))
        window.blit(panel3, (self.pos_panel3))
        if not self.reload_ab[1]:
            window.blit(self.ab_img, (self.pos_panel3[0]+self.p3_b4[0], self.pos_panel3[1]+self.p3_b4[1]))
        else:
            length = 46
            move_by = ab_counter / self.max_recarga  # 10 s Tempo de carga
            time_bar = round(move_by * length)
            pygame.draw.rect(window, (44, 54, 52), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, length, 6), 0)
            pygame.draw.rect(window, (191,228,230), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, time_bar, 6), 0)

        # Imaxe do tipo de torre
        window.blit(self.twr_img, (self.pos_panel2[0]+14, self.pos_panel2[1]+26))
        # Texto do panel2
        draw_text(self.name_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+220, self.pos_panel2[1]+28), window)
        if self.twr.nivel == 1:
            draw_text_2("( I )", self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+290, self.pos_panel2[1]+28), window)
        elif self.twr.nivel == 2:
            draw_text_2("( II )", self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+290, self.pos_panel2[1]+28), window)
        elif self.twr.nivel == 3:
            draw_text_2("( III )", self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+290, self.pos_panel2[1]+28), window)

        vida_actual = str(self.twr.health) + " / " + str(self.twr.max_health) + "  (PV)"
        draw_text(vida_actual, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+115, self.pos_panel2[1]+48), window)


        draw_text(self.rg_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+84, self.pos_panel2[1]+96), window)
        draw_text(self.dmg_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+92, self.pos_panel2[1]+116), window)
        draw_text(self.cad_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+99, self.pos_panel2[1]+136), window)
        draw_text(self.tmp_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+106, self.pos_panel2[1]+156), window)

        # Hovers
        if self.hover == 1:
            window.blit(self.hover_twr_img, (self.pos_panel3[0]+56, self.pos_panel3[1]+14))
            draw_text_2(str(self.std_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+80, self.pos_panel3[1]+93), window)
        elif self.hover == 2:
            draw_text_2(str(self.rg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+157, self.pos_panel3[1]+93), window)
            window.blit(self.hover_twr_img, (self.pos_panel3[0]+133, self.pos_panel3[1]+14))
        elif self.hover == 3:
            draw_text_2(str(self.dmg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+236, self.pos_panel3[1]+93), window)
            window.blit(self.hover_twr_img, (self.pos_panel3[0]+212, self.pos_panel3[1]+14))

        elif self.hover == 4:
            window.blit(self.hover_reparar, (self.pos_panel1[0]+40, self.pos_panel1[1]+14))
            draw_text_2("Recupera 10PV. Custo: " + str(self.repair_cost), self.PIXEL_TEXT, (191,228,230), (self.pos_panel1[0]+40, self.pos_panel1[1]+134), window)
        elif self.hover == 5:
            window.blit(self.hover_mellorar, (self.pos_panel1[0]+117, self.pos_panel1[1]+14))
            draw_text_2("Custo: 1 Bateria", self.PIXEL_TEXT, (191,228,230), (self.pos_panel1[0]+40, self.pos_panel1[1]+134), window)
        elif self.hover == 6:
            window.blit(self.hover_reciclar, (self.pos_panel1[0]+196, self.pos_panel1[1]+14))
            draw_text_2("Destrue a torre. Recupera " + str(self.twr.cost_construction), self.PIXEL_TEXT, (191,228,230), (self.pos_panel1[0]+40, self.pos_panel1[1]+134), window)
        elif self.hover == 7:
            window.blit(self.hover_ab, (self.pos_panel3[0]+self.p3_b4[0]-6, self.pos_panel3[1]+self.p3_b4[1]-6))
        
        
        # Barra de vida
        length = 74 #74
        move_by = self.twr.health / self.twr.max_health
        health_bar = round(move_by * length)

        pygame.draw.rect(window, (44, 54, 52), (self.pos_panel2[0]+72, self.pos_panel2[1]+30, length, 6), 0)
        pygame.draw.rect(window, (191,228,230), (self.pos_panel2[0]+72, self.pos_panel2[1]+30, health_bar, 6), 0)
        # Fondo da barra de vida
        window.blit(self.bg_healthbar, (self.pos_panel2[0]+70, self.pos_panel2[1]+28))









# Estado no que tes un obxeto flotante
class HUDStateTwo(HUDState):
    name = "state_2"
    allowed = ["state_0"]
    twr_img = None

    def __init__(self, twr, comander):
        self.comander = comander
        if twr == "add_rg_twr":
            aux = self.img_rg_twr
            aux_name_txt = "TORRE DE ARTILLERIA"
            aux_rg_txt = "RANGO DE ATAQUE:  " + str(self.rg_twr_rg)
            aux_dmg_txt = "PUNTOS DE ATAQUE:  " + str(self.dmg_twr_rg)
            aux_cad_txt = "CADENCIA DE DISPARO:  " + str(self.cad_twr_rg)
            aux_tmp_txt = "TEMPO DE CONSTRUCION:  " + str(self.tmp_twr_rg)
        elif twr == "add_dmg_twr":
            aux = self.img_dmg_twr
            aux_name_txt = "TORRE DE CAÑONS"
            aux_rg_txt = "RANGO DE ATAQUE:  " + str(self.rg_twr_dmg)
            aux_dmg_txt = "PUNTOS DE ATAQUE:  " + str(self.dmg_twr_dmg)
            aux_cad_txt = "CADENCIA DE DISPARO:  " + str(self.cad_twr_dmg)
            aux_tmp_txt = "TEMPO DE CONSTRUCION:  " + str(self.tmp_twr_dmg)
        else:
            aux = self.img_std_twr
            aux_name_txt = "TORRE DE RAFAGAS"
            aux_rg_txt = "RANGO DE ATAQUE:  " + str(self.rg_twr_std)
            aux_dmg_txt = "PUNTOS DE ATAQUE:  " + str(self.dmg_twr_std)
            aux_cad_txt = "CADENCIA DE DISPARO:  " + str(self.cad_twr_std)
            aux_tmp_txt = "TEMPO DE CONSTRUCION:  " + str(self.tmp_twr_std)
        self.twr_img = aux
        self.name_txt = aux_name_txt
        self.rg_txt = aux_rg_txt
        self.dmg_txt = aux_dmg_txt
        self.cad_txt = aux_cad_txt
        self.tmp_txt = aux_tmp_txt

        self.hover = 0


    def update_pos(self, pos):
        result = [None, ""]
        if (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298):
            if (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80):
                self.hover = 1
            else:
                self.hover = 0
        else:
            self.hover = 0
        return result
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = ["",""]
        if (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298) and\
                (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80):
                result[0] = "cancel_placement"
                result[1] = "to_state_0"
        else:
            if occupied:
                result[1] = "no_transition"
            else:
                result[0] = "confirm_placement"
                result[1] = "to_state_3"
        return result


    def draw(self, window, ab_counter):
        panel1 = self.panel1_desactivado
        panel2 = self.panel2_info_moving
        panel3 = self.panel3_desactivado

        window.blit(panel1, (self.pos_panel1))
        window.blit(panel2, (self.pos_panel2))
        window.blit(panel3, (self.pos_panel3))

        # Debuxar boton
        if self.hover:
            window.blit(self.cancel_hover, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))
        else:
            window.blit(self.cancel_desactivado, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))

        # Debuxar informacion do panel2

        # Imaxe do tipo de torre
        window.blit(self.twr_img, (self.pos_panel2[0]+14, self.pos_panel2[1]+26))
        # Texto do panel2
        draw_text(self.name_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+132, self.pos_panel2[1]+28), window)


        draw_text(self.rg_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+84, self.pos_panel2[1]+96), window)
        draw_text(self.dmg_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+88, self.pos_panel2[1]+116), window)
        draw_text(self.cad_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+99, self.pos_panel2[1]+136), window)
        draw_text(self.tmp_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+103, self.pos_panel2[1]+156), window)






# Estado no que tes seleccionada unha torre non operativa
class HUDStateThree(HUDState):
    name = "state_3"
    allowed = ["state_0", "state_1", "state_2"]

    def __init__(self,twr,comander,reload_ab):
        self.comander = comander
        self.ab_img = None
        self.reload_ab = reload_ab
        self.max_recarga = 0
        if self.comander == "rock":
            self.ab_img = self.ab_rock
            self.max_recarga = 3600
        elif self.comander == "paper":
            self.ab_img = self.ab_paper
            self.max_recarga = 2400
        elif self.comander == "scissors":
            self.ab_img = self.ab_scissors
            self.max_recarga = 1200
        self.hover = 0

        if twr.type == "std":
            aux_name_txt = "TORRE DE RAFAGAS"
        elif twr.type == "rg":
            aux_name_txt = "TORRE DE ARTILLERIA"
        else:
            aux_name_txt = "TORRE DE CAÑONS"
        self.twr = twr
        print(self.twr.non_operative_status)
        if self.twr.non_operative_status == "building" or self.twr.non_operative_status == "repairing":
            self.twr_img = self.img_build_repair
        else:
            self.twr_img = self.img_upgrade
        self.name_txt = aux_name_txt
        self.rg_txt = "RANGO DE ATAQUE:  " + str(twr.tw_range)
        self.dmg_txt = "PUNTOS DE ATAQUE:  " + str(twr.dmg)
        self.cad_txt = "CADENCIA DE DISPARO:  " + str(twr.cadence)
        self.tmp_txt = "TEMPO DE CONSTRUCION:  " + str(5)



    def update_pos(self, pos):
        result = [self.twr, ""]
        if self.twr.operativa:
            result[1] = "to_state_1"

        if self.is_cursor_in_p3_b1(pos):
            self.hover = 1
        
        elif self.is_cursor_in_p3_b2(pos):
            self.hover = 2

        elif self.is_cursor_in_p3_b3(pos):
            self.hover = 3
        
        elif (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298) and\
            (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80):
                self.hover = 4 

        elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
            self.hover = 5

        else:
            self.hover = 0
        return result
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = ["", ""]
        
        if self.is_cursor_in_p3_b1(pos) and scrap >= self.std_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] =  "add_std_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b2(pos) and scrap >= self.rg_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "add_rg_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b3(pos) and scrap >= self.dmg_twr_cost:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "add_dmg_twr"
            result[1] = "to_state_2"
        elif self.is_cursor_in_p3_b4(pos) and not self.reload_ab[1]:
            pygame.mixer.Sound("Sounds/novos/menu_click_qubodup.ogg").play()
            result[0] = "ab_"+self.comander
            result[1] = "to_state_4"
        elif (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298) and\
                (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80) and \
                    self.twr.non_operative_status == "building":
            print("cancel construction")
            result[0] = "cancel_construction"
            result[1] = "to_state_0"
        # clicas e deseleccionas (transicionas ao estado 0)
        elif not selected_tower:
            result[1] = "to_state_0"
        # E seleccionada unha torre distinta
        elif selected_tower != self.twr:
            if selected_tower.operativa:
                result[1] = "to_state_1"
            else:
                result[1] = "to_state_3"

        return result

    def draw(self, window, ab_counter):
        panel1 = self.panel1_desactivado
        panel2 = self.panel2_info_moving
        panel3 = self.panel3_activado

        window.blit(panel1, (self.pos_panel1))
        window.blit(panel2, (self.pos_panel2))
        window.blit(panel3, (self.pos_panel3))

        if not self.reload_ab[1]:
            window.blit(self.ab_img, (self.pos_panel3[0]+self.p3_b4[0], self.pos_panel3[1]+self.p3_b4[1]))
        else:
            length = 46
            move_by = ab_counter / self.max_recarga  # 10 s Tempo de carga
            time_bar = round(move_by * length)
            pygame.draw.rect(window, (44, 54, 52), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, length, 6), 0)
            pygame.draw.rect(window, (191,228,230), (self.pos_panel3[0] + self.p3_b4[0] + 1, self.pos_panel3[1] + self.p3_b4[1] + 20, time_bar, 6), 0)

        hover_img = self.hover_twr_img

        # Imaxe icono estado
        window.blit(self.twr_img, (self.pos_panel2[0]+14, self.pos_panel2[1]+26))

        # debuxar nome
        draw_text(self.name_txt, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+220, self.pos_panel2[1]+28), window)

        # Barra de construccion
        length = 74
        move_by = 0
        if self.twr.non_operative_status == "repairing":
            move_by = self.twr.counter_build / self.twr.tempo_reparacion
        else:
            move_by = self.twr.counter_build / self.twr.tempo_construccion
        time_bar = round(move_by * length)
        # Barra de reparacion

        pygame.draw.rect(window, (44, 54, 52), (self.pos_panel2[0]+72, self.pos_panel2[1]+30, length, 6), 0)
        pygame.draw.rect(window, (191,228,230), (self.pos_panel2[0]+72, self.pos_panel2[1]+30, time_bar, 6), 0)
        # Fondo da barra de vida
        window.blit(self.bg_healthbar, (self.pos_panel2[0]+70, self.pos_panel2[1]+28))

        # Debuxar boton
        if self.twr.non_operative_status == "building" or self.twr.non_operative_status == "upgrading":
            if self.hover == 4:
                window.blit(self.cancel_hover, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))
            else:
                window.blit(self.cancel_desactivado, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))

            
        if self.hover == 1:
            window.blit(hover_img, (self.pos_panel3[0]+56, self.pos_panel3[1]+14))
            draw_text_2(str(self.std_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+80, self.pos_panel3[1]+93), window)
        elif self.hover == 2:
            window.blit(hover_img, (self.pos_panel3[0]+133, self.pos_panel3[1]+14))
            draw_text_2(str(self.rg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+157, self.pos_panel3[1]+93), window)
        elif self.hover == 3:
            window.blit(hover_img, (self.pos_panel3[0]+212, self.pos_panel3[1]+14))
            draw_text_2(str(self.dmg_twr_cost), self.PIXEL_TEXT_BIG, (191,228,230), (self.pos_panel3[0]+236, self.pos_panel3[1]+93), window)
        elif self.hover == 5:
            window.blit(self.hover_ab, (self.pos_panel3[0]+self.p3_b4[0]-6, self.pos_panel3[1]+self.p3_b4[1]-6))








# Estado no que activache unha abilidade activada de comandante
class HUDStateFour(HUDState):
    name = "state_4"
    allowed = ["state_0"]
    twr_img = None

    def __init__(self, twr, comander,reload_ab):
        self.comander = comander
        self.ab_img = None
        self.reload_ab = reload_ab
        if self.comander == "rock":
            self.ab_img = self.ab_rock
            self.ab_nome = "Barricada rexa"
            self.ab_desc1 = "Permite crear unha barricada no mapa"
            self.ab_desc2 = "durante 10 segundos que impide pasar"
            self.ab_desc3 = "a todos os enemigos"
            self.ab_desc4 = ""
        elif self.comander == "paper":
            self.ab_img = self.ab_paper
            self.ab_nome = "Interferencias electromagneticas"
            self.ab_desc1 = "Realiza un ataque en area que afecta a"
            self.ab_desc2 = "todas as celdas nun radio de 4,"
            self.ab_desc3 = "inflinxindo 10 puntos de dano a todos"
            self.ab_desc4 = "os enemigos que se atopen nela"
        elif self.comander == "scissors":
            self.ab_img = self.ab_scissors
            self.ab_nome = "Disparo de precision"
            self.ab_desc1 = "Realiza un forte disparo que afecta"
            self.ab_desc2 = "a unha soa celda do mapa inflinxindo"
            self.ab_desc3 = "200 puntos de dano"
            self.ab_desc4 = ""


    def update_pos(self, pos):
        result = [None, ""]
        if (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298):
            if (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80):
                self.hover = 1
            else:
                self.hover = 0
        else:
            self.hover = 0
        return result
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = ["",""]
        if (pos[0] > self.pos_panel2[0]+200) and (pos[0] < self.pos_panel2[0]+298) and\
                (pos[1] > self.pos_panel2[1]+40) and (pos[1] < self.pos_panel2[1]+80):
                result[0] = "cancel"
                result[1] = "to_state_0"

        elif pos[0] > 188 and pos[0] < 828+320 and pos[1] > 508:
            result[1] = "to_state_4"
        else:
            if occupied or self.reload_ab[1]:
                result[1] = "no_transition"
            else:
                result[0] = "attack"
                result[1] = "to_state_0"
        return result


    def draw(self, window, ab_counter):
        panel1 = self.panel1_desactivado
        panel2 = self.panel2_info_moving
        panel3 = self.panel3_desactivado

        window.blit(panel1, (self.pos_panel1))
        window.blit(panel2, (self.pos_panel2))
        window.blit(panel3, (self.pos_panel3))

        # Debuxar boton
        if self.hover:
            window.blit(self.cancel_hover, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))
        else:
            window.blit(self.cancel_desactivado, (self.pos_panel2[0]+200 ,self.pos_panel2[1]+40))

        # Debuxar informacion do panel2

        # Imaxe do tipo de abilidade
        window.blit(self.ab_img, (self.pos_panel2[0]+14, self.pos_panel2[1]+26))
        # Texto do panel2
        draw_text_2(self.ab_nome, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+68, self.pos_panel2[1]+28), window)
        draw_text_2(self.ab_desc1, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+20, self.pos_panel2[1]+96), window)
        draw_text_2(self.ab_desc2, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+20, self.pos_panel2[1]+110), window)
        draw_text_2(self.ab_desc3, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+20, self.pos_panel2[1]+124), window)
        draw_text_2(self.ab_desc4, self.PIXEL_TEXT, self.HUD_TEXT_COLOUR, (self.pos_panel2[0]+20, self.pos_panel2[1]+138), window)










class HUD:
    # Clase que representa a interfaz grafica integrada
   
    def __init__(self, comander, reload_ab=None):
        # Estado do HUD (por defecto o cero)
        self.comander = comander
        self.state = HUDStateZero(self.comander, reload_ab)
   
    
    def update_pos(self, pos, reload_ab):
        result = self.state.update_pos(pos)
        if result[1] == "to_state_1":
            self.state = HUDStateOne(result[0], self.comander, reload_ab)
        elif result[1] == "to_state_0":
            self.state = HUDStateZero(self.comander, reload_ab) 
    
    def click(self, pos, selected_tower, scrap, batteries, reload_ab, occupied=False):
        result = self.state.click(pos, selected_tower, scrap, batteries, reload_ab, occupied)

        # Cambia de estado
        if result[1] == "to_state_0":
            self.state = HUDStateZero(self.comander, reload_ab)
        elif result[1] == "to_state_1":
            self.state = HUDStateOne(selected_tower, self.comander, reload_ab)

        elif result[1] == "to_state_2":
            self.state = HUDStateTwo(result[0], self.comander)

        elif result[1] == "to_state_3":
            self.state = HUDStateThree(selected_tower, self.comander, reload_ab)
        
        elif result[1] == "to_state_4":
            self.state = HUDStateFour(selected_tower, self.comander, reload_ab)


        
        return result[0]

    def draw(self, window, ab_counter):
        self.state.draw(window, ab_counter)

    
    def is_clicked(self,pos):
        result = False
        if pos[0] > 188 and pos[0] < 828+320 and pos[1] > 508:
            result = True
        return result
