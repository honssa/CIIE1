import pygame
from towers.tower import Tower, TowerAlcance, TowerDano
from towers.moving_object import MovingTile, MovingRadius
from towers.barricade import Barricade
from enemies.enemy import Enemy, EnemyDead, EnemyVeloz, EnemyTank, EnemyBomb, EnemyEngeneer, EnemyVelozDead, EnemyTankDead, EnemyBombDead, EnemyEngeneerDead
from utils.grid import Grid
from utils.tileset import TileMap
from effects.effects import BombExplosion, ScissorsExplosion, PaperInterference
from menu.menu import TowerButton, HUD, HUDStatic
from gate.gate import Gate
from observers.EnemyDeathObserver import EnemyDeathObserver
import time
import random
import os
import math
from escena import Escena

# Constantes

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MATTE_BLACK = (20, 20, 20)
RED = (255, 0, 0, 100)
BLUE = (33, 150, 243)
LIGHT_BLUE = (0, 191, 255)
TRANSPARENT = (255,255,255,100)
SCREEN_WIDTH = 1340
SCREEN_HEIGHT = 700
TILESIZE = 32 #16 # 20
GRIDSIZE = (SCREEN_WIDTH // TILESIZE + 1, SCREEN_HEIGHT // TILESIZE + 1)



# Imaxes
pause_btn = pygame.image.load(os.path.join("Assets","pause_btn.png")).convert_alpha()
add_btn = pygame.image.load(os.path.join("Assets", "add_btn.png")).convert_alpha()
generic_btn = pygame.image.load(os.path.join("Assets", "generic_btn.png")).convert_alpha()
generic_btn_focus = pygame.image.load(os.path.join("Assets", "generic_btn_focus.png")).convert_alpha()
tower1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standard_twr1.png")).convert_alpha(), (64, 85))
tower2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "range_twr1.png")).convert_alpha(), (64, 85))
tower3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "dmg_twr1.png")).convert_alpha(), (64, 85))


class Scrap(EnemyDeathObserver):
    def __init__(self, value):
        self.value = value
    def notificar(self,obj):
        self.value += obj.chatarra
                

class Batteries(EnemyDeathObserver):
    def __init__(self, value):
        self.value = value
    def notificar(self,obj):
        if obj.name == "enxenheiro":
            if random.randrange(2) == 0:
                self.value += 1

class EnemyList(EnemyDeathObserver):
    def __init__(self):
        self.list = []
        self.dead_list = []
    def notificar(self,obj):
        if obj in self.list:
            self.list.remove(obj)

        if obj.name == 'basic':
            self.dead_list.append(EnemyDead(obj.X,obj.Y))
        elif obj.name == 'veloz':
            self.dead_list.append(EnemyVelozDead(obj.X,obj.Y))
        elif obj.name == 'tanque':
            self.dead_list.append(EnemyTankDead(obj.X,obj.Y))
        elif obj.name == 'bomba':
            self.dead_list.append(EnemyBombDead(obj.X,obj.Y))
        elif obj.name == 'enxenheiro':
            self.dead_list.append(EnemyEngeneerDead(obj.X,obj.Y))
            

class Camera:
        def __init__(self, x, y, MAP_BOUNDARIES):
            self.X = x
            self.Y = y
            self.MAP_BOUNDARIES = MAP_BOUNDARIES
        def up(self,pixels):
            if (-self.Y <= self.MAP_BOUNDARIES[2]-SCREEN_HEIGHT):
                self.Y -= pixels
                if (self.Y >= self.MAP_BOUNDARIES[2]-SCREEN_HEIGHT):
                    self.Y = self.MAP_BOUNDARIES[2]-SCREEN_HEIGHT
        def down(self,pixels):
            if (self.Y <= self.MAP_BOUNDARIES[1]):
                self.Y += pixels
                if (self.Y >= self.MAP_BOUNDARIES[1]):
                    self.Y = self.MAP_BOUNDARIES[1]
        def right(self,pixels):
            if (self.X <= self.MAP_BOUNDARIES[0]):
                self.X += pixels
                if (self.X >= self.MAP_BOUNDARIES[0]):
                    self.X = self.MAP_BOUNDARIES[0]
        def left(self,pixels):
            if (-self.X <= self.MAP_BOUNDARIES[3]-SCREEN_WIDTH):
                self.X -= pixels
                if (self.X >= self.MAP_BOUNDARIES[3]-SCREEN_WIDTH):
                    self.X = self.MAP_BOUNDARIES[3]-SCREEN_WIDTH

class Game(Escena):
    def __init__(self, director, map_1, stats):
        Escena.__init__(self, director)
        self.comander = stats["comander"]
        self.width = director.win.get_width()
        self.height = director.win.get_height()
        self.window = director.win
        self.towers = []
        self.barricades = []
        self.efectos = []
        self.enemies = EnemyList()
        self.dead_enemies = [] # Lista de enemigos mortos para executar animacion de morte
        self.timer = time.time()
        self.map = map_1
        self.GRIDSIZE = self.map.GRIDSIZE
        self.TILESIZE = self.map.TILESIZE
        self.grid = Grid(self.GRIDSIZE, self.TILESIZE) # O grid crease a partir do mapa
        self.MAP_BOUNDARIES = (0,0,self.GRIDSIZE[1] * self.TILESIZE[1], self.GRIDSIZE[0] * self.TILESIZE[0]) #Limites do mapa
        self.gates = []
        for gate in stats["gates"]:
            self.gates.append(Gate(self.grid, gate[0], gate[1]))

        self.map.record_obstacles(self.grid) # Carga obstaculos do mapa
        # Carga os percorridos polo que van os enemigos
        self.n_paths = stats["n_paths"]
        self.path = []
        for path_id in stats["paths_id"]:
            self.path.append(self.map.record_path(self.grid, path_id))
        
        self.map_img = self.map.make_map(self.grid)  # Surface (imaxe do mapa)
        self.map_rect = self.map_img[0].get_rect()
        
        self.tower1Button = TowerButton(generic_btn,generic_btn_focus,tower1, self.width - 200, self.height - 100, "example")
        self.tower2Button = TowerButton(generic_btn,generic_btn_focus,tower2, self.width - 300, self.height - 100, "example")
        self.tower3Button = TowerButton(generic_btn,generic_btn_focus,tower3, self.width - 400, self.height - 100, "example")
        self.cursor_sniper_img = pygame.image.load(os.path.join("Assets/cursors","sniper.png")).convert_alpha()
        self.cursor_sniper_img_hover = pygame.image.load(os.path.join("Assets/cursors","sniper2.png")).convert_alpha()
        self.cursor_basic = pygame.image.load(os.path.join("Assets/cursors","basic.png")).convert_alpha()
        self.reload_ab = [0,False]
        self.HUD = HUD(self.comander, self.reload_ab)
        
        self.gates_health = 100
        self.HUDStatic = HUDStatic(self.gates_health)
        self.moving_object = None
        self.chatarra = Scrap(stats["chatarra_inicial"])
        self.batteries = Batteries(stats["baterias_inicial"])
        self.std_tower_cost = 30
        self.rg_tower_cost = 40
        self.dmg_tower_cost = 50
        self.camera = Camera(stats["pos_camara_inicial"][0],stats["pos_camara_inicial"][1], self.MAP_BOUNDARIES)
        self.moving_obj_tower_type = 0
        self.selected_tower = None
        self.ability = False
        self.paper_stop = False
        self.enemies_captured = []
        self.derrota = False
        self.gate_dmged = False

        self.pos_mapa=(0, 0)
        self.pos=(0,0)
        self.camera_step=1

    
    def add_enemie(self, enemy):
        enemy.attachObserver(self.chatarra)
        enemy.attachObserver(self.batteries)
        enemy.attachObserver(self.enemies)
        self.enemies.list.append(enemy)

    
    def generate_enemy(self, enemy):
        if enemy[0] == "normal":
            e = Enemy(self.path[enemy[1]],self.grid)
        elif enemy[0] == "veloz":
            e = EnemyVeloz(self.path[enemy[1]],self.grid)
        elif enemy[0] == "bomba":
            e = EnemyBomb(self.path[enemy[1]],self.grid)
        elif enemy[0] == "tanque":
            e = EnemyTank(self.path[enemy[1]],self.grid)
        elif enemy[0] == "enxenheiro":
            e = EnemyEngeneer(self.path[enemy[1]],self.grid)

        self.add_enemie(e)


    # Funcion que aplica un dano fixo a todas as torres que se atopen nunha area
    def explosion(self, pos, radio, dmg):
        map_pos = self.grid.world_to_map(pos)
        hcells = self.grid.get_range_cells(map_pos, radio)
        for tower in self.towers:
            if self.grid.is_2_area_intersecting(hcells, tower.placement_cells):
                tower.health -= dmg
                if tower.health <= 0:
                    self.grid.free_cells(tower.placement_cells)
                    if self.selected_tower == tower:
                        self.selected_tower = None
                    tower.non_operative_status = "dead"
                    self.towers.remove(tower)
                    del tower




    def update(self, tiempo):
        self.pos = pygame.mouse.get_pos()      #Posición do mouse relativo a pantalla
        pos_0 = self.pos[0] - self.camera.X
        pos_1 = self.pos[1] - self.camera.Y
        self.pos_mapa = (pos_0,pos_1)          #Posición do mouse relativo ao MAPA

        # Actualizar posicion do cursor no HUD
        self.HUD.update_pos(self.pos, self.reload_ab)
        self.reload_ab[0]+=1
        if self.comander == "scissors":
            if self.reload_ab[1] and self.reload_ab[0] > 1200:
                self.reload_ab[0] = 0
                self.reload_ab[1] = False
        elif self.comander == "rock":
            if self.reload_ab[1] and self.reload_ab[0] > 3600:
                self.reload_ab[0] = 0
                self.reload_ab[1] = False
        elif self.comander == "paper":
            if self.reload_ab[1] and self.reload_ab[0] > 2400:
                self.reload_ab[0] = 0
                self.reload_ab[1] = False


        # Revisar se hai obxetos flotantes
        if self.moving_object:
            self.moving_object.move(self.pos_mapa[0], self.pos_mapa[1], self.grid)
            collide = False
            map_pos = self.grid.world_to_map(self.pos_mapa)
            # Revisar se hai colisions
            if self.moving_object.is_colliding(self.grid):
                collide = True
            if self.ability and self.comander == "scissors":
                if self.moving_object.detects_enemy(self.grid, self.enemies.list):
                    self.director.set_cursor_image(self.cursor_sniper_img_hover)
                else:
                    self.director.set_cursor_image(self.cursor_sniper_img)

        # bucle por cada enemigo
        if not self.paper_stop:
            for enemy in self.enemies.list:
                for gate in self.gates:
                    if enemy.checkForGate(gate,self.grid):
                        self.gates_health -= 10
                enemy.move(self.grid)
                enemy.ability(self.enemies, self.grid)
        
        if self.gates_health < self.gates_health and not self.gate_dmged:
            self.director.trigger_secreta = False

        if self.gates_health <= 0:
                self.derrota = True

        # bucle por cada torre atacante
        if not self.paper_stop:
            for tw in self.towers:
                tw.attack(self.enemies.list, self.window, self.grid)
                result = tw.updateProjectiles()
                if result:
                    pattern = self.grid.get_explosion_pattern(result[1],tw.area_exp)
                    self.efectos.append(BombExplosion(pattern,0.1))
        
        # bucle por cada torre en reparacion
        for tw in self.towers:
            if not tw.operativa and tw.non_operative_status == "repairing":
                tw.repair_counter += 1
                if tw.repair_counter > 60 and tw.health < tw.max_health:
                    tw.health += 1
                    tw.repair_counter = 0


        # Verifica se hai barricadas postas
        if len(self.barricades) > 0:
            self.barricades[0].update_barricade()
            if self.barricades[0].BARRICADE_counter > self.barricades[0].BARRICADE_TIME:
                self.grid.free_barricade_cells(self.barricades[0].placement_cells)
                self.barricades = []

        keys = pygame.key.get_pressed() 
        anykey = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]
        diagonal = keys[pygame.K_w] and keys[pygame.K_a] or keys[pygame.K_w] and keys[pygame.K_d]
        diagonal = diagonal or keys[pygame.K_s] and keys[pygame.K_a] or keys[pygame.K_s] and keys[pygame.K_d]
        if (not anykey):  
            self.camera_step = 1

        if (self.camera_step <= 8):
            self.camera_step += 0.18
        step = math.floor(self.camera_step)
        
        if (diagonal):
            step /= 1.4

        if keys[pygame.K_w]:
            #print(step)
            self.camera.down(step)
        if keys[pygame.K_s]:
            self.camera.up(step)
        if keys[pygame.K_a]:
            self.camera.right(step)
        if keys[pygame.K_d]:
            self.camera.left(step)

    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                map_pos = self.grid.world_to_map(self.pos_mapa)

                if self.ability:
                    if self.comander == "scissors":
                        action = self.HUD.click(self.pos, self.selected_tower, self.chatarra.value, self.batteries.value, self.reload_ab)
                        if action == "attack":
                            self.moving_object.attack_enemies_at_position(self.grid, self.enemies.list, 200)
                            self.efectos.append(ScissorsExplosion(self.pos_mapa[0], self.pos_mapa[1]))

                            self.director.set_cursor_image(self.cursor_basic)
                            self.ability = False
                            self.reload_ab[1] = True; self.reload_ab[0] = 0
                            self.moving_object = None
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None
                            
                        elif action == "cancel":
                            self.director.set_cursor_image(self.cursor_basic)
                            self.ability = False
                            self.moving_object = None
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None

                    elif self.comander == "paper":
                        action = self.HUD.click(self.pos, self.selected_tower, self.chatarra.value, self.batteries.value, self.reload_ab)
                        if action == "attack":
                            self.enemies_captured = self.moving_object.capture_enemies(self.grid, self.enemies.list)
                            self.efectos.append(PaperInterference(self.pos_mapa[0], self.pos_mapa[1]))
                            self.moving_object = None

                            self.paper_stop = True
                            self.reload_ab[1] = True; self.reload_ab[0] = 0
                            self.ability = False
                            self.reload_ab[1] = True
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None
                            
                        elif action == "cancel":
                            self.ability = False
                            self.moving_object = None
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None
                    
                    elif self.comander == "rock":
                        occupied = len(self.grid.get_barricade_colliding_tiles(map_pos)) > 0
                        action = self.HUD.click(self.pos, self.selected_tower, self.chatarra.value, self.batteries.value, self.reload_ab, occupied)
                        if action == "attack":
                            self.reload_ab[1] = True; self.reload_ab[0] = 0
                            self.ability = False
                            self.reload_ab[1] = True
                            self.grid.barricade_placement(map_pos)
                            self.barricades.append(self.moving_object)
                            self.moving_object.moving = False
                            self.moving_object = None
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None
                        elif action == "cancel":
                            self.ability = False
                            self.moving_object = None
                            if self.selected_tower:
                                self.selected_tower.selected = False
                                self.selected_tower = None

                           


                # Se estas cun obxeto flotante e clicas no grid
                elif self.moving_object:
                    # Se non e un lugar bloqueado
                    occupied = not (self.grid.is_cell_vacant(map_pos, self.moving_object))
                    action = self.HUD.click(self.pos, self.selected_tower, self.chatarra.value, self.batteries.value, self.reload_ab, occupied)
                    if action == "cancel_placement":
                        self.chatarra.value += self.selected_tower.cost_construction
                        self.moving_object.moving = False
                        self.moving_object = None
                        self.selected_tower = None
                    elif action == "confirm_placement":
                        self.grid.tower_placement(map_pos)
                        if not (type(self.moving_object) is Barricade):
                            self.towers.append(self.moving_object)
                        else:
                            self.barricades.append(self.moving_object)
                        self.towers.sort(key=lambda x: x.Y)
                        self.moving_object.moving = False
                        self.moving_object = None
                    else:
                        pass
                    
                else:
                    # Bucle que comproba se seleccionas unha torre
                    tower_clicked = [False, None]
                    for tower in self.towers:
                            if tower.is_clicked(map_pos[0], map_pos[1]):
                                tower_clicked[0] = True
                                tower_clicked[1] = tower
                                break

                    # Se clicaches nunha torre
                    if tower_clicked[0]:
                        # Se xa tinhas outra seleccionada
                        if self.selected_tower:
                            self.selected_tower.selected = False
                        self.selected_tower = tower_clicked[1]
                        tower.selected = True

                    
                    if (not tower_clicked[0]) and (self.selected_tower) and (not self.HUD.is_clicked(self.pos)):
                        self.selected_tower.selected = False
                        self.selected_tower = None

                    #clicar no HUD
                    action = self.HUD.click(self.pos, self.selected_tower, self.chatarra.value, self.batteries.value, self.reload_ab, False)
                    if action == "add_std_twr":
                        if self.selected_tower:
                            self.selected_tower.selected = False
                            self.selected_tower = None
                        self.add_tower(0)
                        self.chatarra.value -= self.std_tower_cost
                    elif action == "add_rg_twr":
                        if self.selected_tower:
                            self.selected_tower.selected = False
                            self.selected_tower = None
                        self.add_tower(1)
                        self.chatarra.value -= self.rg_tower_cost
                    elif action == "add_dmg_twr":
                        if self.selected_tower:
                            self.selected_tower.selected = False
                            self.selected_tower = None
                        self.add_tower(2)
                        self.chatarra.value -= self.dmg_tower_cost
                    elif action == "cancel_construction":
                        self.chatarra.value += self.selected_tower.cost_construction
                        self.grid.free_cells(self.selected_tower.placement_cells)
                        self.towers.remove(self.selected_tower)
                        self.selected_tower = None
                    elif action == "upgrade":
                        self.batteries.value -= 1
                        self.selected_tower.operativa = False
                        self.selected_tower.non_operative_status = "upgrading"
                    elif action == "repair":
                        self.chatarra.value -= self.selected_tower.repair_cost
                        self.selected_tower.operativa = False
                        self.selected_tower.non_operative_status = "repairing"
                    elif action == "reciclar":
                        self.chatarra.value += self.selected_tower.cost_construction
                        self.grid.free_cells(self.selected_tower.placement_cells)
                        self.towers.remove(self.selected_tower)
                        self.selected_tower = None
                    elif action == "ab_rock":
                        self.ability = True
                        self.add_barricade()
                    elif action == "ab_paper":
                        self.ability = True
                        self.moving_object = MovingRadius(self.pos_mapa, 4, self.grid)
                    elif action == "ab_scissors":
                        self.moving_object = MovingTile(self.pos_mapa[0], self.pos_mapa[1], self.grid)
                        self.director.set_cursor_image(self.cursor_sniper_img)
                        self.ability = True
                        
                    elif action == "cancel_ab":
                        pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    self.director.pauseGame()   


   

    def dibujar(self, window):

        draw_rect = self.map_rect.move(self.camera.X, self.camera.Y)
        # Esto e para que se debuxe o grid so cando hai unha torre flotante ou unha torre seleccionada
        if self.moving_object or self.selected_tower:
            window.blit(self.map_img[0], draw_rect)
        else:
            window.blit(self.map_img[1], draw_rect)


        pygame.draw.line(window, (241, 112, 21), (self.MAP_BOUNDARIES[0]+self.camera.X, self.MAP_BOUNDARIES[1]+self.camera.Y),(self.MAP_BOUNDARIES[0]+self.camera.X,self.MAP_BOUNDARIES[2]+self.camera.Y), 6)
        pygame.draw.line(window, (241, 112, 21), (self.MAP_BOUNDARIES[0]+self.camera.X, self.MAP_BOUNDARIES[1]+self.camera.Y),(self.MAP_BOUNDARIES[3]+self.camera.X,self.MAP_BOUNDARIES[1]+self.camera.Y), 6)
        pygame.draw.line(window, (241, 112, 21), (self.MAP_BOUNDARIES[0]+self.camera.X, self.MAP_BOUNDARIES[2]+self.camera.Y),(self.MAP_BOUNDARIES[3]+self.camera.X,self.MAP_BOUNDARIES[2]+self.camera.Y), 6)
        pygame.draw.line(window, (241, 112, 21), (self.MAP_BOUNDARIES[3]+self.camera.X, self.MAP_BOUNDARIES[1]+self.camera.Y),(self.MAP_BOUNDARIES[3]+self.camera.X,self.MAP_BOUNDARIES[2]+self.camera.Y), 6)

        for enemy in self.enemies.list:
            enemy.draw(window, self.camera)
        
        for dead_enemy in self.enemies.dead_list:
            if dead_enemy.draw(window, self.camera):
                self.enemies.dead_list.remove(dead_enemy)
                if dead_enemy.name == 'bomba':
                    self.explosion((dead_enemy.X, dead_enemy.Y),4,6)   # Posicion / Rango / Dano
                    pattern = self.grid.get_explosion_pattern((dead_enemy.X, dead_enemy.Y), 4) # Centro / radio
                    self.efectos.append(BombExplosion(pattern, 0.1))      # Patron / Retardo entre explosions
                del dead_enemy

        for tower in self.towers:
            tower.draw(window, self.grid, self.camera)

        for gate in self.gates:
            gate.draw(window,self.camera)
 
        for barricade in self.barricades:
            barricade.draw(window,self.grid,self.camera)

        for efecto in self.efectos:
            if efecto.podese_borrar:
                if not (self.comander == "scissors"):
                    self.moving_object = None
                self.paper_stop = False
                self.efectos.remove(efecto)
                self.enemies_captured = []
            else:
                result = efecto.draw(window, self.camera, self.grid)
                if result == "i_hit":
                    for enemy in self.enemies_captured:
                        enemy.hit(5)
                    
                

        if self.moving_object:
            self.moving_object.draw(window, self.grid, self.camera)

        # debuxa HUD
        self.HUD.draw(window, self.reload_ab[0])            
        
        self.HUDStatic.draw(window, self.chatarra.value, self.batteries.value, self.gates_health)   # E ESTO TAMEN
        

    def add_tower(self,tower):
        self.moving_obj_tower_type = tower
        x, y = pygame.mouse.get_pos()
        obj = None
        if (tower == 0):
            obj = Tower(x,y,self.grid, self.comander)
        elif (tower == 1):
            obj = TowerAlcance(x,y,self.grid, self.comander)
        elif (tower == 2):
            obj = TowerDano(x,y,self.grid, self.comander)
        self.moving_object = obj
        obj.moving = True
        self.selected_tower = obj
        self.selected_tower.selected = True


    def add_barricade(self):
        self.moving_obj_tower_type = 0
        x, y = pygame.mouse.get_pos()
        obj = Barricade(x,y,self.grid)
        self.moving_object = obj
        obj.moving = True

