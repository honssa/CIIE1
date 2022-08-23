import pygame
import os
import math
import abc

class MovingObject(pygame.sprite.Sprite):
    def __init__(self,X,Y,grid):
        pygame.sprite.Sprite.__init__(self)
        self.X = X
        self.Y = Y 
        self.moving = False # Se esta flotante non executa a animacion

        self.placement_cells = grid.get_placement_cells(grid.world_to_map((self.X, self.Y)))
        self.collision_cells = []


    @abc.abstractmethod
    def draw(self, window, grid,camera):
        pass

    # Move un obxeto a unha coordenada (x,y)
    def move(self, x, y, grid):
        map_pos = grid.world_to_map((x,y))
        world_pos = grid.map_to_world(map_pos)

        old_map_pos = grid.world_to_map((self.X, self.Y))
        mov_horizontal = map_pos[0] - old_map_pos[0]
        mov_vertical = map_pos[1] - old_map_pos[1]

        self.X = world_pos[0] 
        self.Y = world_pos[1]

        # Mover as celdas de rango tamen
        for cell in self.range_cells:
            cell[0] += mov_horizontal
            cell[1] += mov_vertical
        
        # Mover as celdas de placement
        for cell in self.placement_cells:
            cell[0] += mov_horizontal
            cell[1] += mov_vertical
            #print("CELDA: " + str(cell) )

    def is_colliding(self, grid):
        map_pos = grid.world_to_map((self.X, self.Y))
        result = grid.get_tower_colliding_tiles(map_pos)
        #print("COLISIONS: " + str(result))
        self.collision_cells = result
        return len(result) > 0

    def is_clicked(self, X, Y):
        # recibe coordenadas do mapa
        # Devolve se o obxecto foi clicado
        return [X,Y] in self.placement_cells




class MovingTile(MovingObject):
    def __init__(self,X,Y,grid):
        self.X = X
        self.Y = Y 
        self.moving = False # Se esta flotante non executa a animacion
        self.placement_cells = [list(grid.world_to_map((self.X, self.Y)))]


    def draw(self, window, grid, camera):
        box_surface = pygame.Surface((grid.tileSize[0],grid.tileSize[1]), pygame.SRCALPHA)        
        box_surface.fill((200,200,200, 100))
        for cell in self.placement_cells:
            pos = grid.map_to_world_cornered(cell)
            window.blit(box_surface, (pos[0]+camera.X, pos[1]+camera.Y))
    

    def detects_enemy(self, grid, enemies):
        #print(self.placement_cells)
        for enemy in enemies:
            map_pos = grid.world_to_map((enemy.X, enemy.Y))
            if grid.is_2_area_intersecting([map_pos], self.placement_cells):
                return True
        return False
    
    def attack_enemies_at_position(self, grid, enemies, dmg):
        for enemy in enemies:
            map_pos = grid.world_to_map((enemy.X, enemy.Y))
            if grid.is_2_area_intersecting([map_pos], self.placement_cells):
                enemy.hit(dmg)



    def move(self, x, y, grid):
        map_pos = grid.world_to_map((x,y))
        world_pos = grid.map_to_world(map_pos)

        old_map_pos = grid.world_to_map((self.X, self.Y))
        mov_horizontal = map_pos[0] - old_map_pos[0]
        mov_vertical = map_pos[1] - old_map_pos[1]

        self.X = world_pos[0] 
        self.Y = world_pos[1]
        
        # Mover as celdas de placement
        for cell in self.placement_cells:
            cell[0] += mov_horizontal
            cell[1] += mov_vertical




class MovingRadius(MovingTile):
    def __init__(self,center,rad,grid):
        self.X = center[0]
        self.Y = center[1] 
        self.moving = False # Se esta flotante non executa a animacion
        self.placement_cells = grid.get_range_cells(grid.world_to_map(center), rad) + grid.get_placement_cells(grid.world_to_map(center))
        #self.enemies_captured = []


    def capture_enemies(self, grid, enemies):
        enemies_captured = []
        for enemy in enemies:
            map_pos = grid.world_to_map((enemy.X, enemy.Y))
            if grid.is_2_area_intersecting([map_pos], self.placement_cells):
                enemies_captured.append(enemy)
        return enemies_captured

