import pygame
from towers.tower import Tower, TowerAlcance, TowerDano
import os
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Grid:
    def __init__(self, gridSize, tileSize):
        self.tileSize = tileSize
        self.gridSize = gridSize
        self.width = gridSize[0] * tileSize[0]
        self.height = gridSize[1] * tileSize[1]
        self.grid = np.zeros(gridSize)


    # Devolve as coordenadas do grid dadas as coordenadas xenerais
    def world_to_map(self, world_pos):
        map_pos_x = world_pos[0] // self.tileSize[0]
        map_pos_y = world_pos[1] // self.tileSize[1]
        return (int(map_pos_x), int(map_pos_y))
    

    # Devolve as coordenadas xenerais dadas as cordenadas da casilla do grid hola
    def map_to_world(self, map_pos):
        world_pos_x = (map_pos[0] * self.tileSize[0]) + (self.tileSize[0] // 2)
        world_pos_y = (map_pos[1] * self.tileSize[1]) + (self.tileSize[1] // 2)
        return (world_pos_x, world_pos_y)
    
    
    def map_to_world_cornered(self, map_pos):
        world_pos_x = map_pos[0] * self.tileSize[0]
        world_pos_y = map_pos[1] * self.tileSize[1]
        return (world_pos_x, world_pos_y)
    

    # Debuxa o grid na pantalla
    def draw(self, window):
        for x in range(self.gridSize[0]):
            # Linhas verticais
            vertical_line = pygame.Surface((1, self.height), pygame.SRCALPHA)
            vertical_line.fill((255, 255, 255, 100)) # You can change the 100 depending on what transparency it is.
            window.blit(vertical_line, (self.tileSize[0]*x, 0))
            #pygame.draw.line(window, WHITE, (self.tileSize[0]*x,0), (self.tileSize[0]*x,self.height), 1)

        for y in range(self.gridSize[1]):
            # Linhas horizontais
            horizontal_line = pygame.Surface((self.width, 1), pygame.SRCALPHA)
            horizontal_line.fill((255, 255, 255, 100)) # You can change the 100 depending on what transparency it is.
            window.blit(horizontal_line, (0, self.tileSize[1]*y))
            #pygame.draw.line(window, WHITE, (0,self.tileSize[1]*y), (self.width,self.tileSize[1]*y), 1)
    


    # Debuxa o grid na pantalla
    #def draw(self, window,camera):
    #    for x in range(self.gridSize[0]):
    #        pygame.draw.line(window, WHITE, (self.tileSize[0]*x+camera.X,0), (self.tileSize[0]*x+camera.X,self.height), 1)
    #
    #    for y in range(self.gridSize[1]):
    #        pygame.draw.line(window, WHITE, (0,self.tileSize[1]*y+camera.Y), (self.width,self.tileSize[1]*y+camera.Y), 1)
    

    # Devolve se un emisor nunha posicion "emissor_pos" (Vector2) en coordenadas do mundo
    # ten en rango a un obxetivo na posicion "target_pos" cun rango "tower_range" (Natural)
    def is_in_range(self, target_pos, emissor_pos, range_cells):
        target_cell = self.world_to_map(target_pos)
        return (list(target_cell) in range_cells)
    

    def is_cell_vacant(self, map_pos, object):
        result = False
        if isinstance(object, Tower):
            # Se estas nos limites do mapa
            boundarie_limits = (map_pos[0] == self.gridSize[0]-1) or \
                                    (map_pos[0] == 0) or \
                                        (map_pos[1] == self.gridSize[1]-1) or \
                                            (map_pos[1] == 0)
            # Revisa as 9 celdas do placement
            try:
                row1 = (self.grid[map_pos[0]-1, map_pos[1]-1] == 0) &\
                        ( self.grid[map_pos[0], map_pos[1]-1] == 0) &\
                            (self.grid[map_pos[0]+1, map_pos[1]-1] == 0)

                row2 = (self.grid[map_pos[0]-1, map_pos[1]] == 0) &\
                         (self.grid[map_pos[0], map_pos[1]] == 0) &\
                            (self.grid[map_pos[0]+1, map_pos[1]] == 0)

                row3 = (self.grid[map_pos[0]-1, map_pos[1]+1] == 0) &\
                         (self.grid[map_pos[0], map_pos[1]+1] == 0) &\
                            (self.grid[map_pos[0]+1, map_pos[1]+1] == 0)
                result = row1 & row2 & row3 & (not boundarie_limits)
            except IndexError:
                result = False
        else:
            result = self.grid[map_pos[0], map_pos[1]] == 0
        return result



    def is_cell_in_path(self, map_pos):
        if self.grid[map_pos[0]][map_pos[1]] == 2:
            return True 
        return False


    def path_placing(self, map_pos):
        self.grid[map_pos[0]][map_pos[1]] = 2


    def placement(self, map_pos):
        self.grid[map_pos[0], map_pos[1]] = 1
        self.grid[map_pos[0], map_pos[1]+1] = 1
        self.grid[map_pos[0], map_pos[1]-1] = 1
        if (map_pos[0] < self.gridSize[1]):
            self.grid[map_pos[0]+1, map_pos[1]] = 1
            self.grid[map_pos[0]+1, map_pos[1]-1] = 1
            if (map_pos[1] < self.gridSize[0]):
                self.grid[map_pos[0]+1, map_pos[1]+1] = 1
        self.grid[map_pos[0]-1, map_pos[1]] = 1
        self.grid[map_pos[0]-1, map_pos[1]-1] = 1
        self.grid[map_pos[0]-1, map_pos[1]+1] = 1

    
    def tower_placement(self, map_pos):
        # nove posicions 3x3
        self.grid[map_pos[0], map_pos[1]] = 1
        self.grid[map_pos[0], map_pos[1]+1] = 1
        self.grid[map_pos[0], map_pos[1]-1] = 1
        self.grid[map_pos[0]+1, map_pos[1]] = 1
        self.grid[map_pos[0]-1, map_pos[1]] = 1
        self.grid[map_pos[0]+1, map_pos[1]+1] = 1
        self.grid[map_pos[0]-1, map_pos[1]-1] = 1
        self.grid[map_pos[0]+1, map_pos[1]-1] = 1
        self.grid[map_pos[0]-1, map_pos[1]+1] = 1



    def barricade_placement(self, map_pos):
        # nove posicions 3x3
        self.grid[map_pos[0], map_pos[1]] = 3
        self.grid[map_pos[0], map_pos[1]+1] = 3
        self.grid[map_pos[0], map_pos[1]-1] = 3
        self.grid[map_pos[0]+1, map_pos[1]] = 3
        self.grid[map_pos[0]-1, map_pos[1]] = 3
        self.grid[map_pos[0]+1, map_pos[1]+1] = 3
        self.grid[map_pos[0]-1, map_pos[1]-1] = 3
        self.grid[map_pos[0]+1, map_pos[1]-1] = 3
        self.grid[map_pos[0]-1, map_pos[1]+1] = 3

    def is_barricade(self, map_pos):
        return self.grid[map_pos[0]][map_pos[1]] == 3
    


    # Pon unha SOA casilla a 1 no grid
    def single_placement(self, map_pos):
        self.grid[map_pos[0], map_pos[1]] = 1
    



    def get_placement_cells(self, map_pos):
        placement_cells = []
        placement_cells.append(list((map_pos[0],map_pos[1])))
        placement_cells.append(list((map_pos[0],map_pos[1]+1)))
        placement_cells.append(list((map_pos[0],map_pos[1]-1)))
        placement_cells.append(list((map_pos[0]+1,map_pos[1])))
        placement_cells.append(list((map_pos[0]-1,map_pos[1])))
        placement_cells.append(list((map_pos[0]+1,map_pos[1]+1)))
        placement_cells.append(list((map_pos[0]-1,map_pos[1]-1)))
        placement_cells.append(list((map_pos[0]+1,map_pos[1]-1)))
        placement_cells.append(list((map_pos[0]-1,map_pos[1]+1)))

        # Facer un movemento de todas as tiles -1, -1 (offset)
        #for cell in placement_cells:
        #    cell[0] += -1
        #    cell[1] += -1
        return placement_cells


    # Converte unha lista de listas nun conxunto de tuplas
    def convert_to_tuple_set(self, lista):
        result = set()
        for element in lista:
            result.add((element[0], element[1]))
        return result


    # devolve True se interseccionan e False se non interseccionan
    def is_2_area_intersecting(self, list1, list2):
        set1 = self.convert_to_tuple_set(list1)
        set2 = self.convert_to_tuple_set(list2)

        return not (len(set1.intersection(set2)) == 0)



    def get_range_cells(self, map_pos, tower_range):
        placement_cells = set()
        placement_cells.add(map_pos)
        placement_cells.add((map_pos[0],map_pos[1]))
        placement_cells.add((map_pos[0],map_pos[1]+1))
        placement_cells.add((map_pos[0],map_pos[1]-1))
        placement_cells.add((map_pos[0]+1,map_pos[1]))
        placement_cells.add((map_pos[0]-1,map_pos[1]))
        placement_cells.add((map_pos[0]+1,map_pos[1]+1))
        placement_cells.add((map_pos[0]-1,map_pos[1]-1))
        placement_cells.add((map_pos[0]+1,map_pos[1]-1))
        placement_cells.add((map_pos[0]-1,map_pos[1]+1))

        cells = placement_cells.copy()
        
        for i in range(tower_range):
            tmp_cells = set()
            for cell in cells:
                tmp_cells.add((cell[0] + 1, cell[1]))
                tmp_cells.add((cell[0], cell[1] + 1))
                tmp_cells.add((cell[0] - 1, cell[1]))
                tmp_cells.add((cell[0], cell[1] - 1))
            cells = cells.union(tmp_cells)
        
        cells = cells - placement_cells

        range_cells = []
        for cell in cells:
            range_cells.append(list(cell))
        return range_cells

    

    def get_tower_colliding_tiles(self, map_pos):
        placement_cells = self.get_placement_cells(map_pos)
        colliding_tiles = []
        for cell in placement_cells:
            if not self.is_cell_vacant(cell, None):
                colliding_tiles.append(cell)
        return colliding_tiles
    



    def get_barricade_colliding_tiles(self, map_pos):
        placement_cells = self.get_placement_cells(map_pos)
        colliding_tiles = []
        for cell in placement_cells:
            if not self.is_cell_in_path(cell):
                colliding_tiles.append(cell)
        return colliding_tiles   
    



    def free_cells(self, cells):
        for cell in cells:
            self.grid[cell[0], cell[1]] = 0


    
    def free_barricade_cells(self, cells):
        for cell in cells:
            self.grid[cell[0], cell[1]] = 2


    # Comproba se pos2 esta nalgunha das 4 celdas adxacentes de pos1
    def is_in_4_adjacent(self, pos1, pos2):
        result = False
        if (pos1[0] == pos2[0] and pos1[1]-1 == pos2[1]) or\
                (pos1[0] == pos2[0] and pos1[1]+1 == pos2[1]) or\
                    (pos1[1] == pos2[1] and pos1[0]-1 == pos2[0]) or\
                        (pos1[1] == pos2[1] and pos1[0]+1 == pos2[0]):
            result = True
        return result




    def get_4_adjacent(self, center):
        result = set()
        result.add((center[0]+1,center[1]))
        result.add((center[0]-1,center[1]))
        result.add((center[0],center[1]+1))
        result.add((center[0],center[1]-1))
        return result
    


    def get_8_adjacent(self,center):
        result = set()
        result.add((center[0]+1,center[1]))
        result.add((center[0]-1,center[1]))
        result.add((center[0],center[1]+1))
        result.add((center[0],center[1]-1))

        result.add((center[0]+1,center[1]+1))
        result.add((center[0]+1,center[1]-1))
        result.add((center[0]-1,center[1]+1))
        result.add((center[0]-1,center[1]-1))
        
        return result
        

    def get_explosion_pattern(self, center, radio):
        pattern = [] # Patron de explosion lista de listas
        capas = [] # Capas (segun radio (funciona como o get range cells)) lista de conxuntos
        center = self.world_to_map(center)
        if radio == 0: # soamente o centro da explosion
            pattern.append([center])
        elif radio == 1:
            pattern.append([center])
            pattern.append(list(self.get_4_adjacent(center)))
        elif radio > 2:
            pattern.append([center])
            pattern.append(list(self.get_4_adjacent(center)))
            tmp = set(); tmp.add(center)
            capas.append(tmp)
            tmp = self.get_4_adjacent(center); tmp.add(center)
            capas.append(tmp)

            for x in range(2, radio, 1):
                cells = set()
                for element in capas[x-2]:
                    aux = self.get_8_adjacent(element)
                    cells = cells.union(aux)
                cells_d = cells - capas[x-1]
                pattern.append(list(cells_d)) #2

                cells1 = set()
                cells2 = set()
                for element in capas[x-1]:
                    cells1 = cells1.union(self.get_4_adjacent(element))
                for element in capas[x-2]:
                    cells2 = cells2.union(self.get_8_adjacent(element))
                pattern.append(list(cells1.difference(cells2))) #3
                capas.append(cells1)

        return pattern
