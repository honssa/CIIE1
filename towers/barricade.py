import pygame
import os
import math
from observers.EnemyDeathObserver import EnemyDeathObserver
from towers.moving_object import MovingObject
from towers.projectile import Projectile

TRANSPARENT = (255, 255, 255, 100)

class Focus(EnemyDeathObserver):
    def __init__(self):
        self.enemy = None
    def notificar(self,obj):
        self.enemy = None

class Barricade(MovingObject):
    def __init__(self, X, Y, grid):
        # Invocamos ao constructor da clase pai
        super().__init__(X,Y,grid)

        self.image1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/barricade", "barricade.png")).convert_alpha(), (grid.tileSize[0]*3, grid.tileSize[1]*4))
        # Posicion do sprite
        self.rect = self.image1.get_rect()
        self.rect.centerx = self.X
        self.rect.centery = self.Y

        # Outros atributos
        #self.tower_imgs = [] Esto sera necesario para facer animacions
        self.tw_range = 4
        self.dmg = 2
        self.inRange = False
        self.cadence = 30 # tempo de retardo entre disparos
        self.timer = 0
        self.focus = Focus()
        self.place_color = TRANSPARENT

        self.range_cells = grid.get_range_cells(grid.world_to_map((self.rect.centerx, self.rect.centery)), self.tw_range)

        self.selected = False

        self.projectiles = []
        self.BARRICADE_TIME = 600
        self.BARRICADE_counter = 0
        self.bg_healthbar = pygame.image.load(os.path.join("Assets/HUD", "health_bar_info.png")).convert_alpha()

 
    def is_colliding(self, grid):
        map_pos = grid.world_to_map((self.X, self.Y))
        result = grid.get_barricade_colliding_tiles(map_pos)
        self.collision_cells = result
        return len(result) > 0


    def draw(self, window, grid,camera):
        if self.inRange:
            self.timer += 1
            if self.timer > 30:
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
        self.draw_health_bar(window)



    def draw_health_bar(self, window):
        length = 74
        move_by = self.BARRICADE_counter / self.BARRICADE_TIME
        time_bar = length - round(move_by * length)
        pygame.draw.rect(window, (44, 54, 52), (self.rect.x+12, self.rect.y-47, length, 6), 0)
        pygame.draw.rect(window, (191,228,230), (self.rect.x+12,self.rect.y-47, time_bar, 6), 0)



    def update_barricade(self):
        self.BARRICADE_counter += 1

        
        
    def draw_tower(self,window):
        window.blit(self.image1, (self.rect.x,self.rect.y-16))



    def draw_radius(self, window, grid, camera):
        placement_surface = pygame.Surface((grid.tileSize[0],grid.tileSize[1]), pygame.SRCALPHA)
        
        for cell in self.placement_cells:
            pos = grid.map_to_world_cornered(cell)
            if cell in self.collision_cells:
                placement_surface.fill((255, 0, 0, 100))
            else:
                placement_surface.fill((128,128,128, 100))
            window.blit(placement_surface, (pos[0]+camera.X, pos[1]+camera.Y))