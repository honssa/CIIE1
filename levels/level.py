import pygame
from utils.tileset import TileMap
from game import Game
import os
from escena import Escena
from dialogs.endlevel_scene import EndLevelScreen
from enemies.enemy import Enemy, EnemyDead, EnemyVeloz, EnemyTank, EnemyBomb, EnemyEngeneer
import time
import random




# Carga o mapa e as oleadas do nivel 1
class Level1(Escena):
    def __init__(self, director, comander):
        self.director = director
        self.comander = comander
        self.map = TileMap(os.path.join("maps/level1", "mapa1.tmx")) # Crear tileMap
        self.stats = {"chatarra_inicial": 200,
                      "baterias_inicial":0,
                      "pos_camara_inicial": (-1300,-10), # A q estaba antes era (-600,-300)
                      "comander": comander,
                      "n_paths": 1,
                      "paths_id": [13, 14, 15],
                      "gates": [("horizontal", (69,2))]
                      }
        self.game = Game(self.director, self.map, self.stats)

        self.TIME_REST = 10
        self.TIME_WAVE = 30
        self.TIME_LAST_REST = 20
        self.TIME_LAST_WAVE = 30

        self.wave_counter = 0

        self.STATE = "rest" # rest / last_rest /  wave / last_wave / end
        self.timer = time.time()
        self.enemy_gen_timer = time.time()
        self.enemy_buffer = []
        self.nlanes = 3
        self.id_lvl = 1

        if self.id_lvl == 3:
            back_theme = pygame.mixer.music.load("Sounds/novos/last_level_theme_AlexandrZhelanov.ogg")
            back_theme.set_volume(0.5)
            back_theme.play(-1)
        else:
            pygame.mixer.music.load("Sounds/novos/Background_theme_starlik.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)





    def change_states(self):
        if self.game.derrota:
            pygame.mixer.music.stop()
            self.director.cambiarEscena(EndLevelScreen(self.director, self.comander, self.id_lvl, False))

        if self.STATE == "rest":
            if time.time() - self.timer >= self.TIME_REST:
                self.STATE = "wave"
                self.timer = time.time()
                self.enemy_gen_timer = time.time()
                self.wave_counter += 1
                self.generate_enemies(self.wave_counter)
        elif self.STATE == "wave" and self.wave_counter < 7:
            if time.time() - self.timer >= self.TIME_WAVE:
                self.STATE = "rest"
                self.timer = time.time()
        elif self.STATE == "wave":
            if time.time() - self.timer >= self.TIME_WAVE:
                self.STATE = "last_rest"
                self.timer = time.time()
        elif self.STATE == "last_rest":
            print("time: "  +str(time.time() - self.timer))
            if time.time() - self.timer >= self.TIME_LAST_REST:
                self.STATE = "last_wave"
                self.timer = time.time()
                self.wave_counter += 1
                self.generate_enemies(self.wave_counter)
        elif self.STATE == "last_wave":
            if time.time() - self.timer >= self.TIME_LAST_WAVE:
                self.STATE = "end"
                self.timer = time.time()
        elif self.STATE == "end" and len(self.game.enemies.list) == 0:
            pygame.mixer.music.stop()
            self.director.cambiarEscena(EndLevelScreen(self.director, self.comander, self.id_lvl, True))
    





    def filter_enemies(self, enemy_freq):
        margin = random.randrange(100)
        if enemy_freq["normal"]*100 > margin:
            lane = random.randrange(self.nlanes)
            self.enemy_buffer.append(("normal", lane))

        if enemy_freq["veloz"]*100 > margin:
            lane = random.randrange(self.nlanes)
            self.enemy_buffer.append(("veloz", lane))

        if enemy_freq["bomba"]*100 > margin:
            lane = random.randrange(self.nlanes)
            self.enemy_buffer.append(("bomba", lane))

        if enemy_freq["tanque"]*100 > margin:
            lane = random.randrange(self.nlanes)
            self.enemy_buffer.append(("tanque", lane))

        if enemy_freq["enxenheiro"]*100 > margin:
            lane = random.randrange(self.nlanes)
            self.enemy_buffer.append(("enxenheiro", lane))





    def generate_enemies(self, nwave):  # Number of the wave
        enemy_freq = {"normal": 0, "veloz": 0, "bomba": 0, "tanque": 0, "enxenheiro": 0}

        if nwave == 1:
            enemy_freq = {"normal": 0.7, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0}
        if nwave == 2:
            enemy_freq = {"normal": 0.7, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0}
        if nwave == 3:
            enemy_freq = {"normal": 0.4, "veloz": 0.3, "bomba": 0.2, "tanque": 0.1, "enxenheiro": 0}
        if nwave == 4:
            enemy_freq = {"normal": 0.4, "veloz": 0.2, "bomba": 0.2, "tanque": 0.2, "enxenheiro": 0}
        if nwave == 5:
            enemy_freq = {"normal": 0.55, "veloz": 0.3, "bomba": 0.1, "tanque": 0.05, "enxenheiro": 0.1}
        if nwave == 6:
            enemy_freq = {"normal": 0.3, "veloz": 0.3, "bomba": 0.2, "tanque": 0.2, "enxenheiro": 0.1}
        if nwave == 7:
            enemy_freq = {"normal": 0.2, "veloz": 0.3, "bomba": 0.1, "tanque": 0.3, "enxenheiro": 0.1}
        if nwave == 8:
            enemy_freq = {"normal": 0.2, "veloz": 0.3, "bomba": 0, "tanque": 0.4, "enxenheiro": 0.1}

        while len(self.enemy_buffer) < 30:
            self.filter_enemies(enemy_freq)


    

    def update(self, tiempo):
        self.change_states()
        if time.time() - self.enemy_gen_timer >= 1: # A cada segundo da wave spawneamos un enemigo do noso buffer
            self.enemy_gen_timer = time.time()
            if len(self.enemy_buffer) > 0:
                enemy = self.enemy_buffer.pop() 
                self.game.generate_enemy(enemy)
        

        self.game.update(tiempo)


	
    def eventos(self, lista_eventos):
        self.game.eventos(lista_eventos)

    
    def dibujar(self, win):
        self.game.dibujar(win)




class Level2(Level1):
    def __init__(self, director, comander):
        self.director = director
        self.comander = comander
        self.map = TileMap(os.path.join("maps/level2", "mapa2.tmx")) # Crear tileMap
        self.stats = {"chatarra_inicial": 200,
                      "baterias_inicial":0,
                      "pos_camara_inicial": (-950,-900),
                      "comander": comander,
                      "n_paths": 2,
                      "paths_id": [2, 3, 10, 61, 47, 48],   # 3 primeiros: caminho do norte, 3 segundos caminho do este
                      "gates": [("horizontal", (49,30)), ("horizontal", (49,47)), ("vertical", (59,41)), ("vertical", (41,41))]
                      }
        self.game = Game(self.director, self.map, self.stats)

        self.TIME_REST = 10
        self.TIME_WAVE = 30
        self.TIME_LAST_REST = 20
        self.TIME_LAST_WAVE = 30

        self.wave_counter = 0

        self.STATE = "rest" # rest / last_rest /  wave / last_wave / end
        self.timer = time.time()
        self.enemy_gen_timer = time.time()
        self.enemy_buffer = []
        self.nlanes = 6#12 #6
        self.id_lvl = 2

        if self.id_lvl == 3:
            back_theme = pygame.mixer.Sound("Sounds/novos/last_level_theme_AlexandrZhelanov.ogg")
            back_theme.set_volume(0.5)
            back_theme.play(-1)
        else:
            pygame.mixer.music.load("Sounds/novos/Background_theme_starlik.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)


    def generate_enemies(self, nwave):  # Number of the wave
        enemy_freq = {"normal": 0, "veloz": 0, "bomba": 0, "tanque": 0, "enxenheiro": 0}

        if nwave == 1:
            enemy_freq = {"normal": 0.5, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 2:
            enemy_freq = {"normal": 0.5, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 3:
            enemy_freq = {"normal": 0.3, "veloz": 0.2, "bomba": 0.2, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 4:
            enemy_freq = {"normal": 0.1, "veloz": 0.2, "bomba": 0.3, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 5:
            enemy_freq = {"normal": 0.3, "veloz": 0.3, "bomba": 0.1, "tanque": 0.2, "enxenheiro": 0.1}
        if nwave == 6:
            enemy_freq = {"normal": 0.3, "veloz": 0.2, "bomba": 0.2, "tanque": 0.2, "enxenheiro": 0.1}
        if nwave == 7:
            enemy_freq = {"normal": 0.3, "veloz": 0.1, "bomba": 0.2, "tanque": 0.3, "enxenheiro": 0.1}
        if nwave == 8:
            enemy_freq = {"normal": 0.25, "veloz": 0.25, "bomba": 0, "tanque": 0.4, "enxenheiro": 0.1}

        while len(self.enemy_buffer) < 30:
            self.filter_enemies(enemy_freq)



class Level3(Level1):
    def __init__(self, director, comander):
        self.director = director
        self.comander = comander
        self.map = TileMap(os.path.join("maps/level2", "mapa2.tmx")) # Crear tileMap
        self.stats = {"chatarra_inicial": 100,
                      "baterias_inicial":1,
                      "pos_camara_inicial": (-950,-900),
                      "comander": comander,
                      "n_paths": 2,
                      "paths_id": [2, 3, 10, 61, 47, 48, 32, 18, 38, 7, 21, 14],   # 3 terceiros: caminho do oeste, 3 cuartos: caminho do sur
                      "gates": [("horizontal", (49,30)), ("horizontal", (49,47)), ("vertical", (59,41)), ("vertical", (41,41))]
                      }
        self.game = Game(self.director, self.map, self.stats)

        self.TIME_REST = 10
        self.TIME_WAVE = 30
        self.TIME_LAST_REST = 20
        self.TIME_LAST_WAVE = 30

        self.wave_counter = 0

        self.STATE = "rest" # rest / last_rest /  wave / last_wave / end
        self.timer = time.time()
        self.enemy_gen_timer = time.time()
        self.enemy_buffer = []
        self.nlanes = 12#12 #6
        self.id_lvl = 3

        if self.id_lvl == 3:
            back_theme = pygame.mixer.Sound("Sounds/novos/last_level_theme_AlexandrZhelanov.ogg")
            back_theme.set_volume(0.5)
            back_theme.play(-1)
        else:
            pygame.mixer.music.load("Sounds/novos/Background_theme_starlik.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
    

    def generate_enemies(self, nwave):  # Number of the wave
        enemy_freq = {"normal": 0, "veloz": 0, "bomba": 0, "tanque": 0, "enxenheiro": 0}

        if nwave == 1:
            enemy_freq = {"normal": 0.5, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 2:
            enemy_freq = {"normal": 0.5, "veloz": 0.1, "bomba": 0.1, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 3:
            enemy_freq = {"normal": 0.3, "veloz": 0.2, "bomba": 0.2, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 4:
            enemy_freq = {"normal": 0.1, "veloz": 0.2, "bomba": 0.3, "tanque": 0.1, "enxenheiro": 0.2}
        if nwave == 5:
            enemy_freq = {"normal": 0.3, "veloz": 0.3, "bomba": 0.1, "tanque": 0.2, "enxenheiro": 0.1}
        if nwave == 6:
            enemy_freq = {"normal": 0.3, "veloz": 0.2, "bomba": 0.2, "tanque": 0.2, "enxenheiro": 0.1}
        if nwave == 7:
            enemy_freq = {"normal": 0.3, "veloz": 0.1, "bomba": 0.2, "tanque": 0.3, "enxenheiro": 0.1}
        if nwave == 8:
            enemy_freq = {"normal": 0.25, "veloz": 0.25, "bomba": 0, "tanque": 0.4, "enxenheiro": 0.1}

        while len(self.enemy_buffer) < 30:
            self.filter_enemies(enemy_freq)

    