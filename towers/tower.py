import pygame
import os
import math
from observers.EnemyDeathObserver import EnemyDeathObserver
from towers.moving_object import MovingObject
from towers.projectile import Projectile, ArtilleryProjectile

TRANSPARENT = (255, 255, 255, 100)


class Focus(EnemyDeathObserver):
    def __init__(self):
        self.enemy = None
    def notificar(self,obj):
        self.enemy = None

class Tower(MovingObject):
    def __init__(self, X, Y, grid, comander):
        # Invocamos ao constructor da clase pai
        super().__init__(X,Y,grid)

        self.image2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "range_twr1.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.image3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "dmg_twr1.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        # Torre 2x3
        self.image1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standard_twr1.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        # Imaxes das torres non operativas
        self.image0_std = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standard_twr0.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.image0_rg = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "range_twr0.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.image0_dmg = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "dmg_twr0.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        
        # Imaxes das torres melloradas
        self.standard_twr2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standard_twr2.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.standard_twr3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standard_twr3.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))

        self.range_twr2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "range_twr2.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.range_twr3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "range_twr3.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))

        self.dmg_twr2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "dmg_twr2.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))
        self.dmg_twr3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "dmg_twr3.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*5))

        self.repair_icon = pygame.image.load(os.path.join("Assets/HUD", "build_repair.png"))
        

        # Posicion do sprite
        self.rect = self.image1.get_rect()
        self.rect.centerx = self.X
        self.rect.centery = self.Y

        # Outros atributos
        #self.tower_imgs = [] Esto sera necesario para facer animacions
        self.tw_range = 5
        self.dmg = 2
        self.inRange = False
        self.cadence = 15 # tempo de retardo entre disparos
        self.timer = 0
        self.multipleFocus = []
        self.maxFocus = 1
        self.focus = Focus()
        self.place_color = TRANSPARENT
        self.type = "std"
        self.cost_construction = 30      # coste en chatarra da torre
        self.upgrade_cost1 = 50          # coste para mellorala a nivel 2
        self.upgrade_cost2 = 100         # coste para mellorala a nivel 3
        self.repair_cost = 20            # coste para reparar unha torre
        self.max_health = 30
        self.health = 30
        self.tempo_construccion = 300 # 3 segundos
        self.tempo_reparacion = 600 # 10 segundos
        self.counter_build = 0
        self.repair_counter = 0
        self.operativa = False  # Comeza sendo non operativa
        self.non_operative_status = "building" # building / upgrading / repairing / dead
        self.nivel = 1
        self.comander = comander

        # Cousa das habilidades pasivas
        if self.comander == "rock":
            self.max_health += 20
            self.health += 20
            self.dmg += 1
        elif self.comander == "scissors":
            self.tempo_construccion = 100
            self.tempo_reparacion = 200
            self.tw_range += 1
        elif self.comander == "paper":
            self.max_health += 10
            self.health += 10
            self.tempo_construccion = 200
            self.tempo_reparacion = 400 
        self.range_cells = grid.get_range_cells(grid.world_to_map((self.rect.centerx, self.rect.centery)), self.tw_range)

        self.selected = False

        self.projectiles = []
        self.std_sound = pygame.mixer.Sound("Sounds/novos/tower_std_shoot_demberz.ogg") 

 


    def draw(self, window, grid,camera):
        if self.inRange:
            self.timer += 1
            if self.timer > self.cadence:
                self.timer = 0
        else:
            self.timer = 0

        self.rect.centerx = self.X + camera.X
        self.rect.centery = self.Y + camera.Y
        
        if self.moving or self.selected:
            self.draw_radius(window,grid,camera)


        for p in self.projectiles:
            p.draw(window,camera)
        self.draw_tower(window)


    def upgrade(self):
        if self.nivel < 3:
            self.nivel += 1
        if self.nivel == 2:
            self.maxFocus = 2
            self.dmg = 3
            self.max_health = 40
            self.health = 40
            self.cadence = 12
        elif self.nivel == 3:
            self.maxFocus = 3
            self.dmg = 4
            self.max_health = 50
            self.health = 50
            self.cadence = 10
       
        
    def draw_tower(self,window):
        if self.operativa or self.moving:
            if self.nivel == 1:
                window.blit(self.image1, (self.rect.x,self.rect.y-32))
            elif self.nivel == 2:
                window.blit(self.standard_twr2, (self.rect.x,self.rect.y-32))
            elif self.nivel == 3:
                window.blit(self.standard_twr3, (self.rect.x,self.rect.y-32))

        else:
            self.counter_build += 1
            if self.non_operative_status=="repairing":
                if self.nivel == 1:
                    window.blit(self.image1, (self.rect.x,self.rect.y-32))
                elif self.nivel == 2:
                    window.blit(self.standard_twr2, (self.rect.x,self.rect.y-32))
                elif self.nivel == 3:
                    window.blit(self.standard_twr3, (self.rect.x,self.rect.y-32))
                window.blit(self.repair_icon, (self.rect.x+24, self.rect.y+56))
                if self.counter_build >= self.tempo_reparacion:
                    self.counter_build = 0
                    self.operativa = True
                return
            else:
                window.blit(self.image0_std, (self.rect.x,self.rect.y-32))
            if self.counter_build >= self.tempo_construccion:
                if self.non_operative_status == "upgrading":
                    self.upgrade()


                self.counter_build = 0
                self.operativa = True

    def draw_radius(self, window, grid, camera):    #---------------Antigua funcion de debuxar radio
        box_surface = pygame.Surface((grid.tileSize[0],grid.tileSize[1]), pygame.SRCALPHA)        
        box_surface.fill((200,200,200, 100))
        for cell in self.range_cells:
            pos = grid.map_to_world_cornered(cell)
            window.blit(box_surface, (pos[0]+camera.X, pos[1]+camera.Y))


        placement_surface = pygame.Surface((grid.tileSize[0],grid.tileSize[1]), pygame.SRCALPHA)
        
        for cell in self.placement_cells:
            pos = grid.map_to_world_cornered(cell)
            if cell in self.collision_cells:
                placement_surface.fill((255, 0, 0, 100))
            else:
                placement_surface.fill((14, 71, 194, 100))
            window.blit(placement_surface, (pos[0]+camera.X, pos[1]+camera.Y))
    

    def is_duplicado(self, enemy):
        for focus in self.multipleFocus:
            if focus.enemy == enemy:
                return True
        return False

    
    def attack(self, enemies, window, grid):
        #self.inRange = False
        enemy_closest = []
        chatarra = 0
        if not self.operativa:
            return 0

        # Por cada focus mira se segue en rango
        # Senon esta quitao da lista 
        for focus in self.multipleFocus:
            if not self.isinrange(focus.enemy, grid):
                self.multipleFocus.remove(focus)
                del focus

        # Se tes menos focuses dos maximos
        # engade novos focuses se os hai ata que chegues ao maximo
        if len(self.multipleFocus) < self.maxFocus:
            for enemy in enemies:
                if self.isinrange(enemy, grid) and (not self.is_duplicado(enemy)):
                    enemy_closest.append(enemy)
            if enemy_closest:
                enemy_dir = enemy_closest[0].path[enemy_closest[0].segment]["dir"]
                if enemy_dir == (1,0):
                    enemy_closest.sort(key=lambda x: x.X)
                elif enemy_dir == (-1,0):
                    enemy_closest.sort(key=lambda x: x.X)
                    enemy_closest = enemy_closest[::-1]
                elif enemy_dir == (0,1):
                    enemy_closest.sort(key=lambda x: x.Y)
                elif enemy_dir == (0,-1):
                    enemy_closest.sort(key=lambda x: x.Y)
                    enemy_closest = enemy_closest[::-1]

            while(len(enemy_closest) > 0 and len(self.multipleFocus) < self.maxFocus):
                f = Focus(); f.enemy = enemy_closest.pop(0)
                f.enemy.attachObserver(f)
                self.multipleFocus.append(f)

        
        # Disparalle a todos os focuses
        if self.timer == self.cadence:
            self.std_sound.play()
            for focus in self.multipleFocus:
                self.projectiles.append(Projectile(self.X,self.Y,20,focus.enemy,self.dmg))
        


    def isinrange(self, enemy, grid):    #Antigua función de detectar se enemigo esta en rango
        if not enemy:
            return False

        enemy_pos = (enemy.X, enemy.Y)
        tower_pos = (self.X, self.Y)

        if grid.is_in_range(enemy_pos, tower_pos, self.range_cells):
            self.inRange = True
            return True
        return False


    def updateProjectiles(self):
        for p in self.projectiles:
            if (not p.update()):  #Devolve falso se por calquer motivo o proyectil deberia de deixar de existir
                self.projectiles.remove(p)




class TowerAlcance(Tower):
    def __init__(self, X, Y, grid, comander):
        super().__init__(X,Y,grid, comander)
        self.tw_range = 9
        self.dmg = 30
        self.area_dmg = 5
        self.area_exp = 1
        self.cost_construction = 40      # coste en chatarra da torre
        self.type = "rg"
        self.cadence = 120 # tempo de retardo entre disparos
        self.sound_alc = pygame.mixer.Sound("Sounds/novos/range_tower_shoot_jalastram.ogg")
        self.comander = comander
        if self.comander == "scissors":
            self.tempo_construccion = 100
            self.tempo_reparacion = 200
            self.tw_range += 1
        self.range_cells = grid.get_range_cells(grid.world_to_map((self.rect.centerx, self.rect.centery)), self.tw_range)

        # Cousa das habilidades pasivas
        #if self.comander == "rock":
        #    self.max_health += 20
        #    self.health += 20
        #    self.dmg += 1
        #elif self.comander == "scissors":
        #    self.tempo_construccion = 100
        #    self.tempo_reparacion = 200
        #    self.tw_range += 1
        #elif self.comander == "paper":
        #    self.max_health += 10
        #    self.health += 10
        #    self.tempo_construccion = 200
        #    self.tempo_reparacion = 400 


    def draw_tower(self,window):
        if self.operativa or self.moving:
            if self.nivel == 1:
                window.blit(self.image2, (self.rect.x,self.rect.y-32))
            elif self.nivel == 2:
                window.blit(self.range_twr2, (self.rect.x,self.rect.y-32))
            elif self.nivel == 3:
                window.blit(self.range_twr3, (self.rect.x,self.rect.y-32))
        else:
            self.counter_build += 1
            if self.non_operative_status=="repairing":
                if self.nivel == 1:
                    window.blit(self.image2, (self.rect.x,self.rect.y-32))
                elif self.nivel == 2:
                    window.blit(self.range_twr2, (self.rect.x,self.rect.y-32))
                elif self.nivel == 3:
                    window.blit(self.range_twr3, (self.rect.x,self.rect.y-32))
                window.blit(self.repair_icon, (self.rect.x+24, self.rect.y+56))
                if self.counter_build >= self.tempo_reparacion:
                    self.counter_build = 0
                    self.operativa = True
                return
            else:
                window.blit(self.image0_rg, (self.rect.x,self.rect.y-32))
            if self.counter_build >= self.tempo_construccion:
                if self.non_operative_status == "upgrading":
                    self.upgrade()
                self.counter_build = 0
                self.operativa = True


    # Ataca a enemigos de mais vida dentro do seu rango prioritariamente
    # xenera unha explosion que dana aos enemigos nas 4 celdas adxacentes
    # cadencia: baixa, dano: alto, rango: alto
    def attack(self, enemies, window, grid):
        enemy_closest = []
        enemies_in_radius = []
        chatarra = 0
        if not self.operativa:
            return 0
        # Se existe focus e esta en rango -> atacar
        if self.isinrange(self.focus.enemy, grid):
            if self.timer == self.cadence:
                self.sound_alc.play()
                target_pos = grid.world_to_map((self.focus.enemy.X, self.focus.enemy.Y))
                # Buscar enemigos na area
                for enemy in enemies:
                    map_pos = grid.world_to_map((enemy.X,enemy.Y))
                    area = grid.get_range_cells(target_pos, self.area_exp)
                    if grid.is_2_area_intersecting([map_pos], area):
                        enemies_in_radius.append(enemy)
 
                # display animation
                self.projectiles.append(ArtilleryProjectile(self.X,self.Y,20,self.focus.enemy,self.dmg,enemies_in_radius,self.area_dmg))

        # Senon existe focus buscar un e atacar
        else:
            self.focus.enemy = None
            for enemy in enemies:
                if self.isinrange(enemy, grid):
                    enemy_closest.append(enemy)
            
            if enemy_closest:
                enemy_closest.sort(key=lambda x: x.max_health)
                enemy_closest = enemy_closest[::-1]

            if len(enemy_closest) > 0:
                self.focus.enemy = enemy_closest[0]
                self.focus.enemy.attachObserver(self.focus)
    
    def updateProjectiles(self):
        for p in self.projectiles:
            if (not p.update()):  #Devolve falso se por calquer motivo o proyectil deberia de deixar de existir
                self.projectiles.remove(p)
                return [True, (p.actualX, p.actualY)]
    
    def upgrade(self):
        if self.nivel < 3:
            self.nivel += 1
        if self.nivel == 2:
            self.dmg = 40
            self.area_dmg = 10
            self.area_exp = 3
            self.max_health = 40
            self.health = 40
            self.cadence = 110
        elif self.nivel == 3:
            self.dmg = 50
            self.area_dmg = 15
            self.area_exp = 4
            self.max_health = 50
            self.health = 50
            self.cadence = 100


        



class TowerDano(Tower):
    def __init__(self, X, Y, grid, comander):
        super().__init__(X,Y,grid, comander)
        self.tw_range = 3
        self.dmg = 0.5
        self.cadence = 20
        self.ctd = 0
        self.cost_construction = 50      # coste en chatarra da torre
        self.type = "dmg"
        self.enemies_in_radius = []
        self.dmg_soung = pygame.mixer.Sound("Sounds/novos/dmg_tower_shoot_celestialghost8.ogg")

        self.comander = comander
        if self.comander == "scissors":
            self.tempo_construccion = 100
            self.tempo_reparacion = 200
            self.tw_range += 1
        self.range_cells = grid.get_range_cells(grid.world_to_map((self.rect.centerx, self.rect.centery)), self.tw_range)

        # Cousa das habilidades pasivas
        #if self.comander == "rock":
        #    self.max_health += 20
        #    self.health += 20
        #    self.dmg += 1
        #elif self.comander == "scissors":
        #    self.tempo_construccion = 100
        #    self.tempo_reparacion = 200
        #    self.tw_range += 1
        #elif self.comander == "paper":
        #    self.max_health += 10
        #    self.health += 10
        #    self.tempo_construccion = 200
        #    self.tempo_reparacion = 400 
   


    def draw_tower(self,window):
        if self.operativa or self.moving:
            if self.nivel == 1:
                window.blit(self.image3, (self.rect.x,self.rect.y-32))
            elif self.nivel == 2:
                window.blit(self.dmg_twr2, (self.rect.x,self.rect.y-32))
            elif self.nivel == 3:
                window.blit(self.dmg_twr3, (self.rect.x,self.rect.y-32))
        else:
            self.counter_build += 1
            if self.non_operative_status=="repairing":
                if self.nivel == 1:
                    window.blit(self.image1, (self.rect.x,self.rect.y-32))
                elif self.nivel == 2:
                    window.blit(self.standard_twr2, (self.rect.x,self.rect.y-32))
                elif self.nivel == 3:
                    window.blit(self.standard_twr3, (self.rect.x,self.rect.y-32))
                window.blit(self.repair_icon, (self.rect.x+24, self.rect.y+56))
                if self.counter_build >= self.tempo_reparacion:
                    self.counter_build = 0
                    self.operativa = True
                return
            else:
                window.blit(self.image0_dmg, (self.rect.x,self.rect.y-32))

            if self.counter_build >= self.tempo_construccion:
                if self.non_operative_status == "upgrading":
                    self.upgrade()
                self.counter_build = 0
                self.operativa = True
            
    

    def is_enemy_registered(self, enemy):
        result = -1
        for i in range(len(self.enemies_in_radius)):
            if self.enemies_in_radius[i][0] == enemy:
                result = i
        return result

    # Ataca a todos os enemigos no seu rango
    # dano: acumulativa, rango: baixo
    # Non crea proxectiles
    def attack(self, enemies, window, grid):
        self.focus = None
        chatarra = 0
        if not self.operativa:
            return 0

        self.ctd += 1
        if self.ctd % self.cadence == 0:
            for enemy in enemies:
                e_pos = grid.world_to_map((enemy.X,enemy.Y))
                in_area = grid.is_2_area_intersecting([e_pos], self.range_cells)
                index_enemy = self.is_enemy_registered(enemy)
                if in_area and (index_enemy > -1):
                    self.enemies_in_radius[index_enemy][1] += self.dmg
                    self.dmg_soung.set_volume(0.05)
                    self.dmg_soung.play()
                    enemy.hit(self.enemies_in_radius[index_enemy][1])
                elif in_area:
                    self.enemies_in_radius.append([enemy,0])
                elif (not in_area) and (index_enemy > -1):
                    del self.enemies_in_radius[index_enemy]

    def upgrade(self):
        if self.nivel < 3:
            self.nivel += 1
        if self.nivel == 2:
            self.dmg = 0.7
            self.cadence = 17
            self.max_health = 40
            self.health = 40
        elif self.nivel == 3:
            self.dmg = 1.2
            self.cadence = 14
            self.max_health = 50
            self.health = 50
    
