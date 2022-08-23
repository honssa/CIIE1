import pygame
import pytmx
import configparser
import os




class TileMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * (tm.tilewidth * 2)
        self.height = tm.height * (tm.tileheight * 2)
        self.GRIDSIZE = (tm.width, tm.height)
        self.TILESIZE = (tm.tilewidth * 2, tm.tileheight * 2)
        self.tmxdata = tm
        

    def record_obstacles(self, grid):
        layer = self.tmxdata.get_layer_by_name("obstacles0")
        for x, y, gid in layer:
            if gid != 0: # Se gid e cero e porque non hai ningun tipo de obstaculo
                grid.single_placement((x,y))
        layer = self.tmxdata.get_layer_by_name("obstacles")
        for x, y, gid in layer:
            if gid != 0: # Se gid e cero e porque non hai ningun tipo de obstaculo
                grid.single_placement((x,y))
        layer = self.tmxdata.get_layer_by_name("obstacles1")
        for x, y, gid in layer:
            if gid != 0: # Se gid e cero e porque non hai ningun tipo de obstaculo
                grid.single_placement((x,y))
                layer = self.tmxdata.get_layer_by_name("obstacles2")
        for x, y, gid in layer:
            if gid != 0: # Se gid e cero e porque non hai ningun tipo de obstaculo
                grid.single_placement((x,y))
    

    def record_path(self, grid,path_id):
        path = set()
        start_pos = (0,0)
        for x, y, gid in self.tmxdata.get_layer_by_name("start_position"):
            if gid == path_id:
                start_pos = (x,y)

        #print("START POSITION: " + str(start_pos))
        layer = self.tmxdata.get_layer_by_name("path")
        for x, y, gid in layer:
            #if gid > 0:        # A MELLOR FERRAMENTA DO MUNDO: facer prints
            #    print("GID:  " + str(gid))
            if gid == path_id:
                grid.path_placing((x,y))
                path.add((x,y))
        #print("PATH:  " + str(path))

        path.discard(start_pos)
        #print("PATH: " + str(path))
        segment_list = []
        # Bucle de segmentos
        while(bool(path)):
            segment = {}
            #print("\nSTART POS: " + str(start_pos))
            # Explorar a direccion do segmento
            if (start_pos[0]-1, start_pos[1]) in path:
                path.discard((start_pos[0]-1, start_pos[1]))
                segment = {"ini": start_pos, "fin": None , "dir": (-1,0)}
            elif (start_pos[0]+1, start_pos[1]) in path:
                path.discard((start_pos[0]+1, start_pos[1]))
                segment = {"ini": start_pos, "fin": None, "dir": (1,0)}
            elif (start_pos[0], start_pos[1]-1) in path:
                path.discard((start_pos[0], start_pos[1]-1))
                segment = {"ini": start_pos, "fin": None, "dir": (0,-1)}
            elif (start_pos[0], start_pos[1]+1) in path:
                path.discard((start_pos[0], start_pos[1]+1))
                segment = {"ini": start_pos, "fin": None, "dir": (0,1)}
            else:
                print("CAMINHO DISCONTINUO")
                return None # Recorrido discontinuo (aborta)
        
            # Atopar ultima posicion do segmento (onde remata)
            end_segment = False
            current_pos = (start_pos[0] + segment["dir"][0], start_pos[1] + segment["dir"][1])
            while(not end_segment):  
                if (current_pos[0] + segment["dir"][0], current_pos[1] + segment["dir"][1]) in path:
                    path.discard((current_pos[0] + segment["dir"][0], current_pos[1] + segment["dir"][1]))
                    current_pos = (current_pos[0] + segment["dir"][0], current_pos[1] + segment["dir"][1])
                else:
                    segment["fin"] = current_pos
                    end_segment = True
            #print("SEGMENT: " + str(segment))
        
            segment_list.append(segment)
            start_pos = current_pos

        #print("lista segmentos: " + str(segment_list))
        return segment_list



    def draw_layer(self, surface, layer):
        ti = self.tmxdata.get_tile_image_by_gid # Tile Image
        for x, y, gid in layer:
            tile = ti(gid)
            if tile:
                tile = pygame.transform.scale(tile,(self.TILESIZE[0], self.TILESIZE[1]))
                surface.blit(tile, (x*self.TILESIZE[0], y*self.TILESIZE[1]))
    
    def draw(self, surface, grid, cond):
        #layer = self.tmxdata.get_layer_by_name("background")
        #self.draw_layer(surface, layer)
        #layer = self.tmxdata.get_layer_by_name("background1")
        #self.draw_layer(surface, layer)
        #if cond:
        #    grid.draw()
        #layer = self.tmxdata.get_layer_by_name("obstacles")
        #self.draw_layer(surface, layer)
        #layer = self.tmxdata.get_layer_by_name("obstacles1")
        #self.draw_layer(surface, layer)
        #layer = self.tmxdata.get_layer_by_name("obstacles2")
        #self.draw_layer(surface, layer)

        ti = self.tmxdata.get_tile_image_by_gid # Tile Image

        for layer in self.tmxdata.visible_layers:
            if layer.name == "obstacles" and cond:
                grid.draw(surface)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile,(self.TILESIZE[0], self.TILESIZE[1]))
                        surface.blit(tile, (x*self.TILESIZE[0], y*self.TILESIZE[1]))
                        #surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
    

    def make_map(self,grid):
        tmp_surface = pygame.Surface((self.width, self.height))
        tmp_surface2 = pygame.Surface((self.width, self.height))
        self.draw(tmp_surface, grid, True)
        self.draw(tmp_surface2, grid, False)
        return [tmp_surface, tmp_surface2]
